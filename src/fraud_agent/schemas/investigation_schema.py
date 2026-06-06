from pydantic import BaseModel
from typing import List

class InvestigationResponse(BaseModel):
    Amount: float
    Time: float
    prediction: int
    fraud_probability: float
    risk_level: str
    risk_reason: List[str]
    investigation_summary: str
    recommended_action: str
    llm_report: str
