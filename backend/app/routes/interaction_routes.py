from fastapi import APIRouter
from app.database import db
from app.models.interaction_model import Interaction

router = APIRouter()

interaction_scores = {
    "view": 1,
    "click": 2,
    "cart": 3,
    "purchase": 5
}

@router.post("/track-interaction")
def track_interaction(interaction: Interaction):
    interaction_dict = interaction.dict()
    interaction_dict["score"] = interaction_scores.get(interaction.interaction_type, 0)

    db.interactions.insert_one(interaction_dict)
    return {"message": "Interaction tracked successfully"}

@router.get("/interactions")
def get_interactions():
    interactions = list(db.interactions.find({}, {"_id": 0}))
    return interactions

@router.get("/popular-products")
def get_popular_products():
    pipeline = [
        {
            "$group": {
                "_id": "$product_id",
                "total_score": {"$sum": "$score"}
            }
        },
        {
            "$sort": {"total_score": -1}
        }
    ]

    popular_products = list(db.interactions.aggregate(pipeline))

    result = []
    for item in popular_products:
        result.append({
            "product_id": item["_id"],
            "total_score": item["total_score"]
        })

    return result