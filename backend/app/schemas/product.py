from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category_id: int
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    part_number: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    is_featured: bool = False

class ProductCreate(ProductBase):
    image: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    part_number: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    image: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    slug: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_name: Optional[str] = None
    subcategory_name: Optional[str] = None
    brand_name: Optional[str] = None
    brand_logo: Optional[str] = None
    
    class Config:
        from_attributes = True
