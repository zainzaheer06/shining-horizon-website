from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..models.category import CategoryType

class CategoryBase(BaseModel):
    name: str
    type: CategoryType = CategoryType.SIMPLE
    description: Optional[str] = None
    hero_title: Optional[str] = None
    hero_description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True
    show_on_home: bool = True

class CategoryCreate(CategoryBase):
    image: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    description: Optional[str] = None
    hero_title: Optional[str] = None
    hero_description: Optional[str] = None
    image: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None
    show_on_home: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    slug: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    product_count: Optional[int] = 0
    subcategory_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
