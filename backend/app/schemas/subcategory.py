from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubcategoryBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    image: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class SubcategoryResponse(SubcategoryBase):
    id: int
    slug: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    product_count: Optional[int] = 0
    category_name: Optional[str] = None
    
    class Config:
        from_attributes = True
