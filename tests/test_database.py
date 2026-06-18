import os

import pytest
from sqlmodel import SQLModel, create_engine

from sitelens.web import database


@pytest.fixture(autouse=True)
def use_temporary_database(monkeypatch, tmp_path):
    """Each test gets a fresh, temporary database file instead of the real one."""
    test_db_path = tmp_path / "test_sitelens.db"
    test_engine = create_engine(f"sqlite:///{test_db_path}")
    monkeypatch.setattr(database, "engine", test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield


def _fake_report(domain: str = "example.com") -> dict:
    return {
        "domain": domain,
        "scanned_at": "2026-01-01T00:00:00+00:00",
        "results": [],
        "summary": {
            "total": 4,
            "passed": 3,
            "failed": 1,
            "highest_severity": "medium",
        },
    }


def test_save_scan_stores_record():
    record = database.save_scan(_fake_report())

    assert record.id is not None
    assert record.domain == "example.com"
    assert record.total_checks == 4
    assert record.passed_checks == 3


def test_get_recent_scans_returns_newest_first():
    database.save_scan(_fake_report(domain="first.com"))
    database.save_scan(_fake_report(domain="second.com"))

    results = database.get_recent_scans()

    assert len(results) == 2
    assert results[0].domain == "second.com"  # yang paling baru muncul pertama
