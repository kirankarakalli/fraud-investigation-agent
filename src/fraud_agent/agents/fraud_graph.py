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


def risk_router(State:FraudState):
    risk_level=State['investigation_result']['risk_level']

    if risk_level=='HIGH':
        return 'escalate'
    elif risk_level=="MEDIUM":
        return 'Review'
    else:
        return 'approve'

def approve_node(state):
    return {"workflow_action": "AUTO_APPROVE"}

def review_node(state):
    return {"workflow_action": "MANUAL_REVIEW"}

def escalate_node(state):
    return {"workflow_action": "ESCALATE_TO_FRAUD_TEAM"}



def llm_report_node(State:FraudState):
    report_input = {
        **State["investigation_result"],
        "workflow_action": State["workflow_action"]
        }
    report=generate_llm_report(report_input)

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

builder.add_node('approve_node',approve_node)
builder.add_node('review_node',review_node)
builder.add_node('escalate_node',escalate_node)




builder.add_edge(START,'prediction_node')
builder.add_edge('prediction_node','investigation_node')
builder.add_conditional_edges('investigation_node',risk_router,{
    'approve':'approve_node',
    'review':'review_node',
    'escalate':'escalate_node'

})
builder.add_edge('approve_node','llm_report_node')
builder.add_edge('review_node','llm_report_node')
builder.add_edge('escalate_node','llm_report_node')

builder.add_edge('llm_report_node',END)

graph = builder.compile()

