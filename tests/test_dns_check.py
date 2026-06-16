import dns.resolver
from unittest.mock import MagicMock, patch

from sitelens.checks import dns_check


def _fake_txt_answer(record_text: str) -> list:
    """Helper to build a fake DNS TXT answer list."""
    fake_record = MagicMock()
    fake_record.__str__.return_value = record_text
    return [fake_record]


@patch("sitelens.checks.dns_check.dns.resolver.resolve")
def test_domain_with_both_records_passes(mock_resolve):
    def resolve_side_effect(query_domain, record_type):
        if query_domain.startswith("_dmarc."):
            return _fake_txt_answer('"v=DMARC1; p=reject;"')
        return _fake_txt_answer('"v=spf1 include:_spf.example.com ~all"')

    mock_resolve.side_effect = resolve_side_effect

    result = dns_check.run("example.com")

    assert result["passed"] is True
    assert result["severity"] == "info"


@patch("sitelens.checks.dns_check.dns.resolver.resolve")
def test_domain_missing_dmarc_fails(mock_resolve):
    def resolve_side_effect(query_domain, record_type):
        if query_domain.startswith("_dmarc."):
            raise dns.resolver.NXDOMAIN()
        return _fake_txt_answer('"v=spf1 include:_spf.example.com ~all"')

    mock_resolve.side_effect = resolve_side_effect

    result = dns_check.run("example.com")

    assert result["passed"] is False
    assert "DMARC" in result["message"]
    assert "SPF" not in result["message"]


@patch("sitelens.checks.dns_check.dns.resolver.resolve")
def test_domain_missing_both_records_fails(mock_resolve):
    mock_resolve.side_effect = dns.resolver.NXDOMAIN()

    result = dns_check.run("example.com")

    assert result["passed"] is False
    assert "SPF" in result["message"]
    assert "DMARC" in result["message"]
