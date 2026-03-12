from pydantic import BaseModel

class Interaction(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str