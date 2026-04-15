# Shining Horizon Trading Website

Industrial trading company website with a dynamic frontend, admin dashboard, and FastAPI backend.

---

## Prerequisites

- Python 3.10+
- pip

---

## Installation

```bash
cd SHINING-HORIZON-Website
pip install -r backend/requirements.txt
```

---

## Running the Website

The site requires **two servers** running at the same time — open two terminal windows.

### Terminal 1 — Backend API (port 8001)

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The API will be available at `http://localhost:8001`

### Terminal 2 — Frontend Server (port 8000)

```bash
cd SHINING-HORIZON-Website
python server.py
```

The website will be available at `http://localhost:8000`

---

## Accessing the Site

| Page | URL |
|------|-----|
| Homepage | http://localhost:8000 |
| Categories | http://localhost:8000/categories |
| Products | http://localhost:8000/products |
| Brands | http://localhost:8000/brands |
| Quote Request | http://localhost:8000/quote |
| Admin Dashboard | http://localhost:8000/admin/ |

### Category & Product URLs

```
http://localhost:8000/category/<slug>
http://localhost:8000/product/<slug>
```

Example: `http://localhost:8000/category/industrial-automation`

---

## Admin Dashboard

Go to `http://localhost:8000/admin/`

Default login credentials:
- **Username:** `admin`
- **Password:** `admin123`

From the admin panel you can manage:
- Categories and Subcategories
- Products and Brands
- Import data via CSV
- User accounts

---

## Project Structure

```
SHINING-HORIZON-Website/
├── server.py                  # Custom frontend server with clean URL routing
├── index.html                 # Homepage
├── categories.html            # Categories listing
├── products.html              # Products listing
├── brands.html                # Brands listing
├── quote.html                 # Quote request form
├── category-dynamic.html      # Dynamic category page (served at /category/<slug>)
├── product-dynamic.html       # Dynamic product page (served at /product/<slug>)
├── components/
│   ├── header.js              # Shared header component
│   ├── footer.js              # Shared footer component
│   └── shared-styles.css      # Shared CSS
├── admin/
│   ├── index.html             # Admin dashboard
│   ├── categories.html
│   ├── subcategories.html
│   ├── products.html
│   ├── brands.html
│   ├── users.html
│   └── import.html
└── backend/
    ├── main.py
    ├── requirements.txt
    ├── shining_horizon.db      # SQLite database
    ├── uploads/               # Uploaded images
    └── app/
        ├── routers/           # API route handlers
        ├── models/            # SQLAlchemy models
        ├── schemas/           # Pydantic schemas
        └── services/          # Business logic
```

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, Tailwind CSS, Vanilla JavaScript |
| Backend | FastAPI, SQLAlchemy, SQLite |
| Auth | JWT tokens |
| Animations | AOS (Animate On Scroll) |
| Fonts | Inter (Google Fonts) |
| Frontend Server | Python `http.server` with custom routing |

---

## URL Routing

The custom `server.py` handles clean URLs:

| Request | Serves |
|---------|--------|
| `/` | `index.html` |
| `/categories` | `categories.html` |
| `/admin/products` | `admin/products.html` |
| `/category/air-treatment` | `category-dynamic.html?slug=air-treatment` |
| `/product/circuit-breakers` | `product-circuit-breakers.html` (static) or `product-dynamic.html` |
| Any `*.html` URL | Redirects to clean URL automatically |
