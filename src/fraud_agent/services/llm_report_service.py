from ast import mod
import os
from dotenv import load_dotenv
from langchain_core.outputs import llm_result
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(override=True)

llm=ChatOpenAI(model='gpt-4o', temperature=0.4)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a professional banking fraud investigation analyst.

Generate a concise fraud investigation report.
Do not use markdown.
Do not use **.
Use plain text only.
Display probabilities as percentages.
Do not use scientific notation.
"""
    ),
    (
        "human",
        """
Transaction Details:
Amount: {Amount}
Time: {Time}

Prediction: {prediction}
Fraud Probability: {fraud_probability}
Risk Level: {risk_level}
Risk Reasons: {risk_reason}
Investigation Summary: {investigation_summary}
Recommended Action: {recommended_action}

Format:
1. Executive Summary
2. Risk Assessment
3. Key Reasons
4. Recommended Action
"""
    )
])

chain= prompt| llm


def generate_llm_report(investigation_data: dict) -> str:
    response = chain.invoke(investigation_data)
    return response.content