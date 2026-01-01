from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
import re

from ..models.product import Product
from ..models.category import Category
from ..models.subcategory import Subcategory
from ..models.brand import Brand
from ..schemas.product import ProductCreate, ProductUpdate

class ProductService:
    @staticmethod
    def generate_slug(name: str, part_number: Optional[str] = None) -> str:
        base = part_number if part_number else name
        slug = base.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    @staticmethod
    def get_all(
        db: Session,
        category_id: Optional[int] = None,
        subcategory_id: Optional[int] = None,
        brand_id: Optional[int] = None,
        include_inactive: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        query = db.query(Product)
        
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if subcategory_id:
            query = query.filter(Product.subcategory_id == subcategory_id)
        if brand_id:
            query = query.filter(Product.brand_id == brand_id)
        if not include_inactive:
            query = query.filter(Product.is_active == True)
        
        return query.order_by(Product.display_order).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Product]:
        return db.query(Product).filter(Product.slug == slug).first()
    
    @staticmethod
    def create(db: Session, product_data: ProductCreate) -> Product:
        # Check if category exists
        category = db.query(Category).filter(Category.id == product_data.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Check subcategory if provided
        if product_data.subcategory_id:
            subcategory = db.query(Subcategory).filter(Subcategory.id == product_data.subcategory_id).first()
            if not subcategory:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subcategory not found"
                )
        
        # Check brand if provided
        if product_data.brand_id:
            brand = db.query(Brand).filter(Brand.id == product_data.brand_id).first()
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Brand not found"
                )
        
        slug = ProductService.generate_slug(product_data.name, product_data.part_number)
        
        # Make slug unique if exists
        existing = ProductService.get_by_slug(db, slug)
        if existing:
            count = 1
            while ProductService.get_by_slug(db, f"{slug}-{count}"):
                count += 1
            slug = f"{slug}-{count}"
        
        product = Product(
            name=product_data.name,
            slug=slug,
            category_id=product_data.category_id,
            subcategory_id=product_data.subcategory_id,
            brand_id=product_data.brand_id,
            part_number=product_data.part_number,
            description=product_data.description,
            short_description=product_data.short_description,
            display_order=product_data.display_order,
            is_active=product_data.is_active,
            is_featured=product_data.is_featured
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
        product = ProductService.get_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        update_data = product_data.model_dump(exclude_unset=True)
        
        # Update slug if name or part_number changed
        if "name" in update_data or "part_number" in update_data:
            name = update_data.get("name", product.name)
            part_number = update_data.get("part_number", product.part_number)
            new_slug = ProductService.generate_slug(name, part_number)
            
            existing = ProductService.get_by_slug(db, new_slug)
            if existing and existing.id != product_id:
                count = 1
                while ProductService.get_by_slug(db, f"{new_slug}-{count}"):
                    count += 1
                new_slug = f"{new_slug}-{count}"
            
            update_data["slug"] = new_slug
        
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        product = ProductService.get_by_id(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        db.delete(product)
        db.commit()
        return True
    
    @staticmethod
    def get_with_relations(db: Session, product: Product) -> dict:
        category = db.query(Category).filter(Category.id == product.category_id).first()
        subcategory = db.query(Subcategory).filter(Subcategory.id == product.subcategory_id).first() if product.subcategory_id else None
        brand = db.query(Brand).filter(Brand.id == product.brand_id).first() if product.brand_id else None
        
        return {
            **product.__dict__,
            "category_name": category.name if category else None,
            "subcategory_name": subcategory.name if subcategory else None,
            "brand_name": brand.name if brand else None,
            "brand_logo": brand.logo if brand else None
        }
