

def fraud_rules_check(Amount:float,risk_level:str):
    alerts=[]

    if Amount>1000:
        alerts.append("High transaction amount")

    if risk_level=='HIGH':
        alerts.append("High ML fraud risk")

    if Amount==0:
        alerts.append('Zero amount transaction detected')

    return alerts







