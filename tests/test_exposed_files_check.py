from unittest.mock import MagicMock, patch

from sitelens.checks import exposed_files_check


@patch("sitelens.checks.exposed_files_check.requests.get")
def test_no_files_exposed_passes(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = exposed_files_check.run("example.com")

    assert result["passed"] is True
    assert result["severity"] == "info"


@patch("sitelens.checks.exposed_files_check.requests.get")
def test_env_file_exposed_returns_high_severity(mock_get):
    def get_side_effect(url, timeout=5, allow_redirects=False):
        mock_response = MagicMock()
        mock_response.status_code = 200 if url.endswith("/.env") else 404
        return mock_response

    mock_get.side_effect = get_side_effect

    result = exposed_files_check.run("example.com")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert ".env" in result["message"]


@patch("sitelens.checks.exposed_files_check.requests.get")
def test_unreachable_domain_does_not_crash(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Connection failed")

    result = exposed_files_check.run("this-domain-does-not-exist-12345.invalid")

    assert "passed" in result
    assert "severity" in result
