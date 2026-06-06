from fastapi import APIRouter
from src.fraud_agent.schemas.transaction_schema import TransactionInput
from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.services.investigation_service import investigationReport


router=APIRouter()

@router.post('/predict')
def predict(transaction:TransactionInput):
    return prediction(transaction)


@router.post('/investigate')
def investigate(transaction:TransactionInput):
    return investigationReport(transaction)






