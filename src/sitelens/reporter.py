from datetime import datetime, timezone

from sitelens.checks import dns_check, exposed_files_check, headers_check, ssl_check

ALL_CHECKS = [
    ssl_check.run,
    headers_check.run,
    dns_check.run,
    exposed_files_check.run,
]


def run_all_checks(domain: str) -> dict:
    """
    Runs every registered check against the given domain and returns
    a structured report.

    Returns:
        {
            "domain": str,
            "scanned_at": str (ISO timestamp),
            "results": list[dict],
            "summary": {
                "total": int,
                "passed": int,
                "failed": int,
                "highest_severity": str,
            }
        }
    """
    results = [check(domain) for check in ALL_CHECKS]

    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count
    severities = [r["severity"] for r in results]

    return {
        "domain": domain,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": {
            "total": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "highest_severity": _highest_severity(severities),
        },
    }


def _highest_severity(severities: list[str]) -> str:
    order = ["info", "low", "medium", "high"]
    return max(severities, key=order.index)


def to_markdown(report: dict) -> str:
    """Converts a report dict into a human-readable markdown string."""
    lines = [
        f"# Security Scan Report: {report['domain']}",
        "",
        f"Scanned at: {report['scanned_at']}",
        "",
        f"**Summary:** {report['summary']['passed']}/{report['summary']['total']} checks passed "
        f"(highest severity: {report['summary']['highest_severity']})",
        "",
    ]

    for result in report["results"]:
        status_icon = "✅" if result["passed"] else "⚠️"
        lines.append(f"## {status_icon} {result['name']} ({result['severity']})")
        lines.append("")
        lines.append(f"- **Finding:** {result['message']}")
        lines.append(f"- **Recommendation:** {result['recommendation']}")
        lines.append("")

    return "\n".join(lines)
