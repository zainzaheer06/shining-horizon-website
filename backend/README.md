# Shining Horizon Admin Backend

FastAPI backend for the Shining Horizon Trading admin dashboard.

## Setup

### 1. Install PostgreSQL
Make sure PostgreSQL is installed and running.

### 2. Create Database
```sql
CREATE DATABASE shining_horizon;
```

### 3. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your database credentials
```

### 6. Initialize Database
```bash
python init_db.py
```

This will:
- Create all database tables
- Create a super admin user (username: `admin`, password: `admin123`)
- Create sample categories

### 7. Run the Server
```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Default Credentials

- Username: `admin`
- Password: `admin123`

**Change these in production!**

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Categories
- `GET /categories` - List all categories
- `POST /categories` - Create category
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

### Subcategories
- `GET /subcategories` - List subcategories
- `POST /subcategories` - Create subcategory
- `PUT /subcategories/{id}` - Update subcategory
- `DELETE /subcategories/{id}` - Delete subcategory

### Products
- `GET /products` - List products (with filters)
- `POST /products` - Create product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Brands
- `GET /brands` - List brands
- `POST /brands` - Create brand
- `PUT /brands/{id}` - Update brand
- `DELETE /brands/{id}` - Delete brand

### Upload
- `POST /upload/image/{folder}` - Upload image

### Page Generator
- `POST /generate/all` - Generate all static HTML pages
- `POST /generate/category/{id}` - Generate specific category page

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── database.py       # Database connection
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routers/          # API routes
│   ├── services/         # Business logic
│   └── templates/        # Jinja2 templates for page generation
├── uploads/              # Uploaded images
├── requirements.txt
├── init_db.py           # Database initialization script
└── README.md
```
