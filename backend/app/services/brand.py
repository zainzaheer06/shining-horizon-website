from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException, status
import re

from ..models.brand import Brand
from ..models.product import Product
from ..schemas.brand import BrandCreate, BrandUpdate

class BrandService:
    @staticmethod
    def generate_slug(name: str) -> str:
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    @staticmethod
    def get_all(db: Session, include_inactive: bool = False) -> List[Brand]:
        query = db.query(Brand)
        if not include_inactive:
            query = query.filter(Brand.is_active == True)
        return query.order_by(Brand.display_order).all()
    
    @staticmethod
    def get_by_id(db: Session, brand_id: int) -> Optional[Brand]:
        return db.query(Brand).filter(Brand.id == brand_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Brand]:
        return db.query(Brand).filter(Brand.slug == slug).first()
    
    @staticmethod
    def create(db: Session, brand_data: BrandCreate) -> Brand:
        slug = BrandService.generate_slug(brand_data.name)
        
        # Check if slug exists
        existing = BrandService.get_by_slug(db, slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Brand with this name already exists"
            )
        
        brand = Brand(
            name=brand_data.name,
            slug=slug,
            logo=brand_data.logo,
            display_order=brand_data.display_order,
            is_active=brand_data.is_active
        )
        
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    
    @staticmethod
    def update(db: Session, brand_id: int, brand_data: BrandUpdate) -> Brand:
        brand = BrandService.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        
        update_data = brand_data.model_dump(exclude_unset=True)
        
        # Update slug if name changed
        if "name" in update_data:
            new_slug = BrandService.generate_slug(update_data["name"])
            existing = BrandService.get_by_slug(db, new_slug)
            if existing and existing.id != brand_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Brand with this name already exists"
                )
            update_data["slug"] = new_slug
        
        for field, value in update_data.items():
            setattr(brand, field, value)
        
        db.commit()
        db.refresh(brand)
        return brand
    
    @staticmethod
    def delete(db: Session, brand_id: int) -> bool:
        brand = BrandService.get_by_id(db, brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        
        db.delete(brand)
        db.commit()
        return True
    
    @staticmethod
    def get_with_counts(db: Session, brand: Brand) -> dict:
        product_count = db.query(func.count(Product.id)).filter(Product.brand_id == brand.id).scalar()
        
        return {
            **brand.__dict__,
            "product_count": product_count
        }
