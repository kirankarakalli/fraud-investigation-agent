from src.fraud_agent.schemas.transaction_schema import TransactionInput
import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "fraud_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def prediction(transaction:TransactionInput):

    data = transaction.model_dump()
    
    df=pd.DataFrame([data])

    df[['Amount','Time']]=scaler.transform(df[['Amount','Time']])

    prediction=model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    if probability > 0.7:
        risk_level = "HIGH"
    elif probability > 0.3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
    "prediction": int(prediction),
    "fraud_probability": float(probability),
    "risk_level": risk_level,

    }





    