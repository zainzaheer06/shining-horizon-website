# Shining Horizon Trading Website

## Overview
Complete industrial trading company website with product categories, detailed product pages, and quote request system.

## New Features Added

### 1. Category Pages System
- **Main Categories Page** (`categories.html`) - Overview of all product categories
- **Individual Category Pages** - Detailed pages for each category with products and brands
- **Product Detail Pages** - Comprehensive product information with specifications

### 2. Lifting Equipment Category
- New category added with 8 different product types
- Detailed specifications and capacity information
- Weight capacity ranges from 0.5 to 50+ tons
- Professional brands like Kito, Elephant, Crosby, etc.

### 3. Quote Request System
- **Multi-step Quote Form** (`quote.html`)
- Step 1: Product Information
- Step 2: Company Information  
- Step 3: Project Details
- Pre-populated data when coming from product/brand pages

### 4. Enhanced Navigation
- Updated main navigation to include Categories
- Breadcrumb navigation on all pages
- Mobile-responsive design

## File Structure

```
├── index.html                 # Main homepage
├── categories.html           # All categories overview
├── category-lifting.html     # Lifting equipment category
├── product-chain-hoist.html  # Chain hoist product details
├── quote.html               # Quote request form
└── public/
    ├── logo/
    ├── categories/
    ├── products/
    └── brands/
```

## How It Works

### Category Flow
1. **Homepage** → Click category → **Category Page**
2. **Category Page** → Click product → **Product Detail Page**
3. **Product Page** → Click brand → **Quote Page** (pre-filled)

### Quote Request Flow
1. User can access quote form from any page
2. Form pre-populates with selected product/brand/category
3. Multi-step form collects comprehensive information
4. Form submission sends detailed quote request

### Brand Selection
- Each category shows trusted brands
- Clicking brand redirects to quote form with pre-selected data
- Quote form includes brand, category, and product information

## Key Features

### Lifting Equipment Specifications
- **Chain Hoists**: 0.5-20 ton capacity, 3-12m lift height
- **Wire Rope Hoists**: 1-50 ton capacity, 6-30m lift height  
- **Shackles**: 0.33-150 ton WLL, stainless steel
- **Complete specifications table** with dimensions and weights

### Responsive Design
- Mobile-first approach
- Touch-friendly navigation
- Optimized images and loading
- AOS animations for smooth experience

## Running the Website

1. Start HTTP server: `python -m http.server 8000`
2. Open browser: `http://localhost:8000`
3. Navigate through categories and products
4. Test quote request functionality

## Technical Stack
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Animations**: AOS (Animate On Scroll)
- **Icons**: Heroicons (SVG)
- **Fonts**: Inter (Google Fonts)
- **Server**: Python HTTP Server (development)

## Browser Support
- Chrome, Firefox, Safari, Edge
- Mobile browsers (iOS Safari, Chrome Mobile)
- Responsive breakpoints: sm, md, lg, xl# shining-horizon-website
