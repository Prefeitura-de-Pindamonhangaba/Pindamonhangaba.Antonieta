"""Isolated database and real HTTP/JWT fixtures for backend integration tests."""
import os
import unittest
from unittest.mock import patch

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "security-tests-only-secret-key"
os.environ["ALGORITHM"] = "HS256"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base
from main import app
from models.user_model import User
from services.auth_service import create_access_token, get_password_hash


class DatabaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.password_hash = get_password_hash("TestPassword123!")

    def make_engine(self):
        return create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )

    def setUp(self):
        self.engine = self.make_engine()

        if self.engine.dialect.name == 'sqlite':
            @event.listens_for(self.engine, "connect")
            def enable_foreign_keys(connection, _):
                connection.execute("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)
        self.addCleanup(self.engine.dispose)
        self.db_patch = patch("database.SessionLocal", self.sessions)
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        self.addCleanup(app.dependency_overrides.clear)
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        with self.sessions() as db:
            db.add_all([
                User(id=1, email="admin@example.com", full_name="Admin",
                     role="administrador", hashed_password=self.password_hash),
                User(id=2, email="user@example.com", full_name="User",
                     role="comum", hashed_password=self.password_hash),
            ])
            db.commit()
        self.admin = self.headers("admin@example.com")
        self.user = self.headers("user@example.com")

    def headers(self, email):
        return {"Authorization": "Bearer " + create_access_token({"sub": email})}

    def request(self, method, path, **kwargs):
        kwargs.setdefault("headers", self.user)
        return self.client.request(method, path, **kwargs)

    def stock(self, amount=100):
        response = self.request("POST", "/ration-stock/", json={
            "name": "Test ration", "description": "Test", "unit": "kg", "stock": amount,
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["id"]

    def beneficiary(self):
        response = self.request("POST", "/beneficiary/", json={
            "name": "Test Person", "document": "12345678900", "contact": "12999999999",
            "street": "Test Street", "neighborhood": "Centro",
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["id"]

    def balance(self, stock_id):
        response = self.request("GET", f"/ration-stock/{stock_id}")
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["stock"]
