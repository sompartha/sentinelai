from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text
)

from datetime import datetime, timezone

from src.database import Base


class Incident(Base):

    __tablename__ = "incidents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    query = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False
    )

    failure_type = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    grounded = Column(
        Boolean,
        nullable=False
    )

    risk_level = Column(
        String(50),
        nullable=False
    )

    recommended_action = Column(
        String(100),
        nullable=False
    )

    human_escalation = Column(
        Boolean,
        nullable=False
    )

    explanation = Column(
        Text,
        nullable=False
    )

    timeline = Column(
        Text,
        nullable=True
    )