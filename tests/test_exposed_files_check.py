from sitelens.checks import exposed_files_check


def test_domain_with_no_exposed_files_passes():
    # github.com tidak memiliki file .env atau .git yang terekspos
    result = exposed_files_check.run("github.com")

    assert result["name"] == "Exposed Sensitive Files Check"
    assert "severity" in result
    assert "message" in result
    assert "recommendation" in result


def test_unreachable_domain_does_not_crash():
    # Domain tidak valid harus tetap menghasilkan struktur data yang benar,
    # bukan crash, meskipun semua percobaan request gagal
    result = exposed_files_check.run("this-domain-does-not-exist-12345.invalid")

    assert "passed" in result
    assert "severity" in result
