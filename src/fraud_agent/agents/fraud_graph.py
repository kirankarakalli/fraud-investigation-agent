from sre_parse import State
from langgraph.graph import START,END, StateGraph
from src.fraud_agent.agents.state import FraudState
from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.services.investigation_service import investigationReport
from src.fraud_agent.services.llm_report_service import generate_llm_report
from src.fraud_agent.schemas.transaction_schema import TransactionInput


def prediction_node(State:FraudState):
    transaction_obj = TransactionInput(**State["transaction"])
    result=prediction(transaction_obj)

    return {
        "prediction_result": result
    }


def investigation_node(State:FraudState):
    transaction_obj = TransactionInput(**State["transaction"])
    result=investigationReport(transaction_obj)

    return {
        "investigation_result": result
    }


def llm_report_node(State:FraudState):

    report=generate_llm_report(State['investigation_result'])

    return {
        "llm_report": report
    }


builder=StateGraph(FraudState)


builder.add_node(
    'prediction_node',prediction_node
)

builder.add_node(
    'investigation_node' ,investigation_node
)

builder.add_node(
    'llm_report_node',llm_report_node
)


builder.add_edge(START,'prediction_node')
builder.add_edge('prediction_node','investigation_node')
builder.add_edge('investigation_node','llm_report_node')
builder.add_edge('llm_report_node',END)

graph = builder.compile()

