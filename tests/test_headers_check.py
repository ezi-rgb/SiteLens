from unittest.mock import MagicMock, patch

from sitelens.checks import headers_check


@patch("sitelens.checks.headers_check.requests.get")
def test_site_with_all_headers_present_passes(mock_get):
    mock_response = MagicMock()
    mock_response.headers = {
        "Strict-Transport-Security": "max-age=31536000",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "no-referrer",
    }
    mock_get.return_value = mock_response

    result = headers_check.run("example.com")

    assert result["passed"] is True
    assert result["severity"] == "info"


@patch("sitelens.checks.headers_check.requests.get")
def test_site_missing_some_headers_fails(mock_get):
    mock_response = MagicMock()
    mock_response.headers = {
        "X-Frame-Options": "DENY",
        # Header lain sengaja tidak disertakan untuk simulasi "hilang"
    }
    mock_get.return_value = mock_response

    result = headers_check.run("example.com")

    assert result["passed"] is False
    assert "Strict-Transport-Security" in result["message"]


@patch("sitelens.checks.headers_check.requests.get")
def test_unreachable_domain_returns_high_severity_error(mock_get):
    import requests
    mock_get.side_effect = requests.RequestException("Connection failed")

    result = headers_check.run("this-domain-does-not-exist-12345.invalid")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert "Could not connect" in result["message"]
