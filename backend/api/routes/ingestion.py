from fastapi import APIRouter, Depends, UploadFile, File
from typing import List
import uuid
from backend.models.database import DatabaseConnection
from backend.services.schema_discovery import SchemaDiscovery
from backend.services.document_processor import DocumentProcessor

router = APIRouter()

# Simple in-memory store for job status
job_status_store = {}

@router.post("/api/ingest/database")
def ingest_database(db_connection: DatabaseConnection):
    schema_discovery = SchemaDiscovery()
    schema = schema_discovery.analyze_database(db_connection.connection_string)
    return schema

@router.post("/api/ingest/documents")
async def ingest_documents(files: List[UploadFile] = File(...)):
    job_id = str(uuid.uuid4())
    job_status_store[job_id] = {"status": "processing", "total_files": len(files), "processed_files": 0}

    doc_processor = DocumentProcessor()
    
    file_contents = []
    filenames = []
    for file in files:
        contents = await file.read()
        file_contents.append(contents)
        filenames.append(file.filename)

    doc_processor.process_documents(file_contents, filenames)

    job_status_store[job_id]["status"] = "completed"
    job_status_store[job_id]["processed_files"] = len(files)

    return {"job_id": job_id, "message": f"{len(files)} documents are being processed."}

@router.get("/api/ingest/status/{job_id}")
def ingest_status(job_id: str):
    status = job_status_store.get(job_id)
    if not status:
        return {"error": "Job not found"}
    return status
