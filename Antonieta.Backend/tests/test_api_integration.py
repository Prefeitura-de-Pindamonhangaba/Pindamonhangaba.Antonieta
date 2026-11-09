from datetime import datetime
import unittest

from support import DatabaseTestCase
from models.audit_log_model import AuditLog
from models.beneficiary_model import Beneficiary
from models.user_model import User
from services.auth_service import verify_password


class AuthenticationTests(DatabaseTestCase):
    def login(self, password="TestPassword123!"):
        return self.client.post("/auth/token", data={
            "grant_type": "password", "username": "user@example.com", "password": password,
        })

    def test_login_returns_usable_token_without_password_hash(self):
        response = self.login()
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertNotIn("hashed_password", data["user"])
        me = self.request("GET", "/auth/me", headers={
            "Authorization": "Bearer " + data["access_token"],
        })
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.json()["email"], "user@example.com")

    def test_wrong_password_rejected(self):
        self.assertEqual(self.login("wrong").status_code, 401)

    def test_login_records_audit(self):
        self.assertEqual(self.login().status_code, 200)
        with self.sessions() as db:
            log = db.query(AuditLog).filter_by(action="LOGIN_SUCCESS").one()
            self.assertEqual(log.user_id, 2)
            self.assertNotIn("TestPassword123!", str(log.changes))

    def test_refresh_returns_usable_token(self):
        response = self.request("POST", "/auth/refresh")
        self.assertEqual(response.status_code, 200, response.text)
        me = self.request("GET", "/auth/me", headers={
            "Authorization": "Bearer " + response.json()["access_token"],
        })
        self.assertEqual(me.status_code, 200)

    def test_token_for_deleted_user_rejected(self):
        with self.sessions() as db:
            db.delete(db.get(User, 2))
            db.commit()
        self.assertEqual(self.request("GET", "/auth/me").status_code, 401)

    def test_admin_permission_uses_current_database_role(self):
        with self.sessions() as db:
            db.get(User, 1).role = "comum"
            db.commit()
        self.assertEqual(self.request("GET", "/users/", headers=self.admin).status_code, 403)


class UserManagementTests(DatabaseTestCase):
    def create_user(self):
        return self.request("POST", "/users/", headers=self.admin, json={
            "email": "new@example.com", "password": "NewPassword123!", "full_name": "New User",
        })

    def test_admin_creates_user_with_hashed_password_and_audit(self):
        response = self.create_user()
        self.assertEqual(response.status_code, 200, response.text)
        self.assertNotIn("hashed_password", response.json())
        with self.sessions() as db:
            user = db.get(User, response.json()["id"])
            self.assertNotEqual(user.hashed_password, "NewPassword123!")
            self.assertTrue(verify_password("NewPassword123!", user.hashed_password))
            self.assertEqual(db.query(AuditLog).filter_by(action="CREATE", entity_id=user.id).count(), 1)

    def test_duplicate_email_rejected(self):
        self.assertEqual(self.create_user().status_code, 200)
        self.assertEqual(self.create_user().status_code, 400)

    def test_admin_updates_user_and_records_changes(self):
        response = self.request("PUT", "/users/2", headers=self.admin,
                                json={"full_name": "Updated", "role": "administrador"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["role"], "administrador")
        with self.sessions() as db:
            self.assertEqual(db.query(AuditLog).filter_by(action="UPDATE").one().changes[
                "role"]["old"], "comum")

    def test_admin_cannot_delete_self(self):
        self.assertEqual(self.request("DELETE", "/users/1", headers=self.admin).status_code, 400)

    def test_admin_deletes_user(self):
        self.assertEqual(self.request("DELETE", "/users/2", headers=self.admin).status_code, 204)
        self.assertEqual(self.request("GET", "/users/2", headers=self.admin).status_code, 404)

    def test_unknown_user_returns_404(self):
        self.assertEqual(self.request("GET", "/users/999", headers=self.admin).status_code, 404)

    def test_invalid_role_rejected(self):
        response = self.request("PUT", "/users/2", headers=self.admin, json={"role": "superadmin"})
        self.assertEqual(response.status_code, 422)

    def test_common_user_cannot_read_audit(self):
        self.assertEqual(self.request("GET", "/audit/logs").status_code, 403)

    def test_admin_can_filter_audit(self):
        self.create_user()
        response = self.request("GET", "/audit/logs?action=CREATE", headers=self.admin)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["action"], "CREATE")


class BusinessFlowTests(DatabaseTestCase):
    def test_beneficiary_create_read_delete(self):
        beneficiary_id = self.beneficiary()
        self.assertEqual(self.request("GET", f"/beneficiary/{beneficiary_id}").status_code, 200)
        self.assertEqual(self.request("DELETE", f"/beneficiary/{beneficiary_id}").status_code, 200)
        self.assertEqual(self.request("GET", f"/beneficiary/{beneficiary_id}").status_code, 404)

    def test_invalid_beneficiary_rejected(self):
        self.assertEqual(self.request("POST", "/beneficiary/", json={"name": "A"}).status_code, 422)

    def test_old_beneficiary_hidden_from_list_and_detail(self):
        beneficiary_id = self.beneficiary()
        with self.sessions() as db:
            db.get(Beneficiary, beneficiary_id).old = True
            db.commit()
        self.assertEqual(self.request("GET", "/beneficiary/").json(), [[], 0])
        self.assertEqual(self.request("GET", f"/beneficiary/{beneficiary_id}").status_code, 404)

    def test_input_create_update_delete_adjusts_stock(self):
        stock_id = self.stock()
        payload = {"ration_stock_id": stock_id, "amount": 5.5,
                   "date": datetime.now().isoformat(), "description": "Donation"}
        response = self.request("POST", "/ration-input/", json=payload)
        self.assertEqual(response.status_code, 200, response.text)
        input_id = response.json()["id"]
        self.assertEqual(self.balance(stock_id), 105.5)
        response = self.request("PUT", f"/ration-input/{input_id}",
                                json={**payload, "id": input_id, "amount": 8.25})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(stock_id), 108.25)
        self.assertEqual(self.request("DELETE", f"/ration-input/{input_id}").status_code, 200)
        self.assertEqual(self.balance(stock_id), 100)

    def test_input_route_body_id_mismatch_rejected(self):
        response = self.request("PUT", "/ration-input/1", json={
            "id": 2, "ration_stock_id": 1, "amount": 1,
            "date": datetime.now().isoformat(), "description": "Donation",
        })
        self.assertEqual(response.status_code, 400)

    def test_missing_input_returns_404(self):
        self.assertEqual(self.request("GET", "/ration-input/999").status_code, 404)

    def test_distribution_deducts_fractional_stock(self):
        stock_id = self.stock()
        response = self.request("POST", "/distribution/", json={
            "ration_id": stock_id, "beneficiary_id": self.beneficiary(),
            "amount": 2.75, "date": datetime.now().isoformat(),
        })
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(stock_id), 97.25)

    def test_dashboard_empty_totals(self):
        for path, key in [("total-inputs-month", "total_amount"),
                          ("total-distributions-month", "total_amount"),
                          ("current-total-stock", "current_stock")]:
            with self.subTest(path=path):
                response = self.request("GET", "/dashboard/" + path)
                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(response.json()[key], 0)

    def test_dashboard_stock_reflects_balance(self):
        self.stock(12.5)
        response = self.request("GET", "/dashboard/current-total-stock")
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["current_stock"], 12.5)


if __name__ == "__main__":
    unittest.main()
