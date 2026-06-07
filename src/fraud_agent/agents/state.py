from typing import TypedDict

class FraudState(TypedDict):
    transaction: dict
    prediction_result: dict
    investigation_result: dict
    workflow_action: str
    llm_report: str