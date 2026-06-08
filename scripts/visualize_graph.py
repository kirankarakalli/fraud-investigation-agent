from src.fraud_agent.agents.fraud_graph import graph

png_data = graph.get_graph().draw_mermaid_png()

with open("fraud_graph.png", "wb") as f:
    f.write(png_data)

print("Graph saved as fraud_graph.png")