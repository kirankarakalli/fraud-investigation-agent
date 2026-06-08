# Fraud Investigation Agent

An end-to-end AI-powered Fraud Investigation Agent built using FastAPI, Machine Learning, LangChain, LangGraph, and SQLite.

## Features

* Fraud Prediction using Machine Learning
* Risk Classification (LOW, MEDIUM, HIGH)
* AI-generated Investigation Reports using LLMs
* LangGraph-based Investigation Workflow
* Conditional Routing based on Risk Level
* Audit Logging with SQLite
* Human-in-the-Loop Review Process
* Fraud Case Management APIs
* Investigation Analytics and Statistics

---

## Tech Stack

### Backend

* FastAPI
* Python

### Machine Learning

* Scikit-learn
* Joblib
* Pandas

### LLM & Agent Framework

* LangChain
* LangGraph

### Database

* SQLite
* SQLAlchemy

---

## Workflow

Transaction
↓
Fraud Prediction
↓
Investigation Analysis
↓
Risk Routing

LOW → Auto Approve

MEDIUM → Manual Review

HIGH → Human Approval Required

↓
LLM Investigation Report
↓
Audit Logging
↓
Case Management

---

## LangGraph Workflow

![Fraud Workflow](fraud_graph.png)

---

## API Endpoints

### Fraud Investigation

POST /agent/investigate

Analyze a transaction and generate:

* Fraud prediction
* Risk assessment
* Investigation summary
* LLM-generated report

---

### Human Review

POST /cases/{audit_id}/review

Approve or reject high-risk fraud cases.

---

### Case Management

GET /cases

Retrieve all fraud investigation cases.

GET /cases/{audit_id}

Retrieve a specific case.

GET /cases?status=PENDING

Filter cases by status.

---

### Analytics

GET /cases/stats

Returns:

* Total Cases
* Pending Cases
* Approved Cases
* Rejected Cases
* High Risk Cases
* Medium Risk Cases
* Low Risk Cases

---

## Example Investigation Response

```json
{
  "prediction": 1,
  "fraud_probability": 0.7326,
  "risk_level": "HIGH",
  "workflow_action": "PENDING_HUMAN_APPROVAL",
  "requires_human_review": true
}
```

## Future Enhancements

* LangGraph Checkpointing
* Agent Memory
* Tool Calling
* Notification System
* Dashboard UI
* Multi-Agent Fraud Investigation Workflow

## Author

Kiran Karakalli
