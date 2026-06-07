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
    llm_report: str
    audit_logged: bool
    audit_id: int