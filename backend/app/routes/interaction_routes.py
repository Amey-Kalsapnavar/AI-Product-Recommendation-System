from fastapi import APIRouter
from app.database import db
from app.models.interaction_model import Interaction

router = APIRouter()

@router.post("/track-interaction")
def track_interaction(interaction: Interaction):
    interaction_dict = interaction.dict()
    db.interactions.insert_one(interaction_dict)
    return {"message": "Interaction tracked successfully"}

@router.get("/interactions")
def get_interactions():
    interactions = list(db.interactions.find({}, {"_id": 0}))
    return interactions