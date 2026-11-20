"""Meaningful API tests with a fake store. Real PostgreSQL integration comes next."""

import pytest
from fastapi.testclient import TestClient

from app.db import get_store
from app.main import app


class FakeStore:
    def __init__(self):
        self.available = True
        self.items = {}
        self.next_id = 1

    def ping(self):
        if not self.available:
            raise ConnectionError("test database offline")

    def create_item(self, name):
        self.ping()
        item_id = self.next_id
        self.items[item_id] = name
        self.next_id += 1
        return item_id, name

    def get_item(self, item_id):
        self.ping()
        if item_id not in self.items:
            return None
        return item_id, self.items[item_id]


@pytest.fixture
def client_and_store():
    store = FakeStore()
    app.dependency_overrides[get_store] = lambda: store
    try:
        with TestClient(app) as client:
            yield client, store
    finally:
        app.dependency_overrides.clear()


def test_create_and_read_item(client_and_store):
    client, _ = client_and_store
    created = client.post("/items", json={"name": "  notebook  "})
    assert created.status_code == 201
    assert created.json() == {"id": 1, "name": "notebook"}
    found = client.get("/items/1")
    assert found.status_code == 200
    assert found.json() == created.json()


def test_empty_names_are_rejected(client_and_store):
    client, _ = client_and_store
    assert client.post("/items", json={"name": "   "}).status_code == 422
    assert client.post("/items", json={"name": ""}).status_code == 422


def test_not_found(client_and_store):
    client, _ = client_and_store
    assert client.get("/items/999").status_code == 404


def test_liveness_is_independent_of_database(client_and_store):
    client, store = client_and_store
    store.available = False
    assert client.get("/healthz").status_code == 200
    assert client.get("/readyz").status_code == 503


def test_readiness_when_db_available(client_and_store):
    client, _ = client_and_store
    assert client.get("/readyz").json() == {"status": "ready"}


def test_metrics_expose_real_request_counts_and_latency(client_and_store):
    client, _ = client_and_store
    client.get("/healthz")
    client.get("/items/999")
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "shipops_http_requests_total" in metrics.text
    assert "shipops_http_failed_requests_total" in metrics.text
    assert "shipops_http_request_duration_seconds_bucket" in metrics.text


def test_version_response(client_and_store, monkeypatch):
    client, _ = client_and_store
    monkeypatch.setenv("RELEASE_VERSION", "sha-test123")
    assert client.get("/version").json() == {"version": "sha-test123"}
