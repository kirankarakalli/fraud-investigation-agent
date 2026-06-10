from typing import TypedDict

class FraudState(TypedDict):
    transaction: dict
    prediction_result: dict
    investigation_result: dict
    fraud_alerts: list[str]
    workflow_action: str
    requires_human_review: bool
    notification_sent: bool
    llm_report: str
    audit_logged: bool
    audit_id: int
    similar_case_summary: dict