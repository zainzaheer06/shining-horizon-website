from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from fastapi import HTTPException, status
import re

from ..models.category import Category
from ..models.product import Product
from ..models.subcategory import Subcategory
from ..schemas.category import CategoryCreate, CategoryUpdate

class CategoryService:
    @staticmethod
    def generate_slug(name: str) -> str:
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    @staticmethod
    def get_all(db: Session, include_inactive: bool = False) -> List[Category]:
        query = db.query(Category)
        if not include_inactive:
            query = query.filter(Category.is_active == True)
        return query.order_by(Category.display_order).all()
    
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Category]:
        return db.query(Category).filter(Category.slug == slug).first()
    
    @staticmethod
    def create(db: Session, category_data: CategoryCreate) -> Category:
        slug = CategoryService.generate_slug(category_data.name)
        
        # Check if slug exists
        existing = CategoryService.get_by_slug(db, slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
        
        category = Category(
            name=category_data.name,
            slug=slug,
            type=category_data.type,
            description=category_data.description,
            hero_title=category_data.hero_title,
            hero_description=category_data.hero_description,
            image=category_data.image,
            display_order=category_data.display_order,
            is_active=category_data.is_active,
            show_on_home=category_data.show_on_home
        )
        
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def update(db: Session, category_id: int, category_data: CategoryUpdate) -> Category:
        category = CategoryService.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        update_data = category_data.model_dump(exclude_unset=True)
        
        # Update slug if name changed
        if "name" in update_data:
            new_slug = CategoryService.generate_slug(update_data["name"])
            existing = CategoryService.get_by_slug(db, new_slug)
            if existing and existing.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category with this name already exists"
                )
            update_data["slug"] = new_slug
        
        for field, value in update_data.items():
            setattr(category, field, value)
        
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def delete(db: Session, category_id: int) -> bool:
        category = CategoryService.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        db.delete(category)
        db.commit()
        return True
    
    @staticmethod
    def get_with_counts(db: Session, category: Category) -> dict:
        product_count = db.query(func.count(Product.id)).filter(Product.category_id == category.id).scalar()
        subcategory_count = db.query(func.count(Subcategory.id)).filter(Subcategory.category_id == category.id).scalar()
        
        return {
            **category.__dict__,
            "product_count": product_count,
            "subcategory_count": subcategory_count
        }
