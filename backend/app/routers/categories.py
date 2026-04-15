from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..schemas.product import ProductResponse
from ..services.category import CategoryService
from ..services.auth import get_current_user
from ..models.user import User
from ..models.product import Product
from ..models.subcategory import Subcategory

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/public", response_model=List[CategoryResponse])
def get_public_categories(db: Session = Depends(get_db)):
    """Public endpoint — no auth required. Returns active categories only."""
    categories = CategoryService.get_all(db, include_inactive=False)
    return [CategoryService.get_with_counts(db, cat) for cat in categories]

@router.get("/public/{slug}", response_model=CategoryResponse)
def get_public_category_by_slug(slug: str, db: Session = Depends(get_db)):
    """Public endpoint — fetch a single category by slug, no auth required."""
    category = CategoryService.get_by_slug(db, slug)
    if not category or not category.is_active:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryService.get_with_counts(db, category)

@router.get("/public/{slug}/products")
def get_public_category_products(slug: str, db: Session = Depends(get_db)):
    """Public endpoint — fetch products for a category by slug, no auth required."""
    category = CategoryService.get_by_slug(db, slug)
    if not category or not category.is_active:
        raise HTTPException(status_code=404, detail="Category not found")
    products = db.query(Product).filter(
        Product.category_id == category.id,
        Product.is_active == True
    ).order_by(Product.display_order).all()
    subcategories = db.query(Subcategory).filter(
        Subcategory.category_id == category.id,
        Subcategory.is_active == True
    ).order_by(Subcategory.display_order).all()
    return {
        "category": CategoryService.get_with_counts(db, category),
        "products": [
            {
                "id": p.id, "name": p.name, "slug": p.slug,
                "part_number": p.part_number, "description": p.description,
                "short_description": p.short_description, "image": p.image,
                "brand_id": p.brand_id, "subcategory_id": p.subcategory_id,
            } for p in products
        ],
        "subcategories": [
            {"id": s.id, "name": s.name, "slug": s.slug, "description": s.description}
            for s in subcategories
        ]
    }

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = CategoryService.get_all(db, include_inactive)
    return [CategoryService.get_with_counts(db, cat) for cat in categories]

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = CategoryService.get_by_id(db, category_id)
    if not category:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryService.get_with_counts(db, category)

@router.post("/", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = CategoryService.create(db, category_data)
    return CategoryService.get_with_counts(db, category)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = CategoryService.update(db, category_id, category_data)
    return CategoryService.get_with_counts(db, category)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    CategoryService.delete(db, category_id)
    return {"message": "Category deleted successfully"}
