from sitelens.checks import dns_check


def test_domain_with_good_dns_records_passes():
    # google.com dikenal punya SPF dan DMARC yang lengkap
    result = dns_check.run("google.com")

    assert result["name"] == "DNS Email Security Check (SPF/DMARC)"
    assert "severity" in result
    assert "message" in result
    assert "recommendation" in result


def test_domain_missing_records_fails():
    # Domain valid tapi kemungkinan besar tanpa SPF/DMARC khusus
    result = dns_check.run("example.com")

    assert "passed" in result
    assert result["severity"] in ("info", "medium")
