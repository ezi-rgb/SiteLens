import json
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

DATABASE_URL = "sqlite:///sitelens.db"
engine = create_engine(DATABASE_URL)


class ScanRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    domain: str
    scanned_at: str
    total_checks: int
    passed_checks: int
    highest_severity: str
    report_json: str  # menyimpan seluruh report sebagai JSON string

    def to_report_dict(self) -> dict:
        """Reconstructs the full report dict from the stored JSON."""
        return json.loads(self.report_json)


def init_db() -> None:
    """Creates the database tables if they don't already exist."""
    SQLModel.metadata.create_all(engine)


def save_scan(report: dict) -> ScanRecord:
    """Saves a scan report to the database."""
    record = ScanRecord(
        domain=report["domain"],
        scanned_at=report["scanned_at"],
        total_checks=report["summary"]["total"],
        passed_checks=report["summary"]["passed"],
        highest_severity=report["summary"]["highest_severity"],
        report_json=json.dumps(report),
    )

    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)

    return record


def get_recent_scans(limit: int = 10) -> list[ScanRecord]:
    """Returns the most recent scans, newest first."""
    with Session(engine) as session:
        statement = (
            select(ScanRecord)
            .order_by(ScanRecord.id.desc())
            .limit(limit)
        )
        return list(session.exec(statement))
