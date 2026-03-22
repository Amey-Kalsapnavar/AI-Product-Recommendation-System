from fastapi import APIRouter
from app.ml_engine import (
    get_popularity_recommendations,
    get_cf_recommendations,
    get_hybrid_recommendations
)

router = APIRouter()

@router.get("/popular")
def popular_recommendations(top_n: int = 10):
    """Get top N most popular products"""
    results = get_popularity_recommendations(top_n=top_n)
    return {
        "type": "popularity-based",
        "count": len(results),
        "recommendations": results
    }

@router.get("/collaborative/{user_id}")
def collaborative_recommendations(user_id: str, top_n: int = 10):
    """Get CF recommendations for a specific user"""
    results = get_cf_recommendations(user_id=user_id, top_n=top_n)
    return {
        "type": "collaborative-filtering",
        "user_id": user_id,
        "count": len(results) if isinstance(results, list) else 0,
        "recommendations": results
    }

@router.get("/hybrid/{user_id}")
def hybrid_recommendations(user_id: str, top_n: int = 10):
    """Get hybrid recommendations for a specific user"""
    results = get_hybrid_recommendations(user_id=user_id, top_n=top_n)
    return {
        "type": "hybrid",
        "user_id": user_id,
        "count": len(results) if isinstance(results, list) else 0,
        "recommendations": results
    }
    
@router.get("/users/sample")
def get_sample_users():
    """Get sample user IDs that have personalized recommendations"""
    from app.ml_engine import get_sample_users
    users = get_sample_users(n=20)
    return {"users": users}