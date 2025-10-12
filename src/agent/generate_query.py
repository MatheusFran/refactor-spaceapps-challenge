from langgraph.graph import MessagesState

from src.agent.tool import retriever_tool


def generate_query(state: MessagesState, response_model):
    response = (
        response_model
        .bind_tools([retriever_tool]).invoke(state["messages"])
    )
    return {"messages": [response]}
