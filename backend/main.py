from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import ingestion, query, schema

app = FastAPI()

# This should be more restrictive in a production environment
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router)
app.include_router(query.router)
app.include_router(schema.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the NLP Query Engine API"}
