from fastapi import FastAPI, Request
from agentic_model import agentic_process

app = FastAPI()

@app.post("/query")
async def query_endpoint(request: Request):
    data = await request.json()
    query = data.get("query", "")
    result = agentic_process(query)
    return result