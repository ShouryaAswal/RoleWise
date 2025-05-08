from fastapi import FastAPI, Request
from agentic_model import agentic_process

app = FastAPI()

@app.post("/query")
async def query_endpoint(request: Request):
    data = await request.json()
    query = data.get("query", "")
    result = agentic_process(query)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=10000)