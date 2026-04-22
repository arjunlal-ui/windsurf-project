// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('mobile-open');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.navbar')) {
            navMenu.classList.remove('mobile-open');
        }
    });
});

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Smooth scroll for anchor links
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

// Form validation enhancements
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            // Show error message
            const firstError = form.querySelector('.error');
            if (firstError) {
                firstError.focus();
            }
        }
    });
});

// Remove error class on input
document.querySelectorAll('input, textarea, select').forEach(field => {
    field.addEventListener('input', function() {
        this.classList.remove('error');
    });
});

// Loading states for forms (applied on form submit, not button click)
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const btn = this.querySelector('.btn[type="submit"]');
        if (btn && !btn.classList.contains('loading')) {
            // Use setTimeout so the form submits before we disable the button
            setTimeout(function() {
                btn.classList.add('loading');
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            }, 50);
        }
    });
});

// Dynamic time updates
function updateTimes() {
    const timeElements = document.querySelectorAll('[data-time]');
    timeElements.forEach(element => {
        const timeString = element.getAttribute('data-time');
        if (timeString) {
            const time = new Date(timeString);
            const now = new Date();
            const diff = now - time;
            
            if (diff < 60000) { // Less than 1 minute
                element.textContent = 'Just now';
            } else if (diff < 3600000) { // Less than 1 hour
                element.textContent = Math.floor(diff / 60000) + ' minutes ago';
            } else if (diff < 86400000) { // Less than 1 day
                element.textContent = Math.floor(diff / 3600000) + ' hours ago';
            } else {
                element.textContent = Math.floor(diff / 86400000) + ' days ago';
            }
        }
    });
}

// Update times every minute
setInterval(updateTimes, 60000);
updateTimes();

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.event-card, .day-column, .stat-item').forEach(el => {
    observer.observe(el);
});

// Add animation classes
const style = document.createElement('style');
style.textContent = `
    .event-card, .day-column, .stat-item {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    .mobile-open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--bg-secondary);
        border-top: 1px solid var(--border-color);
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .error {
        border-color: var(--accent-red) !important;
        box-shadow: 0 0 0 2px rgba(255, 92, 92, 0.2) !important;
    }
    
    .loading {
        opacity: 0.7;
        cursor: not-allowed;
    }
`;
document.head.appendChild(style);
