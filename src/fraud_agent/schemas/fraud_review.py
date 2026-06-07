from datetime import datetime, timezone
from src.fraud_agent.database.audit_model import AuditLog
from src.fraud_agent.database.database import SessionLocal
from src.fraud_agent.schemas.HumanRequest_schema import HumanReviewRequest

def review_case(audit_id, review_data:HumanReviewRequest):
    db=SessionLocal()

    try:
        audit_log = db.query(AuditLog).filter(
            AuditLog.id == audit_id
        ).first()

        if not audit_log:
            return {
                "message": "Audit log not found"
            }
        
        audit_log.approval_status=review_data.decision
        audit_log.reviewed_by=review_data.reviewed_by
        audit_log.review_notes=review_data.review_notes
        audit_log.reviewed_at = datetime.now(timezone.utc)

    finally:
        db.close()
