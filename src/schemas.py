from pydantic import BaseModel, Field
from typing import List, Optional


class SentinelRequest(BaseModel):
    query: str
    answer: str
    context: List[str] = Field(default_factory=list)


class SentinelDecision(BaseModel):
    status: str
    failure_type: str
    confidence: float
    grounded: bool
    risk_level: str
    recommended_action: str
    human_escalation: bool
    explanation: str


class IncidentRecord(BaseModel):
    query: str
    failure_type: str
    risk_level: str
    recommended_action: str
    confidence: float
    human_escalation: bool
    explanation: str
    status: str