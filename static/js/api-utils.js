/**
 * API Utility Functions
 * Provides consistent error handling for API calls
 */

const API_BASE = '/api';

/**
 * Make an API request with error handling
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${url}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include'
        });
        
        let data;
        try {
            data = await response.json();
        } catch (e) {
            // If response is not JSON, return text
            const text = await response.text();
            throw new Error(text || 'Invalid response from server');
        }
        
        if (!response.ok) {
            // Handle error response
            const errorMessage = data.error || data.message || data.detail || 'An error occurred';
            throw new Error(errorMessage);
        }
        
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

/**
 * Show error message to user
 */
function showError(message) {
    // Try to use Bootstrap alert if available, otherwise use alert
    if (typeof bootstrap !== 'undefined') {
        // Create and show Bootstrap alert
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.insertBefore(alertDiv, document.body.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    } else {
        alert(message);
    }
}

/**
 * Show success message to user
 */
function showSuccess(message) {
    if (typeof bootstrap !== 'undefined') {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-success alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.insertBefore(alertDiv, document.body.firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    } else {
        alert(message);
    }
}

