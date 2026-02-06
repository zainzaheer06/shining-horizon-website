// API Configuration and Helper Functions
const API_BASE = 'http://localhost:8000';

// Get stored token
function getToken() {
    return localStorage.getItem('admin_token');
}

// Set token
function setToken(token) {
    localStorage.setItem('admin_token', token);
}

// Remove token
function removeToken() {
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
}

// Get current user
function getCurrentUser() {
    const user = localStorage.getItem('admin_user');
    return user ? JSON.parse(user) : null;
}

// Set current user
function setCurrentUser(user) {
    localStorage.setItem('admin_user', JSON.stringify(user));
}

// Check if logged in
function isLoggedIn() {
    return !!getToken();
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// API Request helper
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, config);
        
        if (response.status === 401) {
            removeToken();
            window.location.href = 'login.html';
            return null;
        }
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Auth API
const authAPI = {
    login: async (username, password) => {
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        });
        if (data) {
            setToken(data.access_token);
            setCurrentUser(data.user);
        }
        return data;
    },
    
    logout: () => {
        removeToken();
        window.location.href = 'login.html';
    },
    
    getMe: () => apiRequest('/auth/me'),
};

// Categories API
const categoriesAPI = {
    getAll: (includeInactive = true) => 
        apiRequest(`/categories?include_inactive=${includeInactive}`),
    
    getById: (id) => apiRequest(`/categories/${id}`),
    
    create: (data) => apiRequest('/categories', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    
    update: (id, data) => apiRequest(`/categories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    
    delete: (id) => apiRequest(`/categories/${id}`, {
        method: 'DELETE',
    }),
};

// Subcategories API
const subcategoriesAPI = {
    getAll: (categoryId = null, includeInactive = true) => {
        let url = `/subcategories?include_inactive=${includeInactive}`;
        if (categoryId) url += `&category_id=${categoryId}`;
        return apiRequest(url);
    },
    
    getById: (id) => apiRequest(`/subcategories/${id}`),
    
    create: (data) => apiRequest('/subcategories', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    
    update: (id, data) => apiRequest(`/subcategories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    
    delete: (id) => apiRequest(`/subcategories/${id}`, {
        method: 'DELETE',
    }),
};

// Products API
const productsAPI = {
    getAll: (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.categoryId) params.append('category_id', filters.categoryId);
        if (filters.subcategoryId) params.append('subcategory_id', filters.subcategoryId);
        if (filters.brandId) params.append('brand_id', filters.brandId);
        params.append('include_inactive', 'true');
        params.append('limit', '500');
        return apiRequest(`/products?${params.toString()}`);
    },
    
    getById: (id) => apiRequest(`/products/${id}`),
    
    create: (data) => apiRequest('/products', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    
    update: (id, data) => apiRequest(`/products/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    
    delete: (id) => apiRequest(`/products/${id}`, {
        method: 'DELETE',
    }),
};

// Brands API
const brandsAPI = {
    getAll: (includeInactive = true) => 
        apiRequest(`/brands?include_inactive=${includeInactive}`),
    
    getById: (id) => apiRequest(`/brands/${id}`),
    
    create: (data) => apiRequest('/brands', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    
    update: (id, data) => apiRequest(`/brands/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    
    delete: (id) => apiRequest(`/brands/${id}`, {
        method: 'DELETE',
    }),
};

// Users API
const usersAPI = {
    getAll: () => apiRequest('/users'),
    
    getById: (id) => apiRequest(`/users/${id}`),
    
    create: (data) => apiRequest('/users', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    
    update: (id, data) => apiRequest(`/users/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }),
    
    delete: (id) => apiRequest(`/users/${id}`, {
        method: 'DELETE',
    }),
};

// Upload API
const uploadAPI = {
    uploadImage: async (file, folder) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getToken();
        const response = await fetch(`${API_BASE}/upload/image/${folder}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        return response.json();
    },
};

// Generator API
const generatorAPI = {
    generateAll: () => apiRequest('/generate/all', { method: 'POST' }),
    
    generateCategory: (id) => apiRequest(`/generate/category/${id}`, { method: 'POST' }),
};

// Import API
const importAPI = {
    importCategories: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getToken();
        const response = await fetch(`${API_BASE}/import/categories`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }
        return response.json();
    },
    
    importSubcategories: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getToken();
        const response = await fetch(`${API_BASE}/import/subcategories`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }
        return response.json();
    },
    
    importBrands: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getToken();
        const response = await fetch(`${API_BASE}/import/brands`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }
        return response.json();
    },
    
    importProducts: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = getToken();
        const response = await fetch(`${API_BASE}/import/products`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }
        return response.json();
    },
};
