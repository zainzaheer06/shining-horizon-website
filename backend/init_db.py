"""
Initialize database with super admin user
Run: python init_db.py
"""
import sys
sys.path.append(".")

from app.database import SessionLocal, engine, Base
from app.models import User, Category, Brand
from app.models.user import UserRole
from app.models.category import CategoryType
from app.services.auth import AuthService

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if super admin exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if not existing_admin:
            # Create super admin
            admin = User(
                username="admin",
                email="admin@shininghorizon.com",
                full_name="Super Admin",
                role=UserRole.SUPER_ADMIN,
                password_hash=AuthService.hash_password("admin123")
            )
            db.add(admin)
            db.commit()
            print("✓ Super admin created (username: admin, password: admin123)")
        else:
            print("✓ Super admin already exists")
        
        # Create sample categories if none exist
        existing_categories = db.query(Category).count()
        
        if existing_categories == 0:
            categories = [
                Category(
                    name="Industrial Automation",
                    slug="industrial-automation",
                    type=CategoryType.DETAILED,
                    description="PLCs, VFDs, HMIs & More",
                    hero_title="Industrial Automation",
                    hero_description="Complete range of industrial automation products",
                    display_order=1,
                    show_on_home=True
                ),
                Category(
                    name="Electrical Products",
                    slug="electrical-products",
                    type=CategoryType.DETAILED,
                    description="Cables, Breakers & More",
                    hero_title="Electrical Products",
                    hero_description="Quality electrical products for all applications",
                    display_order=2,
                    show_on_home=True
                ),
                Category(
                    name="Pneumatic Products",
                    slug="pneumatic-products",
                    type=CategoryType.DETAILED,
                    description="Cylinders, Valves & More",
                    hero_title="Pneumatic Products",
                    hero_description="Industrial pneumatic equipment and accessories",
                    display_order=3,
                    show_on_home=True
                ),
                Category(
                    name="Tools",
                    slug="tools",
                    type=CategoryType.SIMPLE,
                    description="Hand & Power Tools",
                    hero_title="Tools",
                    hero_description="Complete range of hand tools, power tools, and industrial equipment",
                    display_order=4,
                    show_on_home=True
                ),
                Category(
                    name="Lifting Equipment",
                    slug="lifting-equipment",
                    type=CategoryType.SIMPLE,
                    description="Chain Hoists, Wire Ropes & More",
                    hero_title="Lifting Equipment",
                    hero_description="Professional lifting and rigging equipment",
                    display_order=5,
                    show_on_home=True
                ),
            ]
            
            for cat in categories:
                db.add(cat)
            
            db.commit()
            print(f"✓ Created {len(categories)} sample categories")
        else:
            print(f"✓ {existing_categories} categories already exist")
        
        print("\n✓ Database initialized successfully!")
        print("\nYou can now run the server with:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload --port 8000")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
