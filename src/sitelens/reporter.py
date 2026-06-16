import importlib
import pkgutil
from datetime import datetime, timezone

from sitelens import checks


def discover_checks() -> list:
    """
    Automatically discovers all check modules inside sitelens.checks
    and returns a list of their `run` functions.

    A valid check module must define a `run(domain: str) -> dict` function.
    Modules that don't follow this contract are skipped with a warning.
    """
    check_functions = []

    for module_info in pkgutil.iter_modules(checks.__path__):
        module = importlib.import_module(f"sitelens.checks.{module_info.name}")

        if not hasattr(module, "run"):
            print(
                f"Warning: skipping '{module_info.name}' — "
                f"no 'run' function found."
            )
            continue

        check_functions.append(module.run)

    return check_functions


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
    checks_to_run = discover_checks()
    results = [check(domain) for check in checks_to_run]

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
