from fastapi import FastAPI
from app.database import db
from app.routes.product_routes import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}