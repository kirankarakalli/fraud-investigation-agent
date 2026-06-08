import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect(
    "fraud_memory.db",
    check_same_thread=False
)

memory = SqliteSaver(conn)