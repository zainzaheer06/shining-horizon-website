from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    display_order: int = 0
    is_active: bool = True

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    logo: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class BrandResponse(BrandBase):
    id: int
    slug: str
    logo: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    product_count: Optional[int] = 0
    
    class Config:
        from_attributes = True
