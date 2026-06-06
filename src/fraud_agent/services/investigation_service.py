from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.schemas.transaction_schema import TransactionInput
from src.fraud_agent.services.llm_report_service import generate_llm_report

def investigationReport(transaction:TransactionInput):

    predict=prediction(transaction)
    probability=predict['fraud_probability']

    if probability > 0.7:
        report={
            "risk_reason": [
                        "High fraud probability detected",
                        "Transaction requires immediate fraud team escalation"
                          ],
            "investigation_summary": "High fraud probability detected.",
            "recommended_action": "Transaction requires immediate review."
        }

    elif probability > 0.3:
        report= {
           "risk_reason": [
                            "Moderate fraud probability detected",
                            "Transaction should be manually reviewed by the fraud team"
                          ],
            "investigation_summary": "Some suspicious patterns detected.",
            "recommended_action": "Manual verification recommended."
        }

    else:
        report= {
            "risk_reason": [
                            "Low fraud probability detected",
                            "No immediate fraud indicators found"
                            ],
            "investigation_summary": "No significant fraud indicators detected.",
            "recommended_action": "Approve transaction."
        }
    
    result= {
        **predict,
        **report
    }

    llm_report=generate_llm_report(result)

    return {
        **result,
        "llm_report":llm_report
    }






