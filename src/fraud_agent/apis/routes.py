from fastapi import APIRouter
from src.fraud_agent.database.audit_model import AuditLog
from src.fraud_agent.schemas import prediction_schema
from src.fraud_agent.schemas.HumanRequest_schema import HumanReviewRequest
from src.fraud_agent.schemas.fraud_review import review_case
from src.fraud_agent.schemas.investigation_schema import InvestigationResponse
from src.fraud_agent.schemas.prediction_schema import PredictionResponse
from src.fraud_agent.schemas.transaction_schema import TransactionInput
from src.fraud_agent.schemas.AgentInvestigationResponse import AgentInvestigationResponse
from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.services.investigation_service import investigationReport
from src.fraud_agent.agents.fraud_graph import graph
from src.fraud_agent.database.database import SessionLocal


router=APIRouter()

@router.get("/cases")
def get_all_cases():
    db = SessionLocal()

    try:
        logs = db.query(AuditLog).all()

        return {
            "count": len(logs),
            "cases": [
            {
            "id": log.id,
            "approval_status": log.approval_status,
            "risk_level": log.risk_level,
            "workflow_action": log.workflow_action,
            "amount": log.amount,
            "prediction": log.prediction,
            "fraud_probability": log.fraud_probability,
            "reviewed_by": log.reviewed_by,
            "review_notes": log.review_notes,
            "timestamp": str(log.timestamp),
            "reviewed_at": str(log.reviewed_at) if log.reviewed_at else None
            }
            for log in logs
            ]
        }

    finally:
        db.close()


@router.post('/predict',response_model=PredictionResponse)
def predict(transaction:TransactionInput):
    return prediction(transaction)


@router.post('/investigate',response_model=InvestigationResponse)
def investigate(transaction:TransactionInput):
    return investigationReport(transaction)

@router.post('/agent/investigate',response_model=AgentInvestigationResponse)
def agent_investigate(transaction:TransactionInput):
    result = graph.invoke({
        "transaction": transaction.model_dump()
    })

    return {
        **result["investigation_result"],
        "workflow_action": result["workflow_action"],
        "requires_human_review": result["requires_human_review"],
        "llm_report": result["llm_report"],
        "audit_logged": result["audit_logged"],
        "audit_id": result["audit_id"]
        
    }

@router.post("/cases/{audit_id}/review")
def review_fraud_case(audit_id: int, review: HumanReviewRequest):
    return review_case(audit_id, review)





