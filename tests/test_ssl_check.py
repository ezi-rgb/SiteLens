from sitelens.checks import ssl_check


def test_valid_domain_returns_passed_true():
    result = ssl_check.run("github.com")

    assert result["name"] == "SSL/TLS Certificate Check"
    assert "severity" in result
    assert "message" in result
    assert "recommendation" in result
    # github.com selalu punya sertifikat valid dengan masa berlaku panjang
    assert result["passed"] is True


def test_invalid_domain_returns_high_severity_error():
    result = ssl_check.run("this-domain-does-not-exist-12345.invalid")

    assert result["passed"] is False
    assert result["severity"] == "high"
    assert "Could not retrieve" in result["message"]
