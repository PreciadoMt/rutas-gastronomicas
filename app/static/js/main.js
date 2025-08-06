// JavaScript principal para Rutas Gastronómicas

// Configuración global
const API_BASE_URL = '';
const STORAGE_KEYS = {
    USER_ID: 'user_id',
    USER_EMAIL: 'user_email',
    USER_NAME: 'user_name'
};

// Utilidades
const utils = {
    // Formatear fecha
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Formatear precio
    formatPrice: (price) => {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(price);
    },

    // Mostrar notificación
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    },

    // Validar formulario
    validateForm: (formId) => {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    },

    // Loading state
    setLoading: (element, isLoading) => {
        if (isLoading) {
            element.classList.add('loading');
            element.style.pointerEvents = 'none';
        } else {
            element.classList.remove('loading');
            element.style.pointerEvents = 'auto';
        }
    }
};

// API Service
const apiService = {
    // Hacer petición GET
    get: async (endpoint) => {
        try {
            const response = await fetch(API_BASE_URL + endpoint);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },

    // Hacer petición POST
    post: async (endpoint, data) => {
        try {
            const response = await fetch(API_BASE_URL + endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    },

    // Hacer petición PUT
    put: async (endpoint, data) => {
        try {
            const response = await fetch(API_BASE_URL + endpoint, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API PUT Error:', error);
            throw error;
        }
    },

    // Hacer petición DELETE
    delete: async (endpoint) => {
        try {
            const response = await fetch(API_BASE_URL + endpoint, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API DELETE Error:', error);
            throw error;
        }
    }
};

// Gestión de autenticación
const auth = {
    // Verificar si el usuario está logueado
    isLoggedIn: () => {
        return localStorage.getItem(STORAGE_KEYS.USER_ID) !== null;
    },

    // Obtener ID del usuario actual
    getCurrentUserId: () => {
        return localStorage.getItem(STORAGE_KEYS.USER_ID);
    },

    // Obtener datos del usuario actual
    getCurrentUser: () => {
        return {
            id: localStorage.getItem(STORAGE_KEYS.USER_ID),
            email: localStorage.getItem(STORAGE_KEYS.USER_EMAIL),
            name: localStorage.getItem(STORAGE_KEYS.USER_NAME)
        };
    },

    // Guardar datos de usuario
    setUser: (userData) => {
        localStorage.setItem(STORAGE_KEYS.USER_ID, userData.id);
        localStorage.setItem(STORAGE_KEYS.USER_EMAIL, userData.email);
        localStorage.setItem(STORAGE_KEYS.USER_NAME, userData.name);
    },

    // Cerrar sesión
    logout: () => {
        localStorage.removeItem(STORAGE_KEYS.USER_ID);
        localStorage.removeItem(STORAGE_KEYS.USER_EMAIL);
        localStorage.removeItem(STORAGE_KEYS.USER_NAME);
        window.location.href = '/';
    },

    // Redirigir si no está logueado
    requireAuth: () => {
        if (!auth.isLoggedIn()) {
            utils.showNotification('Debes iniciar sesión para acceder a esta página', 'warning');
            setTimeout(() => {
                window.location.href = '/users/auth/login';
            }, 2000);
            return false;
        }
        return true;
    }
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Actualizar navbar según estado de autenticación
    updateNavbar();
    
    // Agregar event listeners globales
    setupGlobalEventListeners();
    
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Agregar animaciones de entrada
    const elements = document.querySelectorAll('.card, .btn, .form-control');
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in-up');
    });
});

// Actualizar navbar
function updateNavbar() {
    const isLoggedIn = auth.isLoggedIn();
    const loginLink = document.querySelector('a[href="/users/auth/login"]');
    const registerLink = document.querySelector('a[href="/users/auth/register"]');
    const dashboardLink = document.querySelector('a[href="/dashboard"]');
    
    if (isLoggedIn) {
        const user = auth.getCurrentUser();
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        if (dashboardLink) {
            dashboardLink.style.display = 'block';
            dashboardLink.innerHTML = `<i class="fas fa-user me-1"></i>${user.name}`;
        }
        
        // Agregar botón de logout
        const navbar = document.querySelector('.navbar-nav');
        if (navbar && !document.getElementById('logoutBtn')) {
            const logoutLi = document.createElement('li');
            logoutLi.className = 'nav-item';
            logoutLi.innerHTML = `
                <a class="nav-link" href="#" id="logoutBtn" onclick="auth.logout()">
                    <i class="fas fa-sign-out-alt me-1"></i>Cerrar Sesión
                </a>
            `;
            navbar.appendChild(logoutLi);
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (registerLink) registerLink.style.display = 'block';
        if (dashboardLink) dashboardLink.style.display = 'none';
        
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) logoutBtn.parentElement.remove();
    }
}

// Event listeners globales
function setupGlobalEventListeners() {
    // Prevenir envío de formularios por defecto
    document.addEventListener('submit', function(e) {
        if (e.target.tagName === 'FORM') {
            e.preventDefault();
        }
    });
    
    // Smooth scroll para enlaces internos
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(e.target.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
    
    // Auto-hide alerts
    document.addEventListener('DOMContentLoaded', function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            setTimeout(() => {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) closeBtn.click();
            }, 5000);
        });
    });
}

// Funciones de utilidad para formularios
const formUtils = {
    // Resetear estilos de validación
    resetValidation: (formId) => {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('.is-invalid, .is-valid');
        inputs.forEach(input => {
            input.classList.remove('is-invalid', 'is-valid');
        });
    },

    // Mostrar error en campo específico
    showFieldError: (fieldId, message) => {
        const field = document.getElementById(fieldId);
        field.classList.add('is-invalid');
        
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    },

    // Validar email
    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Validar fecha futura
    validateFutureDate: (dateString) => {
        const date = new Date(dateString);
        const now = new Date();
        return date > now;
    }
};

// Exportar para uso global
window.utils = utils;
window.apiService = apiService;
window.auth = auth;
window.formUtils = formUtils;