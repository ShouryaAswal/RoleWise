from pydantic import BaseModel
from typing import List

class Assessment(BaseModel):
    name: str
    url: str
    remote_support: bool
    adaptive_support: bool
    duration: int
    test_type: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    recommendations: List[Assessment]
