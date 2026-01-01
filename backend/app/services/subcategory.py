from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException, status
import re

from ..models.subcategory import Subcategory
from ..models.product import Product
from ..models.category import Category
from ..schemas.subcategory import SubcategoryCreate, SubcategoryUpdate

class SubcategoryService:
    @staticmethod
    def generate_slug(name: str) -> str:
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    @staticmethod
    def get_all(db: Session, category_id: Optional[int] = None, include_inactive: bool = False) -> List[Subcategory]:
        query = db.query(Subcategory)
        if category_id:
            query = query.filter(Subcategory.category_id == category_id)
        if not include_inactive:
            query = query.filter(Subcategory.is_active == True)
        return query.order_by(Subcategory.display_order).all()
    
    @staticmethod
    def get_by_id(db: Session, subcategory_id: int) -> Optional[Subcategory]:
        return db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str, category_id: int) -> Optional[Subcategory]:
        return db.query(Subcategory).filter(
            Subcategory.slug == slug,
            Subcategory.category_id == category_id
        ).first()
    
    @staticmethod
    def create(db: Session, subcategory_data: SubcategoryCreate) -> Subcategory:
        # Check if category exists
        category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        slug = SubcategoryService.generate_slug(subcategory_data.name)
        
        # Check if slug exists in this category
        existing = SubcategoryService.get_by_slug(db, slug, subcategory_data.category_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subcategory with this name already exists in this category"
            )
        
        subcategory = Subcategory(
            name=subcategory_data.name,
            slug=slug,
            category_id=subcategory_data.category_id,
            description=subcategory_data.description,
            display_order=subcategory_data.display_order,
            is_active=subcategory_data.is_active
        )
        
        db.add(subcategory)
        db.commit()
        db.refresh(subcategory)
        return subcategory
    
    @staticmethod
    def update(db: Session, subcategory_id: int, subcategory_data: SubcategoryUpdate) -> Subcategory:
        subcategory = SubcategoryService.get_by_id(db, subcategory_id)
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subcategory not found"
            )
        
        update_data = subcategory_data.model_dump(exclude_unset=True)
        
        # Update slug if name changed
        if "name" in update_data:
            new_slug = SubcategoryService.generate_slug(update_data["name"])
            category_id = update_data.get("category_id", subcategory.category_id)
            existing = SubcategoryService.get_by_slug(db, new_slug, category_id)
            if existing and existing.id != subcategory_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Subcategory with this name already exists in this category"
                )
            update_data["slug"] = new_slug
        
        for field, value in update_data.items():
            setattr(subcategory, field, value)
        
        db.commit()
        db.refresh(subcategory)
        return subcategory
    
    @staticmethod
    def delete(db: Session, subcategory_id: int) -> bool:
        subcategory = SubcategoryService.get_by_id(db, subcategory_id)
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subcategory not found"
            )
        
        db.delete(subcategory)
        db.commit()
        return True
    
    @staticmethod
    def get_with_counts(db: Session, subcategory: Subcategory) -> dict:
        product_count = db.query(func.count(Product.id)).filter(Product.subcategory_id == subcategory.id).scalar()
        category = db.query(Category).filter(Category.id == subcategory.category_id).first()
        
        return {
            **subcategory.__dict__,
            "product_count": product_count,
            "category_name": category.name if category else None
        }
