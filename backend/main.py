from fastapi import FastAPI
from schemas import QueryRequest, QueryResponse
from model import get_recommendations

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend", response_model=QueryResponse)
def recommend(query: QueryRequest):
    return get_recommendations(query.query)
