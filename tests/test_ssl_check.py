import ssl
import socket
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from sitelens.checks import ssl_check


def _fake_cert(days_from_now: int) -> dict:
    """Helper to build a fake certificate dict with a given expiry offset."""
    expiry = datetime.now(timezone.utc) + timedelta(days=days_from_now)
    return {"notAfter": expiry.strftime("%b %d %H:%M:%S %Y GMT")}


@patch("sitelens.checks.ssl_check._get_certificate")
def test_valid_certificate_with_long_expiry_passes(mock_get_cert):
    mock_get_cert.return_value = _fake_cert(days_from_now=200)

    result = ssl_check.run("example.com")

    assert result["passed"] is True
    assert result["severity"] == "info"


@patch("sitelens.checks.ssl_check._get_certificate")
def test_certificate_expiring_soon_returns_medium_severity(mock_get_cert):
    mock_get_cert.return_value = _fake_cert(days_from_now=15)

    result = ssl_check.run("example.com")

    assert result["passed"] is False
    assert result["severity"] == "medium"
    assert "expires in" in result["message"]


@patch("sitelens.checks.ssl_check._get_certificate")
def test_expired_certificate_returns_high_severity(mock_get_cert):
    mock_get_cert.return_value = _fake_cert(days_from_now=-5)

    result = ssl_check.run("example.com")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert "expired" in result["message"]


@patch("sitelens.checks.ssl_check._get_certificate")
def test_connection_error_returns_high_severity(mock_get_cert):
    mock_get_cert.side_effect = socket.timeout("Connection timed out")

    result = ssl_check.run("this-domain-does-not-exist-12345.invalid")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert "Could not retrieve" in result["message"]
