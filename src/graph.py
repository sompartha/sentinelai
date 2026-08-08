from typing import TypedDict, List, Any

from langgraph.graph import StateGraph, END

from src.agents import (
    detect_prompt_injection,
    diagnose_failure,
    determine_remediation
)


class SentinelState(TypedDict):
    query: str
    answer: str
    context: List[str]

    injection_result: dict
    diagnosis: dict
    remediation: dict

    status: str
    failure_type: str
    confidence: float
    grounded: bool
    risk_level: str
    recommended_action: str
    human_escalation: bool
    explanation: str

    timeline: List[Any]


def build_graph():

    def safety_node(state):

        timeline = state.get(
            "timeline",
            []
        )

        timeline.append({
            "step": "Input Safety Agent",
            "status": "Running"
        })

        result = detect_prompt_injection(
            state["query"]
        )

        timeline.append({
            "step": "Input Safety Agent",
            "status": "Completed"
        })

        return {
            "injection_result": result,
            "timeline": timeline
        }


    def safety_router(state):

        result = state["injection_result"]

        if result.get(
            "is_injection",
            False
        ):
            return "block"

        return "diagnose"


    def block_node(state):

        result = state["injection_result"]

        confidence = float(
            result.get(
                "confidence",
                0.0
            )
        )

        timeline = state.get(
            "timeline",
            []
        )

        timeline.append({
            "step": "Security Decision",
            "status": "BLOCKED"
        })

        return {
            "status": "BLOCKED",
            "failure_type": "PROMPT_INJECTION",
            "confidence": confidence,
            "grounded": False,
            "risk_level": result.get(
                "risk_level",
                "HIGH"
            ),
            "recommended_action": "BLOCK_REQUEST",
            "human_escalation": True,
            "explanation": result.get(
                "explanation",
                "Prompt injection detected."
            ),
            "timeline": timeline
        }


    def diagnosis_node(state):

        timeline = state.get(
            "timeline",
            []
        )

        timeline.append({
            "step": "Failure Diagnosis",
            "status": "Running"
        })

        diagnosis = diagnose_failure(
            state["query"],
            state["answer"],
            state["context"]
        )

        timeline.append({
            "step": "Failure Diagnosis",
            "status": "Completed"
        })

        return {
            "diagnosis": diagnosis,
            "timeline": timeline
        }


    def remediation_node(state):

        diagnosis = state["diagnosis"]

        failure_type = diagnosis.get(
            "failure_type",
            "MODEL_FAILURE"
        )

        risk_level = diagnosis.get(
            "risk_level",
            "HIGH"
        )

        confidence = float(
            diagnosis.get(
                "confidence",
                0.0
            )
        )

        remediation = determine_remediation(
            failure_type,
            risk_level,
            confidence
        )

        timeline = state.get(
            "timeline",
            []
        )

        timeline.append({
            "step": "Automated Remediation",
            "status": remediation[
                "recommended_action"
            ]
        })

        return {
            "remediation": remediation,
            "timeline": timeline
        }


    def decision_node(state):

        diagnosis = state["diagnosis"]
        remediation = state["remediation"]

        timeline = state.get(
            "timeline",
            []
        )

        timeline.append({
            "step": "Reliability Decision",
            "status": diagnosis.get(
                "status",
                "FAILED"
            )
        })

        return {
            "status": diagnosis.get(
                "status",
                "FAILED"
            ),

            "failure_type": diagnosis.get(
                "failure_type",
                "MODEL_FAILURE"
            ),

            "confidence": float(
                diagnosis.get(
                    "confidence",
                    0.0
                )
            ),

            "grounded": bool(
                diagnosis.get(
                    "grounded",
                    False
                )
            ),

            "risk_level": diagnosis.get(
                "risk_level",
                "HIGH"
            ),

            "recommended_action": remediation.get(
                "recommended_action",
                "HUMAN_ESCALATION"
            ),

            "human_escalation": bool(
                remediation.get(
                    "human_escalation",
                    True
                )
            ),

            "explanation": diagnosis.get(
                "explanation",
                ""
            ),

            "timeline": timeline
        }


    workflow = StateGraph(
        SentinelState
    )


    workflow.add_node(
        "safety",
        safety_node
    )

    workflow.add_node(
        "block",
        block_node
    )

    workflow.add_node(
        "diagnosis",
        diagnosis_node
    )

    workflow.add_node(
        "remediation",
        remediation_node
    )

    workflow.add_node(
        "decision",
        decision_node
    )


    workflow.set_entry_point(
        "safety"
    )


    workflow.add_conditional_edges(
        "safety",
        safety_router,
        {
            "block": "block",
            "diagnose": "diagnosis"
        }
    )


    workflow.add_edge(
        "block",
        END
    )

    workflow.add_edge(
        "diagnosis",
        "remediation"
    )

    workflow.add_edge(
        "remediation",
        "decision"
    )

    workflow.add_edge(
        "decision",
        END
    )


    return workflow.compile()