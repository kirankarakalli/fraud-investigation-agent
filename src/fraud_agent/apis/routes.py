from fastapi import APIRouter
from src.fraud_agent.schemas import prediction_schema
from src.fraud_agent.schemas.investigation_schema import InvestigationResponse
from src.fraud_agent.schemas.prediction_schema import PredictionResponse
from src.fraud_agent.schemas.transaction_schema import TransactionInput
from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.services.investigation_service import investigationReport


router=APIRouter()

@router.post('/predict',response_model=PredictionResponse)
def predict(transaction:TransactionInput):
    return prediction(transaction)


@router.post('/investigate',response_model=InvestigationResponse)
def investigate(transaction:TransactionInput):
    return investigationReport(transaction)






