import argparse
import sys

from colorama import Fore, Style, init

from sitelens.reporter import run_all_checks, to_markdown

SEVERITY_COLORS = {
    "info": Fore.GREEN,
    "low": Fore.CYAN,
    "medium": Fore.YELLOW,
    "high": Fore.RED,
}


def main() -> None:
    init(autoreset=True)  # aktifkan colorama, otomatis reset warna setiap print

    parser = argparse.ArgumentParser(
        prog="sitelens",
        description="Lightweight, non-intrusive security scanner for websites.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a domain for security issues")
    scan_parser.add_argument("domain", help="The domain to scan, e.g. example.com")
    scan_parser.add_argument(
        "--export",
        metavar="FILENAME",
        help="Export the report to a markdown file",
    )

    args = parser.parse_args()

    if args.command == "scan":
        _run_scan(args.domain, args.export)


def _run_scan(domain: str, export_path: str | None) -> None:
    print(f"\nScanning {domain}...\n")

    report = run_all_checks(domain)

    for result in report["results"]:
        color = SEVERITY_COLORS.get(result["severity"], "")
        status = "PASS" if result["passed"] else "ISSUE"
        print(f"{color}[{status}] {result['name']} ({result['severity']}){Style.RESET_ALL}")
        print(f"  {result['message']}")
        if not result["passed"]:
            print(f"  → {result['recommendation']}")
        print()

    summary = report["summary"]
    print(
        f"Summary: {summary['passed']}/{summary['total']} checks passed "
        f"(highest severity: {summary['highest_severity']})"
    )

    if export_path:
        markdown = to_markdown(report)
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"\nReport exported to {export_path}")


if __name__ == "__main__":
    main()
