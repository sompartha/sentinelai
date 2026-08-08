from sqlalchemy import func

from src.database import SessionLocal
from src.models import Incident


def get_metrics():

    db = SessionLocal()

    try:
        total = db.query(
            func.count(Incident.id)
        ).scalar()

        passed = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.status == "PASSED"
        ).scalar()

        failed = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.status == "FAILED"
        ).scalar()

        blocked = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.status == "BLOCKED"
        ).scalar()

        hallucinations = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.failure_type == "HALLUCINATION"
        ).scalar()

        prompt_injections = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.failure_type == "PROMPT_INJECTION"
        ).scalar()

        high_risk = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.risk_level == "HIGH"
        ).scalar()

        human_escalations = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.human_escalation == True
        ).scalar()

        return {
            "total_incidents": total,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "hallucinations": hallucinations,
            "prompt_injections": prompt_injections,
            "high_risk_incidents": high_risk,
            "human_escalations": human_escalations
        }

    finally:
        db.close()