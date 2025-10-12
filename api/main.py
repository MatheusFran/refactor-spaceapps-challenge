from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.main import build_agent

graph = build_agent()
app = FastAPI(title="agent_api_rag", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryInput(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Agent API RAG está funcionando!",
        "version": "1.0",
        "endpoints": {
            "query": "/api/query",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/query")
async def query_agent(payload: QueryInput):
    try:
        state = {"messages": [{"role": "user", "content": payload.question}]}
        result = graph.invoke(state)

        return {
            "response": result["messages"][-1].content,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


handler = app
