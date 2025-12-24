// Shared Header Component
function loadHeader() {
    // Check if we're on the home page
    const isHomePage = window.location.pathname === '/' || window.location.pathname.endsWith('index.html') || window.location.pathname === '';
    
    const headerHTML = `
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-3">
                <a href="${isHomePage ? '#home' : 'index.html'}" class="flex items-center gap-3">
                    <img src="public/logo/Shinning_Horizon_logo.png" alt="Shining Horizon Logo" class="h-12 w-auto">
                    <div class="hidden sm:flex flex-col justify-center border-l border-gray-300 pl-3">
                        <h1 class="text-primary font-bold text-xs tracking-wider leading-tight">SHINING HORIZON TRADING CO.</h1>
                        <p class="text-primary-dark mt-0.5" dir="rtl" style="font-family: 'Noto Sans Arabic', 'Segoe UI', Tahoma, sans-serif; font-size: 13px; font-weight: 500;">شركة الأفق المشع للتجارة</p>
                    </div>
                </a>
                <nav class="hidden lg:flex items-center gap-8">
                    <a href="${isHomePage ? '#home' : 'index.html'}" class="text-gray-600 hover:text-primary transition font-medium text-sm">Home</a>
                    <a href="${isHomePage ? '#about' : 'index.html#about'}" class="text-gray-600 hover:text-primary transition font-medium text-sm">About</a>
                    <a href="categories.html" class="text-gray-600 hover:text-primary transition font-medium text-sm">Categories</a>
                    <a href="brands.html" class="text-gray-600 hover:text-primary transition font-medium text-sm">Brands</a>
                    <a href="${isHomePage ? '#products' : 'index.html#products'}" class="text-gray-600 hover:text-primary transition font-medium text-sm">Products</a>
                    <a href="${isHomePage ? '#services' : 'index.html#services'}" class="text-gray-600 hover:text-primary transition font-medium text-sm">Services</a>
                    <a href="${isHomePage ? '#contact' : 'index.html#contact'}" class="text-gray-600 hover:text-primary transition font-medium text-sm">Contact</a>
                </nav>
                <div class="flex items-center gap-4">
                    <a href="quote.html" class="hidden sm:flex btn-primary bg-primary text-white font-semibold py-3 px-6 rounded-lg">Get Quote</a>
                    <button id="mobile-menu-btn" class="lg:hidden text-gray-600 p-2">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
                    </button>
                </div>
            </div>
        </div>
        <div id="mobile-menu" class="lg:hidden fixed inset-0 bg-white z-50 transform translate-x-full transition-transform duration-300">
            <div class="p-6">
                <div class="flex justify-between items-center mb-10">
                    <h2 class="text-2xl font-bold text-primary">Menu</h2>
                    <button id="close-menu" class="text-gray-600 p-2">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>
                </div>
                <nav class="flex flex-col gap-6">
                    <a href="${isHomePage ? '#home' : 'index.html'}" class="text-xl font-semibold text-gray-700 hover:text-primary">Home</a>
                    <a href="${isHomePage ? '#about' : 'index.html#about'}" class="text-xl font-semibold text-gray-700 hover:text-primary">About</a>
                    <a href="categories.html" class="text-xl font-semibold text-gray-700 hover:text-primary">Categories</a>
                    <a href="brands.html" class="text-xl font-semibold text-gray-700 hover:text-primary">Brands</a>
                    <a href="${isHomePage ? '#products' : 'index.html#products'}" class="text-xl font-semibold text-gray-700 hover:text-primary">Products</a>
                    <a href="${isHomePage ? '#services' : 'index.html#services'}" class="text-xl font-semibold text-gray-700 hover:text-primary">Services</a>
                    <a href="${isHomePage ? '#contact' : 'index.html#contact'}" class="text-xl font-semibold text-gray-700 hover:text-primary">Contact</a>
                    <a href="quote.html" class="text-xl font-semibold text-primary">Get Quote</a>
                </nav>
            </div>
        </div>
    </header>
    `;
    
    document.getElementById('header-placeholder').innerHTML = headerHTML;
    
    // Initialize mobile menu
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeMenuBtn = document.getElementById('close-menu');
    
    mobileMenuBtn?.addEventListener('click', () => { 
        mobileMenu.style.transform = 'translateX(0)'; 
    });
    closeMenuBtn?.addEventListener('click', () => { 
        mobileMenu.style.transform = 'translateX(100%)'; 
    });
    mobileMenu?.querySelectorAll('a').forEach(link => { 
        link.addEventListener('click', () => { 
            mobileMenu.style.transform = 'translateX(100%)'; 
        }); 
    });
}

// Auto-load when DOM is ready
document.addEventListener('DOMContentLoaded', loadHeader);
