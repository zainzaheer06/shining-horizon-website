from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..services.category import CategoryService
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/categories", tags=["Categories"])

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
