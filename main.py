from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnableLambda

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

SYSTEM_PROMPT = """
You are a trading strategy generator assistant. Based on the user query, generate a clear buy and sell strategy using technical indicators like RSI, VWAP, MACD, etc. Output in plain English in steps.
"""

USER_EXAMPLE = """
User: Can you build a strategy using VWAP and RSI for buying and selling stocks?

Response:
Buy Strategy:
1. Wait for price to cross above VWAP.
2. RSI should be below 30 and start rising.

Sell Strategy:
1. Price crosses below VWAP.
2. RSI is above 70 and starts to decline.
"""


# # Define state: {'input': ..., 'strategy': ...}
# def generate_strategy(state):
#     user_query = state['input']
#     prompt = f"{SYSTEM_PROMPT}\nUser: {user_query}"
#     result = llm.invoke(prompt)
#     return {'input': user_query, 'strategy': result.content}

# # Wrap in LangGraph
# builder = StateGraph()
# builder.add_node("strategy_generator", RunnableLambda(generate_strategy))
# builder.set_entry_point("strategy_generator")
# builder.add_edge("strategy_generator", END)

# graph = builder.compile()


# output = graph.invoke({"input": "Can you build a strategy using VWAP and RSI for buying and selling stocks?"})
# print(output['strategy'])

from langgraph.graph import StateGraph, END
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnableLambda
from typing import TypedDict

# Define state
class StrategyState(TypedDict):
    input: str
    strategy: str

# LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

# Node logic
def generate_strategy(state: StrategyState) -> StrategyState:
    user_query = state['input']
    prompt = f"Build a trading strategy based on: {user_query}"
    result = llm.invoke(prompt)
    return {"input": user_query, "strategy": result.content}

# Build the LangGraph
builder = StateGraph(StrategyState)
builder.add_node("generate_strategy", RunnableLambda(generate_strategy))
builder.set_entry_point("generate_strategy")
builder.add_edge("generate_strategy", END)

graph = builder.compile()

# Run it
result = graph.invoke({"input": "Build a VWAP + RSI buy/sell strategy"})
print(result)
