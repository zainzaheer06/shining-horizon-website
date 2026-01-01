from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..schemas.subcategory import SubcategoryCreate, SubcategoryUpdate, SubcategoryResponse
from ..services.subcategory import SubcategoryService
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/subcategories", tags=["Subcategories"])

@router.get("/", response_model=List[SubcategoryResponse])
def get_subcategories(
    category_id: Optional[int] = Query(None),
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subcategories = SubcategoryService.get_all(db, category_id, include_inactive)
    return [SubcategoryService.get_with_counts(db, sub) for sub in subcategories]

@router.get("/{subcategory_id}", response_model=SubcategoryResponse)
def get_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subcategory = SubcategoryService.get_by_id(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return SubcategoryService.get_with_counts(db, subcategory)

@router.post("/", response_model=SubcategoryResponse)
def create_subcategory(
    subcategory_data: SubcategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subcategory = SubcategoryService.create(db, subcategory_data)
    return SubcategoryService.get_with_counts(db, subcategory)

@router.put("/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(
    subcategory_id: int,
    subcategory_data: SubcategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subcategory = SubcategoryService.update(db, subcategory_id, subcategory_data)
    return SubcategoryService.get_with_counts(db, subcategory)

@router.delete("/{subcategory_id}")
def delete_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    SubcategoryService.delete(db, subcategory_id)
    return {"message": "Subcategory deleted successfully"}
