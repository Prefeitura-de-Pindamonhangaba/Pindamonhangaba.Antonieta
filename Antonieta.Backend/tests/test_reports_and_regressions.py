"""Known defects are explicit expected failures, never silently skipped."""
from datetime import datetime
import unittest

from support import DatabaseTestCase
from models.distribution_model import Distribution


class ReportTests(DatabaseTestCase):
    def setUp(self):
        super().setUp()
        self.stock_id = self.stock()
        beneficiary_id = self.beneficiary()
        with self.sessions() as db:
            db.add_all([
                Distribution(ration_id=self.stock_id, beneficiary_id=beneficiary_id,
                             amount=2.5, date=datetime(2026, 1, 15), old=False),
                Distribution(ration_id=self.stock_id, beneficiary_id=beneficiary_id,
                             amount=4, date=datetime(2026, 2, 28, 23, 59), old=False),
                Distribution(ration_id=self.stock_id, beneficiary_id=beneficiary_id,
                             amount=100, date=datetime(2026, 1, 15), old=True),
            ])
            db.commit()

    def report(self, query):
        response = self.request("GET", "/reports/distribution-volume-by-month?" + query)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_year_report_aggregates_and_excludes_old_records(self):
        report = self.report("year=2026")
        self.assertEqual(report["summary"]["total_volume"], 6.5)
        self.assertEqual(report["summary"]["total_distributions"], 2)
        self.assertEqual(report["summary"]["periods_count"], 2)

    def test_month_filter(self):
        report = self.report("year=2026&month=1")
        self.assertEqual(report["summary"]["total_volume"], 2.5)
        self.assertEqual(report["data"][0]["month_year"], "2026-01")

    def test_date_range_includes_end_of_final_day(self):
        report = self.report("start_date=2026-02-01&end_date=2026-02-28")
        self.assertEqual(report["summary"]["total_volume"], 4)

    def test_nonexistent_ration_returns_empty_report(self):
        report = self.report("year=2026&ration_id=999")
        self.assertEqual(report["data"], [])
        self.assertEqual(report["summary"]["total_volume"], 0)

    def test_invalid_date_returns_400(self):
        response = self.request("GET", "/reports/distribution-volume-by-month?start_date=invalid")
        self.assertEqual(response.status_code, 400, response.text)


class KnownRegressionTests(DatabaseTestCase):
    """Remove expectedFailure as the corresponding production defects are fixed."""

    def test_insufficient_stock_returns_400_without_changing_balance(self):
        """Insufficient stock must be rejected before any balance changes."""
        stock_id = self.stock(1)
        beneficiary_id = self.beneficiary()
        with TestClientWithoutServerExceptions() as client:
            response = client.post("/distribution/", headers=self.user, json={
                "ration_id": stock_id, "beneficiary_id": beneficiary_id,
                "amount": 2, "date": datetime.now().isoformat(),
            })
        self.assertEqual(response.status_code, 400, response.text)
        self.assertEqual(self.balance(stock_id), 1)

    def test_negative_input_rejected_without_changing_balance(self):
        """Only positive finite amounts may increase stock."""
        stock_id = self.stock()
        for amount in (-5, 0):
            with self.subTest(amount=amount):
                response = self.request("POST", "/ration-input/", json={
                    "ration_stock_id": stock_id, "amount": amount,
                    "date": datetime.now().isoformat(), "description": "Invalid donation",
                })
                self.assertEqual(response.status_code, 422, response.text)
                self.assertEqual(self.balance(stock_id), 100)

    def test_invalid_input_update_preserves_existing_amount_and_stock(self):
        stock_id = self.stock()
        payload = {"ration_stock_id": stock_id, "amount": 5,
                   "date": datetime.now().isoformat(), "description": "Donation"}
        created = self.request("POST", "/ration-input/", json=payload)
        self.assertEqual(created.status_code, 200, created.text)
        input_id = created.json()["id"]
        for amount in (-5, 0, "NaN", "Infinity", "-Infinity"):
            with self.subTest(amount=amount):
                response = self.request("PUT", f"/ration-input/{input_id}",
                                        json={**payload, "id": input_id, "amount": amount})
                self.assertEqual(response.status_code, 422, response.text)
                self.assertEqual(self.balance(stock_id), 105)
                self.assertEqual(self.request("GET", f"/ration-input/{input_id}").json()["amount"], 5)

    def test_nonfinite_input_rejected(self):
        stock_id = self.stock()
        for amount in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(amount=amount):
                response = self.request("POST", "/ration-input/", json={
                    "ration_stock_id": stock_id, "amount": amount,
                    "date": datetime.now().isoformat(), "description": "Invalid donation",
                })
                self.assertEqual(response.status_code, 422, response.text)
                self.assertEqual(self.balance(stock_id), 100)

    @unittest.expectedFailure
    def test_distribution_delete_restores_stock(self):
        """BUG: deletion passes the model class to db.delete and does not restore stock."""
        stock_id = self.stock()
        created = self.request("POST", "/distribution/", json={
            "ration_id": stock_id, "beneficiary_id": self.beneficiary(),
            "amount": 5, "date": datetime.now().isoformat(),
        })
        self.assertEqual(created.status_code, 200, created.text)
        with TestClientWithoutServerExceptions() as client:
            response = client.delete(f"/distribution/{created.json()['id']}", headers=self.user)
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(self.balance(stock_id), 100)


def TestClientWithoutServerExceptions():
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app, raise_server_exceptions=False)
