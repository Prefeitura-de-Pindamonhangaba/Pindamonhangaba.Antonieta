"""Run with: python -m unittest discover -s tests -v (from backend)."""
import os
import unittest
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

# Isolate tests from the configured application database and JWT secrets.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "security-tests-only-secret-key"
os.environ["ALGORITHM"] = "HS256"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from database import get_db
from main import app
from services.auth_service import create_access_token, get_current_user


class EndpointSecurityTests(unittest.TestCase):
    def setUp(self):
        app.dependency_overrides[get_db] = lambda: None
        self.client = TestClient(app)
        self.routes = [route for route in app.routes if isinstance(route, APIRoute)]

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()

    def request_route(self, route, headers=None):
        path = route.path
        for name in route.param_convertors:
            path = path.replace("{" + name + "}", "1")
        return self.client.request(sorted(route.methods)[0], path, headers=headers)

    def test_every_endpoint_except_login_requires_authentication(self):
        for route in self.routes:
            if route.path == "/auth/token":
                continue
            with self.subTest(path=route.path, methods=route.methods):
                response = self.request_route(route)
                self.assertEqual(response.status_code, 401, response.text)
                self.assertEqual(response.headers["www-authenticate"], "Bearer")

    def test_invalid_and_expired_tokens_are_rejected_on_every_protected_route(self):
        expired = create_access_token(
            {"sub": "user@example.com"}, timedelta(minutes=-1)
        )
        for token in ("invalid-token", expired):
            for route in self.routes:
                if route.path == "/auth/token":
                    continue
                with self.subTest(path=route.path, token=token):
                    response = self.request_route(
                        route, {"Authorization": f"Bearer {token}"}
                    )
                    self.assertEqual(response.status_code, 401, response.text)

    def test_common_user_cannot_access_any_user_management_endpoint(self):
        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
            id=1, email="user@example.com", role="comum"
        )
        for route in self.routes:
            if route.path.startswith("/users"):
                with self.subTest(methods=route.methods, path=route.path):
                    response = self.request_route(route)
                    self.assertEqual(response.status_code, 403, response.text)

    def test_admin_can_list_users(self):
        app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
            id=1, email="admin@example.com", role="administrador"
        )
        with patch("controllers.user_controller.get_all_users", return_value=[]):
            self.assertEqual(self.client.get("/users/").status_code, 200)

    def test_authenticated_common_user_can_access_business_endpoints(self):
        token = create_access_token({"sub": "user@example.com"})
        user = SimpleNamespace(id=1, email="user@example.com", role="comum")
        with patch("services.auth_service.get_user", return_value=user), patch(
            "controllers.beneficiary_controller.get_all_beneficiaries_service",
            return_value=([], 0),
        ):
            response = self.client.get(
                "/beneficiary/", headers={"Authorization": f"Bearer {token}"}
            )
        self.assertEqual(response.status_code, 200, response.text)

    def test_login_remains_public(self):
        with patch("controllers.auth_controller.authenticate_user", return_value=None):
            response = self.client.post("/auth/token", data={
                "grant_type": "password", "username": "user@example.com",
                "password": "wrong-password",
            })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Email ou senha incorretos")

    def test_api_documentation_is_not_public(self):
        for path in ("/docs", "/redoc", "/openapi.json"):
            self.assertEqual(self.client.get(path).status_code, 404)


if __name__ == "__main__":
    unittest.main()
