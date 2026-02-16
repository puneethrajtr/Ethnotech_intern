/**
 * Blog Platform JavaScript
 * Handles interactive functionality and user experience enhancements
 */

// Global application object
const BlogApp = {
    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupKeyboardNavigation();
        
        console.log('Blog Platform initialized successfully');
    },

    setupEventListeners() {
        // DOM content loaded
        document.addEventListener('DOMContentLoaded', () => {
            this.setupSearchDelayedInput();
            this.setupFormValidation();
            this.setupTooltips();
            this.setupScrollToTop();
        });

        // Window scroll events
        window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 100));
        
        // Window resize events
        window.addEventListener('resize', this.throttle(this.handleResize.bind(this), 250));
    },

    initializeComponents() {
        this.setupDeleteConfirmation();
        this.setupSearchEnhancements();
        this.setupCardHoverEffects();
        this.setupFormEnhancements();
        this.setupLoadingStates();
    },

    setupKeyboardNavigation() {
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.focusSearchInput();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeActiveModal();
            }
        });
    },

    /**
     * Delete Confirmation Functionality
     */
    setupDeleteConfirmation() {
        // Global function for delete confirmation (called from templates)
        window.confirmDelete = (postId, postTitle) => {
            const modal = document.getElementById('deleteConfirmModal');
            if (modal) {
                const titleElement = document.getElementById('postTitle');
                const linkElement = document.getElementById('deleteConfirmLink');
                
                if (titleElement && linkElement) {
                    titleElement.textContent = postTitle;
                    
                    // Update the delete link
                    const baseUrl = linkElement.href.replace(/\/admin\/delete\/\d+$/, '');
                    linkElement.href = `${window.location.origin}/admin/delete/${postId}`;
                    
                    // Show modal
                    const bsModal = new bootstrap.Modal(modal);
                    bsModal.show();
                }
            }
        };

        // Add confirmation for direct delete links
        document.addEventListener('click', (e) => {
            const deleteLink = e.target.closest('a[href*="/admin/delete/"]');
            if (deleteLink && !deleteLink.dataset.confirmed) {
                e.preventDefault();
                
                const confirmed = confirm('Are you sure you want to delete this post? This action cannot be undone.');
                if (confirmed) {
                    deleteLink.dataset.confirmed = 'true';
                    deleteLink.click();
                }
            }
        });
    },

    /**
     * Search Functionality Enhancements
     */
    setupSearchEnhancements() {
        const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
        
        searchInputs.forEach(input => {
            // Add search icon animation
            input.addEventListener('focus', () => {
                const icon = input.parentElement.querySelector('.fas.fa-search');
                if (icon) {
                    icon.style.color = '#0d6efd';
                }
            });

            input.addEventListener('blur', () => {
                const icon = input.parentElement.querySelector('.fas.fa-search');
                if (icon) {
                    icon.style.color = '';
                }
            });

            // Auto-submit search after delay
            input.addEventListener('input', this.debounce((e) => {
                const value = e.target.value.trim();
                if (value.length >= 3) {
                    this.performSearch(value);
                }
            }, 500));
        });
    },

    setupSearchDelayedInput() {
        const searchInput = document.querySelector('input[name="q"]');
        if (searchInput) {
            let searchTimeout;
            
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                const value = e.target.value.trim();
                
                // Show loading state
                this.showSearchLoading(true);
                
                searchTimeout = setTimeout(() => {
                    this.showSearchLoading(false);
                    
                    if (value.length >= 2) {
                        // Auto-search could be implemented here
                        console.log('Auto-search for:', value);
                    }
                }, 300);
            });
        }
    },

    performSearch(query) {
        // This could implement live search functionality
        console.log('Performing search for:', query);
        // In a real implementation, this might make an AJAX request
    },

    showSearchLoading(show) {
        const searchButton = document.querySelector('button[type="submit"] .fa-search');
        if (searchButton) {
            if (show) {
                searchButton.className = 'fas fa-spinner fa-spin';
            } else {
                searchButton.className = 'fas fa-search';
            }
        }
    },

    focusSearchInput() {
        const searchInput = document.querySelector('input[name="q"], input[type="search"]');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    },

    /**
     * Card Hover Effects
     */
    setupCardHoverEffects() {
        const cards = document.querySelectorAll('.blog-card, .card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.animateCard(card, 'hover');
            });
            
            card.addEventListener('mouseleave', () => {
                this.animateCard(card, 'normal');
            });
        });
    },

    animateCard(card, state) {
        if (state === 'hover') {
            card.style.transform = 'translateY(-4px)';
            card.style.transition = 'all 0.3s ease';
        } else {
            card.style.transform = 'translateY(0)';
        }
    },

    /**
     * Form Enhancements
     */
    setupFormEnhancements() {
        this.setupFormValidation();
        this.setupTextareaAutoResize();
        this.setupCharacterCount();
        this.setupFormSubmitLoading();
    },

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    this.showFormErrors(form);
                }
            });

            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        });
    },

    validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    },

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required';
        }
        
        // Specific field validations
        if (field.name === 'title' && value.length > 0 && value.length < 5) {
            isValid = false;
            errorMessage = 'Title must be at least 5 characters long';
        }
        
        if (field.name === 'content' && value.length > 0 && value.length < 50) {
            isValid = false;
            errorMessage = 'Content must be at least 50 characters long';
        }
        
        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    },

    showFieldValidation(field, isValid, errorMessage) {
        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        // Remove existing error message
        const existing = field.parentElement.querySelector('.invalid-feedback');
        if (existing) {
            existing.remove();
        }
        
        if (!isValid && errorMessage) {
            field.classList.add('is-invalid');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.textContent = errorMessage;
            field.parentElement.appendChild(errorDiv);
        } else if (field.value.trim()) {
            field.classList.add('is-valid');
        }
    },

    showFormErrors(form) {
        const firstError = form.querySelector('.is-invalid');
        if (firstError) {
            firstError.focus();
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    },

    setupTextareaAutoResize() {
        const textareas = document.querySelectorAll('textarea');
        
        textareas.forEach(textarea => {
            textarea.addEventListener('input', () => {
                this.autoResizeTextarea(textarea);
            });
            
            // Initial resize
            this.autoResizeTextarea(textarea);
        });
    },

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    },

    setupCharacterCount() {
        const contentField = document.getElementById('content');
        if (contentField) {
            contentField.addEventListener('input', () => {
                this.updateCharacterCount(contentField);
            });
            
            // Initial count
            this.updateCharacterCount(contentField);
        }
    },

    updateCharacterCount(field) {
        const content = field.value;
        const wordCount = content.trim() === '' ? 0 : content.trim().split(/\s+/).length;
        const charCount = content.length;
        
        const wordCountElement = document.getElementById('wordCount');
        const charCountElement = document.getElementById('charCount');
        
        if (wordCountElement) wordCountElement.textContent = wordCount;
        if (charCountElement) charCountElement.textContent = charCount;
    },

    setupFormSubmitLoading() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitButton = form.querySelector('button[type="submit"]');
                if (submitButton) {
                    this.showButtonLoading(submitButton, true);
                }
            });
        });
    },

    showButtonLoading(button, show) {
        if (show) {
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            button.disabled = true;
        } else {
            const originalText = button.dataset.originalText;
            if (originalText) {
                button.innerHTML = originalText;
            }
            button.disabled = false;
        }
    },

    /**
     * Loading States
     */
    setupLoadingStates() {
        // Show loading on navigation
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && !link.getAttribute('href').startsWith('#')) {
                this.showPageLoading();
            }
        });
    },

    showPageLoading() {
        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;
        document.body.appendChild(loader);
        
        // Remove after timeout (fallback)
        setTimeout(() => {
            if (loader.parentElement) {
                loader.remove();
            }
        }, 5000);
    },

    /**
     * Scroll Functionality
     */
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Show/hide scroll to top button
        this.toggleScrollToTopButton(scrollTop > 300);
        
        // Navbar shadow on scroll
        this.toggleNavbarShadow(scrollTop > 50);
    },

    toggleScrollToTopButton(show) {
        let button = document.getElementById('scrollToTop');
        
        if (show && !button) {
            button = document.createElement('button');
            button.id = 'scrollToTop';
            button.className = 'btn btn-primary position-fixed bottom-0 end-0 m-4';
            button.innerHTML = '<i class="fas fa-arrow-up"></i>';
            button.style.zIndex = '1050';
            button.addEventListener('click', this.scrollToTop);
            document.body.appendChild(button);
        } else if (!show && button) {
            button.remove();
        }
    },

    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    },

    setupScrollToTop() {
        // Initial check
        this.handleScroll();
    },

    toggleNavbarShadow(show) {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (show) {
                navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
            } else {
                navbar.style.boxShadow = '';
            }
        }
    },

    /**
     * Responsive Functionality
     */
    handleResize() {
        // Update mobile menu if needed
        this.updateMobileMenu();
    },

    updateMobileMenu() {
        const navbar = document.querySelector('.navbar-collapse');
        if (navbar && window.innerWidth > 768) {
            navbar.classList.remove('show');
        }
    },

    /**
     * Tooltips
     */
    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    /**
     * Modal Functionality
     */
    closeActiveModal() {
        const activeModal = document.querySelector('.modal.show');
        if (activeModal) {
            const bsModal = bootstrap.Modal.getInstance(activeModal);
            if (bsModal) {
                bsModal.hide();
            }
        }
    },

    /**
     * Utility Functions
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Notification System
     */
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        notification.style.zIndex = '1060';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
        
        return notification;
    },

    /**
     * Copy to Clipboard
     */
    copyToClipboard(text) {
        if (navigator.clipboard) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return Promise.resolve();
        }
    }
};

// Global functions for template use
window.sharePost = function(platform) {
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    
    let shareUrl = '';
    
    switch (platform) {
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?text=${title}&url=${url}`;
            break;
        case 'linkedin':
            shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
            break;
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
            break;
        default:
            console.warn('Unknown platform:', platform);
            return;
    }
    
    window.open(shareUrl, '_blank', 'width=600,height=400');
};

window.copyLink = function() {
    BlogApp.copyToClipboard(window.location.href)
        .then(() => {
            BlogApp.showNotification('Link copied to clipboard!', 'success', 2000);
        })
        .catch(() => {
            BlogApp.showNotification('Failed to copy link', 'danger', 3000);
        });
};

window.filterByCategory = function(category) {
    if (category) {
        const baseUrl = window.location.origin + window.location.pathname.split('/')[0];
        window.location.href = `${baseUrl}/category/${encodeURIComponent(category)}`;
    } else {
        const baseUrl = window.location.origin;
        window.location.href = baseUrl;
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    BlogApp.init();
});

// Export for module systems (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlogApp;
}