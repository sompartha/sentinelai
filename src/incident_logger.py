import json
from datetime import datetime, timezone
from pathlib import Path

from src.database import SessionLocal
from src.models import Incident


LOG_FILE = Path("incidents.jsonl")


def log_incident(query: str, result: dict):

    timestamp = datetime.now(timezone.utc)

    timeline = result.get("timeline", [])

    record = {
        "timestamp": timestamp.isoformat(),
        "query": query,
        "status": result.get("status", "UNKNOWN"),
        "failure_type": result.get("failure_type", "UNKNOWN"),
        "confidence": result.get("confidence", 0.0),
        "grounded": result.get("grounded", False),
        "risk_level": result.get("risk_level", "UNKNOWN"),
        "recommended_action": result.get(
            "recommended_action",
            "UNKNOWN"
        ),
        "human_escalation": result.get(
            "human_escalation",
            False
        ),
        "explanation": result.get(
            "explanation",
            ""
        ),
        "timeline": timeline
    }

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record) + "\n"
        )

    db = SessionLocal()

    try:

        incident = Incident(
            timestamp=timestamp,
            query=query,
            status=record["status"],
            failure_type=record["failure_type"],
            confidence=record["confidence"],
            grounded=record["grounded"],
            risk_level=record["risk_level"],
            recommended_action=record[
                "recommended_action"
            ],
            human_escalation=record[
                "human_escalation"
            ],
            explanation=record["explanation"],
            timeline=json.dumps(timeline)
        )

        db.add(incident)
        db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()