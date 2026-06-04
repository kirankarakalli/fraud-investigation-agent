from fastapi import FastAPI
from src.fraud_agent.apis.routes import router
import uvicorn

app = FastAPI(title="Banking Fraud Investigation Agent")
app.include_router(router)

@app.get('/')
def welcome():
    return {"message": "Fraud Investigation Agent API is running"}



if __name__=="__main__":
    uvicorn.run(app)