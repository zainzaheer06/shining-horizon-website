from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
import os
from typing import List

from ..config import settings
from ..models.category import Category, CategoryType
from ..models.subcategory import Subcategory
from ..models.product import Product
from ..models.brand import Brand

class PageGenerator:
    def __init__(self, db: Session):
        self.db = db
        self.frontend_dir = settings.FRONTEND_DIR
        self.template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        
        # Create template directory if not exists
        os.makedirs(self.template_dir, exist_ok=True)
        
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
    
    def generate_all(self):
        """Generate all static pages"""
        results = {
            "categories": [],
            "products": [],
            "errors": []
        }
        
        try:
            # Generate category pages
            categories = self.db.query(Category).filter(Category.is_active == True).all()
            for category in categories:
                try:
                    self.generate_category_page(category)
                    results["categories"].append(category.name)
                except Exception as e:
                    results["errors"].append(f"Category {category.name}: {str(e)}")
            
            # Generate product pages for detailed categories
            for category in categories:
                if category.type == CategoryType.DETAILED:
                    subcategories = self.db.query(Subcategory).filter(
                        Subcategory.category_id == category.id,
                        Subcategory.is_active == True
                    ).all()
                    
                    for subcategory in subcategories:
                        try:
                            self.generate_product_page(category, subcategory)
                            results["products"].append(f"{category.slug}/{subcategory.slug}")
                        except Exception as e:
                            results["errors"].append(f"Product page {subcategory.name}: {str(e)}")
            
        except Exception as e:
            results["errors"].append(f"General error: {str(e)}")
        
        return results
    
    def generate_category_page(self, category: Category):
        """Generate a category page based on its type"""
        if category.type == CategoryType.DETAILED:
            return self._generate_detailed_category(category)
        else:
            return self._generate_simple_category(category)
    
    def _generate_detailed_category(self, category: Category):
        """Generate detailed category page (like Industrial Automation)"""
        subcategories = self.db.query(Subcategory).filter(
            Subcategory.category_id == category.id,
            Subcategory.is_active == True
        ).order_by(Subcategory.display_order).all()
        
        brands = self.db.query(Brand).filter(Brand.is_active == True).order_by(Brand.display_order).all()
        
        template = self.env.get_template("category_detailed.html")
        html = template.render(
            category=category,
            subcategories=subcategories,
            brands=brands
        )
        
        filename = f"category-{category.slug}.html"
        filepath = os.path.join(self.frontend_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        return filepath
    
    def _generate_simple_category(self, category: Category):
        """Generate simple category page (like Tools)"""
        products = self.db.query(Product).filter(
            Product.category_id == category.id,
            Product.is_active == True
        ).order_by(Product.display_order).all()
        
        brands = self.db.query(Brand).filter(Brand.is_active == True).order_by(Brand.display_order).all()
        
        template = self.env.get_template("category_simple.html")
        html = template.render(
            category=category,
            products=products,
            brands=brands
        )
        
        filename = f"category-{category.slug}.html"
        filepath = os.path.join(self.frontend_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        return filepath
    
    def generate_product_page(self, category: Category, subcategory: Subcategory):
        """Generate product listing page for a subcategory"""
        products = self.db.query(Product).filter(
            Product.subcategory_id == subcategory.id,
            Product.is_active == True
        ).order_by(Product.display_order).all()
        
        # Get brand info for each product
        products_with_brands = []
        for product in products:
            brand = None
            if product.brand_id:
                brand = self.db.query(Brand).filter(Brand.id == product.brand_id).first()
            products_with_brands.append({
                "product": product,
                "brand": brand
            })
        
        brands = self.db.query(Brand).filter(Brand.is_active == True).order_by(Brand.display_order).all()
        
        template = self.env.get_template("product_listing.html")
        html = template.render(
            category=category,
            subcategory=subcategory,
            products=products_with_brands,
            brands=brands
        )
        
        filename = f"product-{subcategory.slug}.html"
        filepath = os.path.join(self.frontend_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        return filepath
