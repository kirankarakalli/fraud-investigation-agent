from langgraph.graph import START,END, StateGraph
from src.fraud_agent.agents.state import FraudState
from src.fraud_agent.services.prediction_service import prediction
from src.fraud_agent.services.investigation_service import investigationReport
from src.fraud_agent.services.llm_report_service import generate_llm_report
from src.fraud_agent.schemas.transaction_schema import TransactionInput
from src.fraud_agent.services.audit_log_service import save_audit_log
from src.fraud_agent.agents.checkpointer import memory
from src.fraud_agent.tools.similar_case_tool import get_similar_cases
from src.fraud_agent.tools.fraud_rules_tool import fraud_rules_check

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
        return 'review'
    else:
        return 'approve'

def approve_node(state):
    return {"workflow_action": "AUTO_APPROVE","requires_human_review": False}

def review_node(state):
    return {"workflow_action": "MANUAL_REVIEW","requires_human_review": True}

def escalate_node(state):
    return {"workflow_action": "PENDING_HUMAN_APPROVAL","requires_human_review": True}

def fraud_rule_node(state):

    alerts = fraud_rules_check(
        Amount=state["prediction_result"]["Amount"],
        risk_level=state["prediction_result"]["risk_level"]
    )

    return {
        "fraud_alerts": alerts
    }

def similar_case_node(state):
    risk_level = state["investigation_result"]["risk_level"]

    result = get_similar_cases(risk_level)

    return {
        "similar_case_summary": result
    }

def llm_report_node(State:FraudState):
    report_input = {
        **State["investigation_result"],
        "fraud_alerts": State["fraud_alerts"],
        "similar_case_summary": State.get("similar_case_summary", {}),
        "workflow_action": State["workflow_action"],
         "requires_human_review": State["requires_human_review"]
        }
    report=generate_llm_report(report_input)

    return {
        "llm_report": report
    }

def audit_log_node(State:FraudState):
    llm_result = {
        **State["investigation_result"],
        "workflow_action": State["workflow_action"]
        }

    audit_id=save_audit_log(llm_result)

    return {
        "audit_logged": True,
        "audit_id":audit_id
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
builder.add_node('audit_log_node',audit_log_node)
builder.add_node('fraud_rule_node',fraud_rule_node)
builder.add_node("similar_case_node", similar_case_node)



builder.add_edge(START,'prediction_node')
builder.add_edge('prediction_node','investigation_node')
builder.add_edge('investigation_node','fraud_rule_node')

builder.add_conditional_edges('fraud_rule_node',risk_router,{
    'approve':'approve_node',
    'review':'review_node',
    'escalate':'escalate_node'

})
builder.add_edge('approve_node','llm_report_node')
builder.add_edge('review_node','llm_report_node')
builder.add_edge(
    "escalate_node",
    "similar_case_node"
)

builder.add_edge(
    "similar_case_node",
    "llm_report_node"
)
builder.add_edge('llm_report_node','audit_log_node')
builder.add_edge('audit_log_node',END)

graph = builder.compile(checkpointer=memory)

