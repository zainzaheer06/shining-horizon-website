from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.product import ProductCreate, ProductUpdate, ProductResponse
from ..services.product import ProductService
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/public")
def get_public_products(
    category_slug: Optional[str] = Query(None),
    subcategory_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Public endpoint — no auth required. Filter by category or subcategory slug."""
    from ..models.product import Product
    from ..models.category import Category
    from ..models.subcategory import Subcategory
    from ..models.brand import Brand

    query = db.query(Product).filter(Product.is_active == True)

    if category_slug:
        cat = db.query(Category).filter(Category.slug == category_slug).first()
        if not cat:
            return []  # slug not found — return empty, don't leak all products
        query = query.filter(Product.category_id == cat.id)

    if subcategory_slug:
        sub = db.query(Subcategory).filter(Subcategory.slug == subcategory_slug).first()
        if not sub:
            return []
        query = query.filter(Product.subcategory_id == sub.id)

    products = query.order_by(Product.display_order).all()

    result = []
    for p in products:
        brand = db.query(Brand).filter(Brand.id == p.brand_id).first() if p.brand_id else None
        sub = db.query(Subcategory).filter(Subcategory.id == p.subcategory_id).first() if p.subcategory_id else None
        result.append({
            "id": p.id, "name": p.name, "slug": p.slug,
            "part_number": p.part_number, "description": p.description,
            "short_description": p.short_description, "image": p.image,
            "brand_name": brand.name if brand else None,
            "subcategory_name": sub.name if sub else None,
        })
    return result

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
