import requests

REQUIRED_HEADERS = {
    "Strict-Transport-Security": {
        "severity": "medium",
        "recommendation": (
            "Add the Strict-Transport-Security header to force browsers "
            "to always use HTTPS for this site."
        ),
    },
    "X-Frame-Options": {
        "severity": "medium",
        "recommendation": (
            "Add the X-Frame-Options header to prevent this site from "
            "being embedded in a clickjacking iframe attack."
        ),
    },
    "X-Content-Type-Options": {
        "severity": "low",
        "recommendation": (
            "Add the X-Content-Type-Options: nosniff header to prevent "
            "MIME type sniffing attacks."
        ),
    },
    "Content-Security-Policy": {
        "severity": "medium",
        "recommendation": (
            "Add a Content-Security-Policy header to restrict which "
            "sources of scripts, styles, and other resources can load."
        ),
    },
    "Referrer-Policy": {
        "severity": "low",
        "recommendation": (
            "Add a Referrer-Policy header to control what information "
            "is shared when users click outbound links."
        ),
    },
}


def run(domain: str) -> dict:
    """
    Checks for the presence of common security-related HTTP headers.

    Returns:
        dict with keys: name, severity, passed, message, recommendation
    """
    name = "Security Headers Check"
    url = f"https://{domain}"

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        return {
            "name": name,
            "severity": "high",
            "passed": False,
            "message": f"Could not connect to {url}: {e}",
            "recommendation": "Make sure the site is reachable over HTTPS.",
        }

    missing = []
    for header, info in REQUIRED_HEADERS.items():
        if header not in response.headers:
            missing.append({"header": header, **info})

    if not missing:
        return {
            "name": name,
            "severity": "info",
            "passed": True,
            "message": "All common security headers are present.",
            "recommendation": "No action needed.",
        }

    highest_severity = _highest_severity([m["severity"] for m in missing])
    missing_names = ", ".join(m["header"] for m in missing)
    recommendations = " ".join(m["recommendation"] for m in missing)

    return {
        "name": name,
        "severity": highest_severity,
        "passed": False,
        "message": f"Missing security headers: {missing_names}.",
        "recommendation": recommendations,
    }


def _highest_severity(severities: list[str]) -> str:
    """Returns the most severe level among a list of severities."""
    order = ["info", "low", "medium", "high"]
    return max(severities, key=order.index)
