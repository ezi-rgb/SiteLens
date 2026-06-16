from unittest.mock import patch

from sitelens.reporter import discover_checks, run_all_checks, to_markdown


def _fake_check_result(passed: bool, severity: str = "info") -> dict:
    return {
        "name": "Fake Check",
        "severity": severity,
        "passed": passed,
        "message": "Fake message",
        "recommendation": "Fake recommendation",
    }


def test_discover_checks_finds_all_core_checks():
    check_functions = discover_checks()

    assert len(check_functions) >= 4
    for check_function in check_functions:
        assert callable(check_function)


@patch("sitelens.reporter.discover_checks")
def test_run_all_checks_returns_full_report_structure(mock_discover):
    mock_discover.return_value = [
        lambda domain: _fake_check_result(passed=True),
        lambda domain: _fake_check_result(passed=False, severity="medium"),
    ]

    report = run_all_checks("example.com")

    assert report["domain"] == "example.com"
    assert "scanned_at" in report
    assert len(report["results"]) == 2
    assert report["summary"]["total"] == 2
    assert report["summary"]["passed"] == 1
    assert report["summary"]["failed"] == 1


@patch("sitelens.reporter.discover_checks")
def test_to_markdown_produces_readable_output(mock_discover):
    mock_discover.return_value = [lambda domain: _fake_check_result(passed=True)]

    report = run_all_checks("example.com")
    markdown = to_markdown(report)

    assert "# Security Scan Report: example.com" in markdown
    assert "Summary:" in markdown
    assert "Fake Check" in markdown
