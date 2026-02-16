from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running"}


from app.database import db

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}
