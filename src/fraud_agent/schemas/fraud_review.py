from datetime import datetime, timezone
from src.fraud_agent.database.audit_model import AuditLog
from src.fraud_agent.database.database import SessionLocal
from src.fraud_agent.schemas.HumanRequest_schema import HumanReviewRequest


def review_case(audit_id: int, review_data: HumanReviewRequest):
    db = SessionLocal()

    try:
        audit_log = db.query(AuditLog).filter(
            AuditLog.id == audit_id
        ).first()

        if not audit_log:
            return {"message": "Audit log not found"}

        audit_log.approval_status = review_data.decision.upper()
        audit_log.reviewed_by = review_data.reviewed_by
        audit_log.review_notes = review_data.review_notes
        audit_log.reviewed_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(audit_log)

        return {
            "audit_id": audit_log.id,
            "approval_status": audit_log.approval_status,
            "reviewed_by": audit_log.reviewed_by,
            "review_notes": audit_log.review_notes,
            "reviewed_at": str(audit_log.reviewed_at),
            "message": "Human review completed"
        }

    finally:
        db.close()
