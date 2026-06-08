from src.fraud_agent.database.database import SessionLocal,engine,Base
from src.fraud_agent.database.audit_model import AuditLog

Base.metadata.create_all(bind=engine)

def save_audit_log(result: dict):
    db = SessionLocal()

    try:
        if result.get("workflow_action") == "PENDING_HUMAN_APPROVAL":
            approval_status = "PENDING"
        else:
            approval_status = "NOT_REQUIRED"
        audit_log = AuditLog(
            amount=result.get("Amount"),
            time=result.get("Time"),
            prediction=result.get("prediction"),
            fraud_probability=result.get("fraud_probability"),
            risk_level=result.get("risk_level"),
            workflow_action=result.get("workflow_action"),
            approval_status=approval_status
        )

        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        count = db.query(AuditLog).count()

        print("Saved Audit ID:", audit_log.id)
        print("Total Audit Rows:", count)

        return audit_log.id

    finally:
        db.close()