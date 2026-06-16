from sitelens.checks import headers_check


def test_site_with_good_headers_passes():
    # github.com dikenal menerapkan banyak security header dengan baik
    result = headers_check.run("github.com")

    assert result["name"] == "Security Headers Check"
    assert "severity" in result
    assert "message" in result
    assert "recommendation" in result


def test_unreachable_domain_returns_high_severity_error():
    result = headers_check.run("this-domain-does-not-exist-12345.invalid")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert "Could not connect" in result["message"]
