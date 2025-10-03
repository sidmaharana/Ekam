from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.services.query_engine import QueryEngine
from backend.config import settings

class Query(BaseModel):
    query: str

router = APIRouter()

@router.post("/api/query")
def query(query: Query):
    query_engine = QueryEngine(settings.DATABASE_URL)
    result = query_engine.process_query(query.query)
    return result

@router.get("/api/query/history")
def query_history():
    # Placeholder for query history implementation
    return {"message": "Query history endpoint"}