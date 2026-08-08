import json

import streamlit as st
from sqlalchemy import func

from src.database import Base, SessionLocal, engine
from src.models import Incident


Base.metadata.create_all(bind=engine)


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)


def get_data():

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

        injections = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.failure_type == "PROMPT_INJECTION"
        ).scalar()

        high_risk = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.risk_level == "HIGH"
        ).scalar()

        escalations = db.query(
            func.count(Incident.id)
        ).filter(
            Incident.human_escalation.is_(True)
        ).scalar()

        incidents = db.query(
            Incident
        ).order_by(
            Incident.id.desc()
        ).limit(50).all()

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "blocked": blocked,
            "hallucinations": hallucinations,
            "injections": injections,
            "high_risk": high_risk,
            "escalations": escalations,
            "incidents": incidents
        }

    finally:
        db.close()


data = get_data()


st.title("🛡️ SentinelAI")

st.subheader(
    "AI Reliability & Incident Response Dashboard"
)

st.divider()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Incidents",
    data["total"]
)

col2.metric(
    "Passed",
    data["passed"]
)

col3.metric(
    "Failed",
    data["failed"]
)

col4.metric(
    "Blocked",
    data["blocked"]
)


st.divider()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Hallucinations",
    data["hallucinations"]
)

col2.metric(
    "Prompt Injections",
    data["injections"]
)

col3.metric(
    "High Risk",
    data["high_risk"]
)

col4.metric(
    "Human Escalations",
    data["escalations"]
)


st.divider()


st.subheader("Incident Overview")


chart_data = {
    "PASSED": data["passed"],
    "FAILED": data["failed"],
    "BLOCKED": data["blocked"]
}


st.bar_chart(chart_data)


st.divider()


st.subheader("Agent Execution Timeline")


if data["incidents"]:

    selected_id = st.selectbox(
        "Select an incident",
        [
            incident.id
            for incident in data["incidents"]
        ]
    )

    selected = next(
        incident
        for incident in data["incidents"]
        if incident.id == selected_id
    )

    st.write(
        f"**Query:** {selected.query}"
    )

    st.write(
        f"**Status:** {selected.status}"
    )

    st.write(
        f"**Failure Type:** {selected.failure_type}"
    )

    st.write(
        f"**Risk Level:** {selected.risk_level}"
    )

    st.write(
        f"**Recommended Action:** "
        f"{selected.recommended_action}"
    )

    if selected.timeline:

        try:
            timeline = json.loads(
                selected.timeline
            )
        except Exception:
            timeline = []

        for index, event in enumerate(
            timeline,
            start=1
        ):

            step = event.get(
                "step",
                "Unknown Step"
            )

            status = event.get(
                "status",
                "Unknown"
            )

            st.write(
                f"**{index}. {step}** → `{status}`"
            )

    else:

        st.info(
            "No execution timeline recorded "
            "for this incident."
        )

else:

    st.info(
        "No incidents recorded yet."
    )


st.divider()


st.subheader("Recent Incidents")


if data["incidents"]:

    rows = []

    for incident in data["incidents"]:

        rows.append({
            "ID": incident.id,
            "Timestamp": incident.timestamp,
            "Status": incident.status,
            "Failure Type": incident.failure_type,
            "Risk": incident.risk_level,
            "Action": incident.recommended_action,
            "Confidence": incident.confidence,
            "Human Escalation": (
                incident.human_escalation
            ),
            "Query": incident.query
        })

    st.dataframe(
        rows,
        use_container_width=True
    )

else:

    st.info(
        "No incidents recorded yet."
    )