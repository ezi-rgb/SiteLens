from unittest.mock import patch

from fastapi.testclient import TestClient

from sitelens.web.app import app

client = TestClient(app)


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
