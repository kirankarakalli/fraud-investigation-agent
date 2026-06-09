from pydantic import BaseModel


class AgentInvestigationResponse(BaseModel):
    Amount: float
    Time: float
    prediction: int
    fraud_probability: float
    risk_level: str
    risk_reason: list[str]
    investigation_summary: str
    recommended_action: str
    workflow_action: str
    requires_human_review: bool
    llm_report: str
    audit_logged: bool
    audit_id: int
    fraud_alerts: list[str]
    similar_case_summary: dict
    