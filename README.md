# SentinelAI

## Autonomous Multi-Agent AI Reliability & Incident Response Platform

SentinelAI is an AI reliability platform designed to evaluate LLM-generated responses, identify failure causes, recommend remediation actions, and record incidents for monitoring and analysis.

Unlike a system that only checks whether an answer is correct, SentinelAI attempts to determine **why an AI response failed** and routes the failure through an appropriate response workflow.

## Key Capabilities

- Prompt injection detection
- LLM response groundedness evaluation
- Hallucination detection
- Insufficient-context detection
- Retrieval failure analysis
- Automated remediation decisions
- Human escalation for high-risk incidents
- Agent execution timeline
- SQLite-based incident persistence
- JSONL audit logging
- Reliability metrics API
- Streamlit monitoring dashboard
- FastAPI REST API
- LangGraph-based agent workflow

## Architecture

```text
                         User Request
                              |
                              v
                    +-------------------+
                    | Input Safety Agent|
                    +-------------------+
                              |
                     Prompt Injection?
                       /           \
                     Yes            No
                      |              |
                      v              v
                   BLOCK       Failure Diagnosis
                                      |
                                      v
                              +---------------+
                              | Diagnosis     |
                              | Agent         |
                              +---------------+
                                      |
                                      v
                              +---------------+
                              | Remediation   |
                              | Decision      |
                              +---------------+
                                      |
                     +----------------+----------------+
                     |                |                |
                     v                v                v
                 ALLOW          REGENERATE      HUMAN ESCALATION
                     |
                     v
              Incident Logging
                     |
             +-------+-------+
             |               |
             v               v
        SQLite Database   incidents.jsonl
             |
             v
       Metrics API
             |
             v
      Streamlit Dashboard

      # SentinelAI

Autonomous Multi-Agent AI Reliability and Incident Response Platform.

## 🚀 Live Demo

[**Open SentinelAI Live Demo**](https://sentinelai-2nnagmc2fyphihtszt4ga4.streamlit.app/)

## 📂 GitHub Repository

[**View Source Code**](https://github.com/sompartha/sentinelai)