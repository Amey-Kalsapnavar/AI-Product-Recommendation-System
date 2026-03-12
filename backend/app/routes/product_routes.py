from fastapi import APIRouter
from app.database import db
from app.models.product_model import Product

router = APIRouter()

@router.post("/add-product")
def add_product(product: Product):
    product_dict = product.dict()
    db.products.insert_one(product_dict)
    return {"message": "Product added successfully"}

from fastapi import APIRouter
from app.database import db
from app.models.product_model import Product

router = APIRouter()

@router.post("/add-product")
def add_product(product: Product):
    product_dict = product.dict()
    db.products.insert_one(product_dict)
    return {"message": "Product added successfully"}

@router.get("/products")
def get_products():
    products = list(db.products.find({}, {"_id": 0}))
    return products