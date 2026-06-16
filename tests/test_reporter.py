from sitelens.reporter import discover_checks, run_all_checks, to_markdown


def test_discover_checks_finds_all_core_checks():
    check_functions = discover_checks()

    # Minimal harus menemukan 4 check inti V1: ssl, headers, dns, exposed_files
    assert len(check_functions) >= 4

    # Setiap item harus berupa function yang bisa dipanggil
    for check_function in check_functions:
        assert callable(check_function)


def test_run_all_checks_returns_full_report_structure():
    report = run_all_checks("github.com")

    assert report["domain"] == "github.com"
    assert "scanned_at" in report
    assert len(report["results"]) >= 4  # minimal 4 check inti V1
    assert report["summary"]["total"] == len(report["results"])
    assert report["summary"]["passed"] + report["summary"]["failed"] == len(report["results"])


def test_to_markdown_produces_readable_output():
    report = run_all_checks("github.com")
    markdown = to_markdown(report)

    assert "# Security Scan Report: github.com" in markdown
    assert "Summary:" in markdown
    # Setiap nama check harus muncul di laporan
    assert "SSL/TLS Certificate Check" in markdown
