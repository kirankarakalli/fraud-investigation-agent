from pydantic import BaseModel

class PredictionResponse(BaseModel):
    Amount: float
    Time: float
    prediction: int
    fraud_probability: float
    risk_level: str