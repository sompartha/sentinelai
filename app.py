from fastapi import FastAPI, HTTPException

from src.graph import build_graph
from src.schemas import (
    SentinelRequest,
    SentinelDecision
)
from src.incident_logger import log_incident
from src.metrics import get_metrics


app = FastAPI(
    title="SentinelAI",
    description=(
        "Autonomous Multi-Agent AI Reliability "
        "and Incident Response Platform"
    ),
    version="1.0.0"
)


workflow = build_graph()


@app.get("/")
def health_check():

    return {
        "service": "SentinelAI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/metrics")
def metrics():

    return get_metrics()


@app.post(
    "/evaluate",
    response_model=SentinelDecision
)
def evaluate(
    request: SentinelRequest
):

    try:

        initial_state = {
            "query": request.query,
            "answer": request.answer,
            "context": request.context,

            "injection_result": {},
            "diagnosis": {},
            "remediation": {},

            "status": "",
            "failure_type": "",
            "confidence": 0.0,
            "grounded": False,
            "risk_level": "",
            "recommended_action": "",
            "human_escalation": False,
            "explanation": "",

            "timeline": []
        }

        result = workflow.invoke(
            initial_state
        )

        log_incident(
            request.query,
            result
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )