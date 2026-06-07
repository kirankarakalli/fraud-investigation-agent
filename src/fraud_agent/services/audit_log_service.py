from datetime import datetime,timezone
import json
from pathlib import Path

LOG_PATH=Path('logs/fraud_audit_logs.jsonl')
LOG_PATH.parent.mkdir(exist_ok=True)


def save_audit_log(result:dict):
    log_enrty={
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "amount": result.get("Amount"),
        "time": result.get("Time"),
        "prediction": result.get("prediction"),
        "fraud_probability": result.get("fraud_probability"),
        "risk_level": result.get("risk_level"),
        "workflow_action": result.get("workflow_action")
    }

    with open(LOG_PATH,'a') as file:
        file.write(json.dumps(log_enrty)+'\n')

