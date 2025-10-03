from fastapi import APIRouter
from backend.services.schema_discovery import SchemaDiscovery
from backend.config import settings

router = APIRouter()

@router.get("/api/schema")
def get_schema():
    """
    Return current discovered schema for visualization
    """
    schema_discovery = SchemaDiscovery()
    schema = schema_discovery.analyze_database(settings.DATABASE_URL)
    return schema
