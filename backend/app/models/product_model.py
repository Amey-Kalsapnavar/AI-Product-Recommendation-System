from pydantic import BaseModel

class Product(BaseModel):
    name: str
    category: str
    description: str
    price: float
    image_url: str