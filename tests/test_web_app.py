from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

from sitelens.web import database
from sitelens.web.app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_temporary_database(monkeypatch, tmp_path):
    """Ensures the web app tests use a fresh, temporary database with tables created."""
    test_db_path = tmp_path / "test_sitelens.db"
    test_engine = create_engine(f"sqlite:///{test_db_path}")
    monkeypatch.setattr(database, "engine", test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "SiteLens" in response.text


@patch("sitelens.web.app.run_all_checks")
@patch("sitelens.web.app.save_scan")
def test_scan_endpoint_redirects_to_home(mock_save_scan, mock_run_all_checks):
    mock_run_all_checks.return_value = {
        "domain": "example.com",
        "scanned_at": "2026-01-01T00:00:00",
        "results": [],
        "summary": {"total": 1, "passed": 1, "failed": 0, "highest_severity": "info"},
    }

    response = client.post("/scan", data={"domain": "example.com"}, follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/"
