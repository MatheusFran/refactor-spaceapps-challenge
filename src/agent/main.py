from typing import Literal
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.tools.retriever import create_retriever_tool

from src.agent.generate_query import generate_query as custom_generate_query
from src.agent.models import init_chat_model, response_model  # Supondo que você tenha init_chat_model e response_model

# -------------------------
# Configuration / Prompts
# -------------------------

GRADE_PROMPT = (
    "You are a grader assessing relevance of a retrieved document to a user question.\n"
    "Here is the retrieved document:\n\n{context}\n\n"
    "Here is the user question: {question}\n"
    "If the document contains keyword(s) or semantic meaning related to the user question, "
    "grade it as relevant. Give a binary score 'yes' or 'no'."
)

REWRITE_PROMPT = (
    "Look at the input and try to reason about the underlying semantic intent / meaning.\n"
    "Here is the initial question:\n-------\n{question}\n-------\n"
    "Formulate an improved question:"
)

GENERATE_PROMPT = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If you don't know the answer, just say that you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Question: {question}\n"
    "Context: {context}"
)

# -------------------------
# Tool Definition
# -------------------------

def retriever_tool(retriever):
    """Create a retriever tool for blog posts."""
    return create_retriever_tool(
        retriever,
        "retrieve_blog_posts",
        "Search and return information about Lilian Weng blog posts."
    )

# -------------------------
# Response Models
# -------------------------

class GradeDocuments(BaseModel):
    """Grade documents using a binary score for relevance check."""
    binary_score: str = Field(description="Relevance score: 'yes' if relevant, or 'no' if not relevant")

grader_model = init_chat_model("openai:gpt-4.1", temperature=0)

# -------------------------
# Node Functions
# -------------------------

def generate_query(state: MessagesState, response_model):
    """Generate a query using the user's messages."""
    response = response_model.bind_tools([retriever_tool]).invoke(state["messages"])
    return {"messages": [response]}

def grade_documents(state: MessagesState) -> Literal["generate_answer", "rewrite_question"]:
    """Determine whether the retrieved documents are relevant to the question."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)

    response = grader_model.with_structured_output(GradeDocuments).invoke(
        [{"role": "user", "content": prompt}]
    )
    return "generate_answer" if response.binary_score == "yes" else "rewrite_question"

def rewrite_question(state: MessagesState):
    """Rewrite the original user question for clarity."""
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [{"role": "user", "content": response.content}]}

def generate_answer(state: MessagesState):
    """Generate an answer using retrieved context."""
    question = state["messages"][0].content
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    response = response_model.invoke([{"role": "user", "content": prompt}])
    return {"messages": [response]}

# -------------------------
# Workflow Setup
# -------------------------

def build_workflow(retriever):
    workflow = StateGraph(MessagesState)

    # Nodes
    workflow.add_node(generate_query)
    workflow.add_node("retrieve", ToolNode([retriever_tool(retriever)]))
    workflow.add_node(rewrite_question)
    workflow.add_node(generate_answer)

    # Edges
    workflow.add_edge(START, "generate_query_or_respond")
    workflow.add_conditional_edges(
        "generate_query_or_respond",
        tools_condition,
        {
            "tools": "retrieve",
            END: END,
        },
    )
    workflow.add_conditional_edges("retrieve", grade_documents)
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("rewrite_question", "generate_query_or_respond")

    return workflow.compile()

# -------------------------
# Example usage
# -------------------------

# graph = build_workflow(retriever)
