import uu
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
from uuid import uuid4

router=APIRouter(tags=["Banking Fraud API EndPoints"])

@router.get("/cases")
def get_all_cases(status: str | None = None):
    db = SessionLocal()

    try:
        query = db.query(AuditLog)
        if status:
            query = query.filter(
                AuditLog.approval_status == status.upper()
            )

        logs = query.all()

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

@router.get('/cases/stats')
def get_case_stats():
    db = SessionLocal()

    try:
        total_cases = db.query(AuditLog).count()

        pending_cases = db.query(AuditLog).filter(
            AuditLog.approval_status == 'PENDING'
        ).count()

        approved_cases = db.query(AuditLog).filter(
            AuditLog.approval_status == 'APPROVED'
        ).count()

        rejected_cases = db.query(AuditLog).filter(
            AuditLog.approval_status == 'REJECTED'
        ).count()

        high_risk_cases = db.query(AuditLog).filter(
            AuditLog.risk_level == 'HIGH'
        ).count()

        medium_risk_cases = db.query(AuditLog).filter(
            AuditLog.risk_level == 'MEDIUM'
        ).count()

        low_risk_cases = db.query(AuditLog).filter(
            AuditLog.risk_level == 'LOW'
        ).count()

        return {
            'total_cases': total_cases,
            'pending_cases': pending_cases,
            'approved_cases': approved_cases,
            'rejected_cases': rejected_cases,
            'high_risk_cases': high_risk_cases,
            'medium_risk_cases': medium_risk_cases,
            'low_risk_cases': low_risk_cases
        }

    finally:
        db.close()


@router.get("/cases/{audit_id}")
def get_all_case_by_id(audit_id:int):
    db = SessionLocal()

    try:
        log = db.query(AuditLog).filter(AuditLog.id==audit_id).first()

        if not log:
            return {"message": "Case not found"}

        return {
            "id": log.id,
            "timestamp": str(log.timestamp),
            "amount": log.amount,
            "time": log.time,
            "prediction": log.prediction,
            "fraud_probability": log.fraud_probability,
            "risk_level": log.risk_level,
            "workflow_action": log.workflow_action,
            "approval_status": log.approval_status,
            "reviewed_by": log.reviewed_by,
            "review_notes": log.review_notes,
            "reviewed_at": str(log.reviewed_at) if log.reviewed_at else None
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
    config = {
    "configurable": {
        "thread_id": str(uuid4())
    }
}
    result = graph.invoke({
        "transaction": transaction.model_dump()},
        config=config
    )
    return {
        **result["investigation_result"],
        "workflow_action": result["workflow_action"],
        "requires_human_review": result["requires_human_review"],
        "fraud_alerts": result["fraud_alerts"],
        "similar_case_summary": result.get("similar_case_summary", {}),
        "notification_sent": result.get("notification_sent", False),
        "llm_report": result["llm_report"],
        "audit_logged": result["audit_logged"],
        "audit_id": result["audit_id"]
        
    }

@router.post("/cases/{audit_id}/review")
def review_fraud_case(audit_id: int, review: HumanReviewRequest):
    return review_case(audit_id, review)





