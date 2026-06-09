from src.fraud_agent.database.database import SessionLocal
from src.fraud_agent.services.audit_log_service import AuditLog


def get_similar_cases(risk_level:str):
  
    db=SessionLocal()
    try:

        similar_cases=db.query(AuditLog).filter(AuditLog.risk_level==risk_level).all()
        rejected_cases = [
            case for case in similar_cases
            if case.approval_status == "REJECTED"
            ]

        pending_cases = [
            case for case in similar_cases
            if case.approval_status == "PENDING"
            ]

        return {
            "risk_level": risk_level,
            "similar_cases_count": len(similar_cases),
            "rejected_cases_count": len(rejected_cases),
            "pending_cases_count": len(pending_cases)
            }

    finally:
        db.close()