from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker,declarative_base
from pathlib import Path

DB_PATH=Path('fraud_agent.db')

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine=create_engine(DATABASE_URL,connect_args={'check_same_thread':False})
SessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()
