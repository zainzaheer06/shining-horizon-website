from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..services.product import ProductService
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = Query(None),
    subcategory_id: Optional[int] = Query(None),
    brand_id: Optional[int] = Query(None),
    include_inactive: bool = Query(False),
    skip: int = Query(0),
    limit: int = Query(100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = ProductService.get_all(
        db, category_id, subcategory_id, brand_id, include_inactive, skip, limit
    )
    return [ProductService.get_with_relations(db, product) for product in products]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = ProductService.get_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductService.get_with_relations(db, product)

@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = ProductService.create(db, product_data)
    return ProductService.get_with_relations(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = ProductService.update(db, product_id, product_data)
    return ProductService.get_with_relations(db, product)

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ProductService.delete(db, product_id)
    return {"message": "Product deleted successfully"}
