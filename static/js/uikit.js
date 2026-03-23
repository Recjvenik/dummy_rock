// ═══════════════════════════════════════════════════════════════
// AI LAB - UI/UX UTILITIES
// ═══════════════════════════════════════════════════════════════

const UIKit = {
    // Toast Notification System
    toast: {
        container: null,
        
        init() {
            if (!this.container) {
                this.container = document.createElement('div');
                this.container.className = 'toast-container';
                document.body.appendChild(this.container);
            }
        },
        
        show(message, type = 'info', duration = 4000) {
            this.init();
            
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            
            const icons = {
                success: '✓',
                error: '✕',
                info: 'ℹ',
                warning: '⚠'
            };
            
            toast.innerHTML = `
                <div class="toast-icon">${icons[type] || icons.info}</div>
                <div class="toast-content">
                    <div class="toast-message">${message}</div>
                </div>
            `;
            
            this.container.appendChild(toast);
            
            setTimeout(() => {
                toast.classList.add('toast-out');
                setTimeout(() => toast.remove(), 200);
            }, duration);
        },
        
        success(message, duration) {
            this.show(message, 'success', duration);
        },
        
        error(message, duration) {
            this.show(message, 'error', duration);
        },
        
        info(message, duration) {
            this.show(message, 'info', duration);
        }
    },
    
    // Progress Bar
    progress: {
        bar: null,
        
        init() {
            if (!this.bar) {
                this.bar = document.createElement('div');
                this.bar.className = 'progress-bar';
                this.bar.innerHTML = '<div class="progress-bar-fill"></div>';
                document.body.appendChild(this.bar);
            }
        },
        
        show() {
            this.init();
            this.bar.style.display = 'block';
        },
        
        hide() {
            if (this.bar) {
                this.bar.style.display = 'none';
            }
        },
        
        set(percent) {
            this.init();
            this.show();
            const fill = this.bar.querySelector('.progress-bar-fill');
            fill.style.width = `${percent}%`;
        },
        
        indeterminate() {
            this.init();
            this.show();
            this.bar.innerHTML = '<div class="progress-bar-indeterminate"></div>';
        }
    },
    
    // Modal System
    modal: {
        create(options = {}) {
            const overlay = document.createElement('div');
            overlay.className = 'modal-overlay';
            
            const modal = document.createElement('div');
            modal.className = 'modal';
            
            modal.innerHTML = `
                <div class="modal-header">
                    <div class="modal-title">${options.title || 'Modal'}</div>
                    <button class="modal-close" aria-label="Close">✕</button>
                </div>
                <div class="modal-body">
                    ${options.content || ''}
                </div>
                ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
            `;
            
            overlay.appendChild(modal);
            document.body.appendChild(overlay);
            
            const close = () => {
                overlay.style.animation = 'fade-out 0.2s ease';
                setTimeout(() => overlay.remove(), 200);
            };
            
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) close();
            });
            
            modal.querySelector('.modal-close').addEventListener('click', close);
            
            return { overlay, modal, close };
        }
    },
    
    // Loading Spinner
    spinner: {
        create() {
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            return spinner;
        }
    },
    
    // Smooth Scroll
    scrollTo(element, offset = 0) {
        const targetPosition = element.getBoundingClientRect().top + window.pageYOffset - offset;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    },
    
    // Debounce
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
    
    // Throttle
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Copy to Clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.toast.success('Copied to clipboard!');
            return true;
        } catch (err) {
            this.toast.error('Failed to copy');
            return false;
        }
    },
    
    // Lazy Load Images
    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    },
    
    // Animate on Scroll
    animateOnScroll() {
        const elements = document.querySelectorAll('[data-animate]');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        elements.forEach(el => observer.observe(el));
    }
};

// Auto-initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    UIKit.lazyLoadImages();
    UIKit.animateOnScroll();
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn-primary, .btn-green').forEach(btn => {
        btn.classList.add('btn-ripple');
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                UIKit.scrollTo(target, 80);
            }
        });
    });
});

// Page Load Progress
window.addEventListener('load', () => {
    UIKit.progress.hide();
});

// Export for use in other scripts
window.UIKit = UIKit;
