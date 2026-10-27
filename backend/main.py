from fastapi import FastAPI
from database.connection import engine
from database.connection import Base, engine
from database import models

from fastapi.middleware.cors import CORSMiddleware
from routers.auth import router as auth_router

app = FastAPI(title="Stackly IT Solutions Backend")

app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:56579",
        "http://localhost:56579",
        "null"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

if engine is not None:
    Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Stackly backend is running successfully"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/database-check")
def database_check():
    if engine is None:
        return {"status": "error", "message": "DATABASE_URL is not configured"}

    try:
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"status": "success", "message": "MySQL connection successful"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}