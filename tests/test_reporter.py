from sitelens.reporter import run_all_checks, to_markdown


def test_run_all_checks_returns_full_report_structure():
    report = run_all_checks("github.com")

    assert report["domain"] == "github.com"
    assert "scanned_at" in report
    assert len(report["results"]) == 4
    assert report["summary"]["total"] == 4
    assert report["summary"]["passed"] + report["summary"]["failed"] == 4


def test_to_markdown_produces_readable_output():
    report = run_all_checks("github.com")
    markdown = to_markdown(report)

    assert "# Security Scan Report: github.com" in markdown
    assert "Summary:" in markdown
    # Setiap nama check harus muncul di laporan
    assert "SSL/TLS Certificate Check" in markdown
