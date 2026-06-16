import socket
import ssl
from datetime import datetime, timezone


def run(domain: str) -> dict:
    """
    Checks the SSL/TLS certificate of a domain.

    Returns:
        dict with keys: name, severity, passed, message, recommendation
    """
    name = "SSL/TLS Certificate Check"

    try:
        cert = _get_certificate(domain)
    except Exception as e:
        return {
            "name": name,
            "severity": "high",
            "passed": False,
            "message": f"Could not retrieve SSL certificate: {e}",
            "recommendation": (
                "Make sure the site is reachable over HTTPS (port 443) "
                "and has a valid SSL certificate installed."
            ),
        }

    expiry_str = cert.get("notAfter")
    expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
    expiry_date = expiry_date.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    days_left = (expiry_date - now).days

    if days_left < 0:
        return {
            "name": name,
            "severity": "high",
            "passed": False,
            "message": f"SSL certificate expired {abs(days_left)} day(s) ago.",
            "recommendation": "Renew the SSL certificate immediately.",
        }

    if days_left < 30:
        return {
            "name": name,
            "severity": "medium",
            "passed": False,
            "message": f"SSL certificate expires in {days_left} day(s).",
            "recommendation": "Renew the SSL certificate soon to avoid downtime warnings.",
        }

    return {
        "name": name,
        "severity": "info",
        "passed": True,
        "message": f"SSL certificate is valid for {days_left} more day(s).",
        "recommendation": "No action needed.",
    }


def _get_certificate(domain: str, port: int = 443, timeout: int = 5) -> dict:
    """Opens a TLS connection and returns the certificate dict."""
    context = ssl.create_default_context()
    with socket.create_connection((domain, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            return ssock.getpeercert()
