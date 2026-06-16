import dns.resolver


def run(domain: str) -> dict:
    """
    Checks for the presence of SPF and DMARC DNS records.

    Returns:
        dict with keys: name, severity, passed, message, recommendation
    """
    name = "DNS Email Security Check (SPF/DMARC)"

    has_spf = _has_spf_record(domain)
    has_dmarc = _has_dmarc_record(domain)

    if has_spf and has_dmarc:
        return {
            "name": name,
            "severity": "info",
            "passed": True,
            "message": "SPF and DMARC records are both present.",
            "recommendation": "No action needed.",
        }

    missing = []
    if not has_spf:
        missing.append("SPF")
    if not has_dmarc:
        missing.append("DMARC")

    return {
        "name": name,
        "severity": "medium",
        "passed": False,
        "message": f"Missing DNS record(s): {', '.join(missing)}.",
        "recommendation": (
            "Add the missing record(s) to your domain's DNS settings to "
            "help prevent email spoofing and phishing using your domain."
        ),
    }


def _has_spf_record(domain: str) -> bool:
    """Checks if the domain has a TXT record starting with 'v=spf1'."""
    try:
        answers = dns.resolver.resolve(domain, "TXT")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return False

    for record in answers:
        if "v=spf1" in str(record):
            return True
    return False


def _has_dmarc_record(domain: str) -> bool:
    """Checks if _dmarc.<domain> has a TXT record starting with 'v=DMARC1'."""
    dmarc_domain = f"_dmarc.{domain}"
    try:
        answers = dns.resolver.resolve(dmarc_domain, "TXT")
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return False

    for record in answers:
        if "v=DMARC1" in str(record):
            return True
    return False
