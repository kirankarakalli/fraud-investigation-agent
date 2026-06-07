from sqlalchemy import Column,Integer,Float,String,DateTime, null
from datetime import datetime,timezone
from src.fraud_agent.database.database import Base

class AuditLog(Base):
    __tablename__='audit_logs'

    id=Column(Integer,primary_key=True,index=True)
    timestamp=Column(DateTime, default=lambda: datetime.now(timezone.utc))
    amount = Column(Float)
    time = Column(Float)
    prediction = Column(Integer)
    fraud_probability = Column(Float)
    risk_level = Column(String)
    workflow_action = Column(String)
    approval_status=Column(String,default="Not Required")
    reviewed_by=Column(String,nullable=True)
    review_notes=Column(String,nullable=True)
    reviewed_at= Column(DateTime,nullable=True)

