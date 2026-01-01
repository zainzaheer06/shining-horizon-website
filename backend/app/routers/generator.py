from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.generator import PageGenerator
from ..services.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/generate", tags=["Page Generator"])

@router.post("/all")
def generate_all_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate all static HTML pages from database"""
    generator = PageGenerator(db)
    results = generator.generate_all()
    return results

@router.post("/category/{category_id}")
def generate_category_page(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a specific category page"""
    from ..services.category import CategoryService
    
    category = CategoryService.get_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    generator = PageGenerator(db)
    filepath = generator.generate_category_page(category)
    
    return {"message": "Page generated successfully", "filepath": filepath}
