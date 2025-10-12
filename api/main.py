import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agent.main import build_agent

graph = build_agent()
app = FastAPI(title="agent_api_rag", version="1.0")

class QueryInput(BaseModel):
    question: str

@app.post("/query")
async def query_agent(payload: QueryInput):
    try:
        state = {"messages": [{"role": "user", "content": payload.question}]}
        result = graph.invoke(state)

        return {
            "response": result["messages"][-1].content,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)