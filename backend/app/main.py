from fastapi import FastAPI
from app.database import db

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}
