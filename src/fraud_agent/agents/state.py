from typing import TypedDict

class FraudState(TypedDict):
    transaction: dict
    prediction_result: dict
    investigation_result: dict
    workflow_action: str
    requires_human_review: bool
    llm_report: str
    audit_logged: bool
    audit_id: int