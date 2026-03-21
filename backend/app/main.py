from fastapi import FastAPI
from app.database import db
from app.routes.product_routes import router as product_router
from app.routes.interaction_routes import router as interaction_router
from app.routes.recommendation_routes import router as recommendation_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ── CORS — allow React frontend ────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────
app.include_router(product_router)
app.include_router(interaction_router)
app.include_router(recommendation_router, prefix="/recommendations", tags=["Recommendations"])

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}