from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id", ondelete="SET NULL"), nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="SET NULL"), nullable=True)
    
    name = Column(String(200), nullable=False)
    slug = Column(String(200), index=True, nullable=False)
    part_number = Column(String(100))  # For detailed category products
    description = Column(Text)
    short_description = Column(String(500))  # For simple category products
    image = Column(String(255))
    
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    subcategory = relationship("Subcategory", back_populates="products")
    brand = relationship("Brand", back_populates="products")
