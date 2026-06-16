import requests

COMMON_SENSITIVE_FILES = [
    ".env",
    ".git/config",
    ".git/HEAD",
    "wp-config.php.bak",
    "config.php.bak",
    "backup.zip",
    "db_backup.sql",
    "phpinfo.php",
    ".htpasswd",
    "composer.json",
]


def run(domain: str) -> dict:
    """
    Checks if common sensitive files are publicly accessible.

    Returns:
        dict with keys: name, severity, passed, message, recommendation
    """
    name = "Exposed Sensitive Files Check"
    base_url = f"https://{domain}"

    exposed = []
    for filename in COMMON_SENSITIVE_FILES:
        if _is_publicly_accessible(base_url, filename):
            exposed.append(filename)

    if not exposed:
        return {
            "name": name,
            "severity": "info",
            "passed": True,
            "message": "No common sensitive files were found exposed.",
            "recommendation": "No action needed.",
        }

    return {
        "name": name,
        "severity": "high",
        "passed": False,
        "message": f"Publicly accessible sensitive file(s) found: {', '.join(exposed)}.",
        "recommendation": (
            "Remove or block public access to these files immediately. "
            "Sensitive files like .env or .git should never be reachable "
            "via a direct URL."
        ),
    }


def _is_publicly_accessible(base_url: str, filename: str, timeout: int = 5) -> bool:
    """Returns True if the given file returns a 200 OK response."""
    url = f"{base_url}/{filename}"
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=False)
    except requests.RequestException:
        return False

    return response.status_code == 200
