// Utility Functions

// Show toast notification
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            ${type === 'success' 
                ? '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>'
                : '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>'}
        </svg>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// Show loading
function showLoading(container) {
    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
        </div>
    `;
}

// Show empty state
function showEmptyState(container, message = 'No items found') {
    container.innerHTML = `
        <div class="empty-state">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
            <h3>${message}</h3>
            <p>Click the button above to add a new item</p>
        </div>
    `;
}

// Open modal
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Confirm dialog
function confirmDialog(message) {
    return new Promise((resolve) => {
        const result = confirm(message);
        resolve(result);
    });
}

// Format date
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

// Truncate text
function truncateText(text, maxLength = 50) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Update page title
function setPageTitle(title) {
    document.title = `${title} - Shining Horizon Admin`;
    const headerTitle = document.querySelector('.header-title');
    if (headerTitle) headerTitle.textContent = title;
}

// Initialize user info in header
function initUserInfo() {
    const user = getCurrentUser();
    if (user) {
        const userNameEl = document.querySelector('.user-name');
        const userRoleEl = document.querySelector('.user-role');
        const userAvatarEl = document.querySelector('.user-avatar');
        
        if (userNameEl) userNameEl.textContent = user.full_name || user.username;
        if (userRoleEl) userRoleEl.textContent = user.role === 'super_admin' ? 'Super Admin' : 'Admin';
        if (userAvatarEl) userAvatarEl.textContent = (user.full_name || user.username).charAt(0).toUpperCase();
    }
}

// Handle image upload preview
function handleImageUpload(inputId, previewId, callback) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    input.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.innerHTML = `<img src="${e.target.result}" class="image-preview" alt="Preview">`;
        };
        reader.readAsDataURL(file);
        
        // Call callback if provided
        if (callback) {
            callback(file);
        }
    });
}

// Set active nav item
function setActiveNav(page) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });
}

// Populate select with options
function populateSelect(selectId, items, valueKey = 'id', labelKey = 'name', placeholder = 'Select...') {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    select.innerHTML = `<option value="">${placeholder}</option>`;
    items.forEach(item => {
        select.innerHTML += `<option value="${item[valueKey]}">${escapeHtml(item[labelKey])}</option>`;
    });
}

// Get form data as object
function getFormData(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const data = {};

    // Explicitly capture all checkboxes first (unchecked ones are absent from FormData)
    Array.from(form.elements).forEach(el => {
        if (el.type === 'checkbox' && el.name) {
            data[el.name] = el.checked;
        }
    });

    formData.forEach((value, key) => {
        const el = form.elements[key];
        if (el?.type === 'checkbox') {
            return; // already handled above
        } else if (value !== '') {
            // Only convert to number for number inputs and selects, not text fields
            if ((el?.type === 'number' || el?.tagName === 'SELECT') && !isNaN(value) && value.trim() !== '') {
                data[key] = Number(value);
            } else {
                data[key] = value;
            }
        }
    });

    return data;
}

// Reset form
function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) form.reset();
}

// Fill form with data
function fillForm(formId, data) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    Object.keys(data).forEach(key => {
        const element = form.elements[key];
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = data[key];
            } else {
                element.value = data[key] || '';
            }
        }
    });
}
