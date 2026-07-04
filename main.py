from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_routes import router as auth_router
from database.db import Base, engine
from models import favorite_model, user_model
from routes.excuse import router as excuse_router
from routes.favorite import router as favorite_router


# Create database tables on application startup.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sorry Not Sorry Backend",
    description="AI-powered excuse generator API built with FastAPI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(excuse_router)
app.include_router(auth_router)
app.include_router(favorite_router)


@app.get("/")
def root():
    return {"message": "Sorry Not Sorry"}
