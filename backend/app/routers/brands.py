from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.brand import BrandCreate, BrandUpdate, BrandResponse
from ..services.brand import BrandService
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.get("/", response_model=List[BrandResponse])
def get_brands(
    include_inactive: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brands = BrandService.get_all(db, include_inactive)
    return [BrandService.get_with_counts(db, brand) for brand in brands]

@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = BrandService.get_by_id(db, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return BrandService.get_with_counts(db, brand)

@router.post("/", response_model=BrandResponse)
def create_brand(
    brand_data: BrandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = BrandService.create(db, brand_data)
    return BrandService.get_with_counts(db, brand)

@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    brand_data: BrandUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand = BrandService.update(db, brand_id, brand_data)
    return BrandService.get_with_counts(db, brand)

@router.delete("/{brand_id}")
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    BrandService.delete(db, brand_id)
    return {"message": "Brand deleted successfully"}
