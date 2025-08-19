// Main JavaScript functionality for the utility tools website

// Global utilities
class ToolsApp {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupTheme();
    }

    setupEventListeners() {
        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (mobileMenu && !mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });

        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupTheme() {
        // Add any theme-related functionality here
        // Could include dark mode toggle in the future
    }

    // Utility functions
    static copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            }).catch(() => {
                this.fallbackCopyToClipboard(text);
            });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    }

    static fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showNotification('Copied to clipboard!', 'success');
        } catch (err) {
            this.showNotification('Failed to copy to clipboard', 'error');
        }
        
        document.body.removeChild(textArea);
    }

    static showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());

        const notification = document.createElement('div');
        notification.className = `notification fixed top-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        // Set colors based on type
        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            warning: 'bg-yellow-500 text-white',
            info: 'bg-blue-500 text-white'
        };
        
        notification.className += ` ${colors[type] || colors.info}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    static async submitForm(formId, endpoint) {
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        const resultDiv = document.getElementById('result');
        
        if (!resultDiv) {
            console.error('Result div not found');
            return;
        }
        
        // Show loading state
        resultDiv.innerHTML = `
            <div class="bg-white border border-gray-200 rounded-lg p-8 shadow-sm">
                <div class="flex items-center justify-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                    <span class="ml-3 text-gray-600">Processing...</span>
                </div>
            </div>
        `;
        resultDiv.classList.remove('hidden');
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success !== false) {
                this.displayResult(data);
            } else {
                resultDiv.innerHTML = `
                    <div class="bg-red-50 border border-red-200 rounded-lg p-6">
                        <div class="flex items-center">
                            <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                            </svg>
                            <p class="text-red-800 font-medium">Error: ${data.result}</p>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            resultDiv.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-lg p-6">
                    <div class="flex items-center">
                        <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                        </svg>
                        <p class="text-red-800 font-medium">Network Error: ${error.message}</p>
                    </div>
                </div>
            `;
        }
    }

    static displayResult(data) {
        const resultDiv = document.getElementById('result');
        let html = '<div class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">';
        
        // Header
        html += `
            <div class="bg-green-50 border-b border-green-200 px-6 py-4">
                <div class="flex items-center">
                    <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    <h3 class="text-lg font-medium text-green-800">Results</h3>
                </div>
            </div>
        `;
        
        html += '<div class="p-6">';
        
        // Handle special cases for different data types
        if (data.qr_code) {
            // QR Code result
            html += `
                <div class="text-center mb-6">
                    <img src="${data.qr_code}" alt="QR Code" class="mx-auto border border-gray-300 rounded-lg">
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Original Text:</label>
                    <div class="flex items-center space-x-2">
                        <input readonly value="${data.text}" class="flex-1 p-3 border border-gray-300 rounded-lg bg-white">
                        <button onclick="ToolsApp.copyToClipboard('${data.text}');" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">Copy</button>
                    </div>
                </div>
            `;
        } else {
            // Regular results
            for (const [key, value] of Object.entries(data)) {
                if (key === 'success') continue;
                
                html += `<div class="mb-6 last:mb-0">`;
                html += `<label class="block text-sm font-medium text-gray-700 mb-2">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</label>`;
                
                if (typeof value === 'string' && value.length > 100) {
                    html += `<div class="relative">`;
                    html += `<textarea readonly class="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 font-mono text-sm result-box" rows="8">${this.escapeHtml(value)}</textarea>`;
                    html += `<button onclick="ToolsApp.copyToClipboard(\`${value.replace(/`/g, '\\`').replace(/\\/g, '\\\\')}\`);" class="absolute top-2 right-2 px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors">Copy</button>`;
                    html += `</div>`;
                } else if (typeof value === 'object' && value !== null) {
                    html += `<div class="relative">`;
                    html += `<pre class="w-full p-4 border border-gray-300 rounded-lg bg-gray-50 font-mono text-sm result-box overflow-x-auto">${this.escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
                    html += `<button onclick="ToolsApp.copyToClipboard(\`${JSON.stringify(value, null, 2).replace(/`/g, '\\`').replace(/\\/g, '\\\\')}\`);" class="absolute top-2 right-2 px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors">Copy</button>`;
                    html += `</div>`;
                } else {
                    html += `<div class="flex items-center space-x-2">`;
                    html += `<input readonly value="${this.escapeHtml(String(value))}" class="flex-1 p-3 border border-gray-300 rounded-lg bg-gray-50">`;
                    html += `<button onclick="ToolsApp.copyToClipboard('${String(value).replace(/'/g, "\\'")}');" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">Copy</button>`;
                    html += `</div>`;
                }
                html += `</div>`;
            }
        }
        
        html += '</div></div>';
        resultDiv.innerHTML = html;
    }

    static escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // File upload handler
    static handleFileUpload(inputId, callback) {
        const input = document.getElementById(inputId);
        const file = input.files[0];
        
        if (!file) {
            this.showNotification('Please select a file', 'warning');
            return;
        }
        
        // Check file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            this.showNotification('File size must be less than 10MB', 'error');
            return;
        }
        
        callback(file);
    }

    // Form validation
    static validateForm(formId) {
        const form = document.getElementById(formId);
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('border-red-500');
                isValid = false;
            } else {
                field.classList.remove('border-red-500');
            }
        });
        
        return isValid;
    }

    // Analytics (placeholder for future implementation)
    static trackToolUsage(toolName) {
        // In production, you'd send this to your analytics service
        console.log(`Tool used: ${toolName}`);
    }
}

// Advanced tool functions
class AdvancedTools {
    static async processImage(file, operation, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        
        Object.keys(options).forEach(key => {
            formData.append(key, options[key]);
        });
        
        try {
            const response = await fetch(`/api/image/${operation}`, {
                method: 'POST',
                body: formData
            });
            
            return await response.json();
        } catch (error) {
            throw new Error(`Image processing failed: ${error.message}`);
        }
    }

    static async analyzeWebsite(url) {
        const formData = new FormData();
        formData.append('url', url);
        
        try {
            const response = await fetch('/api/web/meta-analyzer', {
                method: 'POST',
                body: formData
            });
            
            return await response.json();
        } catch (error) {
            throw new Error(`Website analysis failed: ${error.message}`);
        }
    }

    static async processFile(file, operation) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`/api/file/${operation}`, {
                method: 'POST',
                body: formData
            });
            
            return await response.json();
        } catch (error) {
            throw new Error(`File processing failed: ${error.message}`);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ToolsApp();
});

// Make functions globally available
window.ToolsApp = ToolsApp;
window.AdvancedTools = AdvancedTools;

// Global functions for template usage
window.copyToClipboard = ToolsApp.copyToClipboard.bind(ToolsApp);
window.showNotification = ToolsApp.showNotification.bind(ToolsApp);
window.submitForm = ToolsApp.submitForm.bind(ToolsApp);
window.displayResult = ToolsApp.displayResult.bind(ToolsApp);