from ast import mod
import os
from dotenv import load_dotenv
from langchain_core.outputs import llm_result
from langchain_openai import ChatOpenAI
from src.fraud_agent.prompts.fraud_report_prompt import prompt


load_dotenv(override=True)

llm=ChatOpenAI(model='gpt-4o', temperature=0.4)



chain=prompt| llm


def generate_llm_report(investigation_data: dict) -> str:
    investigation_data["fraud_probability"] = round(investigation_data["fraud_probability"] * 100,2)
    response = chain.invoke(investigation_data)
    return response.content