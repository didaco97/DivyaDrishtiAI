// ===== ANIMATIONS CONTROLLER =====
// Handles all UI animations and effects

class AnimationsController {
    constructor() {
        this.animationQueue = [];
        this.isAnimating = false;
        this.observers = new Map();
        
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.setupAnimationEvents();
        this.initializePageAnimations();
        console.log('Animations controller initialized');
    }

    setupIntersectionObserver() {
        // Create intersection observer for scroll animations
        this.intersectionObserver = new IntersectionObserver(
            (entries) => this.handleIntersection(entries),
            {
                threshold: 0.1,
                rootMargin: '50px'
            }
        );

        // Observe all animatable elements
        document.querySelectorAll('[data-animate]').forEach(el => {
            this.intersectionObserver.observe(el);
        });
    }

    handleIntersection(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const animationType = element.dataset.animate;
                this.triggerAnimation(element, animationType);
                this.intersectionObserver.unobserve(element);
            }
        });
    }

    setupAnimationEvents() {
        // Listen for custom animation events
        document.addEventListener('triggerAnimation', (e) => {
            this.handleCustomAnimation(e.detail);
        });

        document.addEventListener('newDetection', (e) => {
            this.animateNewDetection(e.detail);
        });

        document.addEventListener('securityAlert', (e) => {
            this.animateSecurityAlert(e.detail);
        });

        document.addEventListener('modelLoading', (e) => {
            this.animateModelLoading(e.detail.loading);
        });
    }

    initializePageAnimations() {
        // Animate page load
        this.animatePageLoad();
        
        // Add hover effects to interactive elements
        this.setupHoverEffects();
        
        // Initialize particle effects
        this.initializeParticleEffects();
    }

    animatePageLoad() {
        // Staggered animation for main panels
        const panels = document.querySelectorAll('.panel-enter');
        panels.forEach((panel, index) => {
            panel.style.setProperty('--index', index);
            panel.classList.add('animate');
        });

        // Animate header
        const header = document.querySelector('.header');
        if (header) {
            header.style.transform = 'translateY(-100%)';
            header.style.opacity = '0';
            
            setTimeout(() => {
                header.style.transition = 'all 0.6s ease-out';
                header.style.transform = 'translateY(0)';
                header.style.opacity = '1';
            }, 200);
        }

        // Animate floating action button
        const fab = document.querySelector('.fab');
        if (fab) {
            fab.style.transform = 'scale(0) rotate(180deg)';
            setTimeout(() => {
                fab.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                fab.style.transform = 'scale(1) rotate(0deg)';
            }, 1000);
        }
    }

    setupHoverEffects() {
        // Add hover effects to cards
        document.querySelectorAll('.glass-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                this.animateCardHover(card, true);
            });
            
            card.addEventListener('mouseleave', () => {
                this.animateCardHover(card, false);
            });
        });

        // Add hover effects to buttons
        document.querySelectorAll('.primary-button, .action-btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                this.animateButtonHover(btn, true);
            });
            
            btn.addEventListener('mouseleave', () => {
                this.animateButtonHover(btn, false);
            });
        });

        // Add click ripple effect
        document.querySelectorAll('.btn-ripple').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.createRippleEffect(e);
            });
        });
    }

    animateCardHover(card, isHover) {
        if (isHover) {
            card.style.transform = 'translateY(-5px) scale(1.02)';
            card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3), 0 0 30px rgba(0, 229, 255, 0.2)';
        } else {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
        }
    }

    animateButtonHover(button, isHover) {
        if (isHover) {
            button.style.transform = 'translateY(-2px) scale(1.05)';
            button.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.3), 0 0 20px rgba(0, 229, 255, 0.4)';
        } else {
            button.style.transform = 'translateY(0) scale(1)';
            button.style.boxShadow = '';
        }
    }

    createRippleEffect(event) {
        const button = event.currentTarget;
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
            z-index: 1;
        `;

        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    }

    animateNewDetection(detection) {
        // Create detection notification animation
        const notification = this.createDetectionNotification(detection);
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 100);

        // Animate out
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 3000);

        // Pulse effect on detection counter
        this.pulseElement(document.querySelector('.alert-count'));
    }

    createDetectionNotification(detection) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 120px;
            right: 20px;
            background: rgba(255, 82, 82, 0.9);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #FF5252;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1001;
            min-width: 250px;
            backdrop-filter: blur(10px);
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Detection Alert</strong>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                ${detection.class} detected with ${(detection.confidence * 100).toFixed(0)}% confidence
            </div>
        `;

        return notification;
    }

    animateSecurityAlert(alertData) {
        // Flash effect for critical alerts
        if (alertData.severity === 'critical') {
            this.createFlashEffect('#FF5252');
        }

        // Shake emergency button
        const emergencyBtn = document.getElementById('emergencyStop');
        if (emergencyBtn) {
            emergencyBtn.classList.add('shake');
            setTimeout(() => emergencyBtn.classList.remove('shake'), 500);
        }

        // Pulse status indicator
        const statusDot = document.querySelector('.status-dot');
        if (statusDot) {
            statusDot.style.animation = 'pulse 0.5s ease-in-out 3';
        }
    }

    animateModelLoading(isLoading) {
        const modelSelect = document.getElementById('modelSelect');
        const dropdown = modelSelect.parentElement;

        if (isLoading) {
            // Add loading spinner
            const spinner = document.createElement('div');
            spinner.className = 'model-loading-spinner';
            spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            spinner.style.cssText = `
                position: absolute;
                right: 30px;
                top: 50%;
                transform: translateY(-50%);
                color: var(--accent-teal);
                z-index: 10;
            `;
            dropdown.appendChild(spinner);

            // Disable dropdown
            modelSelect.disabled = true;
            modelSelect.style.opacity = '0.6';
        } else {
            // Remove loading spinner
            const spinner = dropdown.querySelector('.model-loading-spinner');
            if (spinner) spinner.remove();

            // Enable dropdown
            modelSelect.disabled = false;
            modelSelect.style.opacity = '1';

            // Success animation
            this.createSuccessEffect(dropdown);
        }
    }

    createFlashEffect(color = '#FFFFFF') {
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${color};
            opacity: 0;
            z-index: 9999;
            pointer-events: none;
            animation: flash 0.3s ease-out;
        `;

        document.body.appendChild(flash);
        setTimeout(() => flash.remove(), 300);
    }

    createSuccessEffect(element) {
        const checkmark = document.createElement('div');
        checkmark.innerHTML = '<i class="fas fa-check"></i>';
        checkmark.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%) scale(0);
            color: var(--accent-green);
            font-size: 1.2rem;
            animation: successPop 0.6s ease-out;
            z-index: 10;
        `;

        element.style.position = 'relative';
        element.appendChild(checkmark);

        setTimeout(() => checkmark.remove(), 600);
    }

    pulseElement(element) {
        if (!element) return;
        
        element.style.animation = 'pulse 0.6s ease-out';
        setTimeout(() => {
            element.style.animation = '';
        }, 600);
    }

    initializeParticleEffects() {
        // Create subtle particle background
        this.createParticleBackground();
    }

    createParticleBackground() {
        const particleContainer = document.createElement('div');
        particleContainer.className = 'particle-background';
        particleContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        `;

        // Create particles
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 2px;
                height: 2px;
                background: rgba(0, 229, 255, 0.3);
                border-radius: 50%;
                animation: float ${5 + Math.random() * 10}s linear infinite;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation-delay: ${Math.random() * 5}s;
            `;
            particleContainer.appendChild(particle);
        }

        document.body.appendChild(particleContainer);
    }

    // Utility animation methods
    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.opacity = '1';
        }, 10);
    }

    fadeOut(element, duration = 300) {
        element.style.transition = `opacity ${duration}ms ease`;
        element.style.opacity = '0';
        
        return new Promise(resolve => {
            setTimeout(resolve, duration);
        });
    }

    slideIn(element, direction = 'right', duration = 300) {
        const transforms = {
            'right': 'translateX(100%)',
            'left': 'translateX(-100%)',
            'up': 'translateY(-100%)',
            'down': 'translateY(100%)'
        };

        element.style.transform = transforms[direction];
        element.style.transition = `transform ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.transform = 'translate(0, 0)';
        }, 10);
    }

    bounce(element, intensity = 1) {
        element.style.animation = `bounce ${0.6 * intensity}s ease-out`;
        setTimeout(() => {
            element.style.animation = '';
        }, 600 * intensity);
    }

    shake(element, intensity = 1) {
        element.style.animation = `shake ${0.5 * intensity}s ease-out`;
        setTimeout(() => {
            element.style.animation = '';
        }, 500 * intensity);
    }

    glow(element, color = 'var(--accent-teal)', duration = 1000) {
        const originalBoxShadow = element.style.boxShadow;
        element.style.transition = `box-shadow ${duration}ms ease`;
        element.style.boxShadow = `0 0 20px ${color}`;
        
        setTimeout(() => {
            element.style.boxShadow = originalBoxShadow;
        }, duration);
    }

    // Performance monitoring
    measureAnimationPerformance(animationName, callback) {
        const start = performance.now();
        
        callback();
        
        const end = performance.now();
        console.log(`Animation "${animationName}" took ${end - start} milliseconds`);
    }

    // Cleanup
    destroy() {
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
        
        // Remove particle background
        const particleBackground = document.querySelector('.particle-background');
        if (particleBackground) {
            particleBackground.remove();
        }
        
        console.log('Animations controller destroyed');
    }
}

// Initialize animations controller
document.addEventListener('DOMContentLoaded', () => {
    window.animationsController = new AnimationsController();
});

// Add animation keyframes to CSS
const animationKeyframes = `
    @keyframes flash {
        0% { opacity: 0; }
        50% { opacity: 0.8; }
        100% { opacity: 0; }
    }
    
    @keyframes successPop {
        0% { transform: translateY(-50%) scale(0); }
        50% { transform: translateY(-50%) scale(1.2); }
        100% { transform: translateY(-50%) scale(1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;

// Inject animation keyframes
const animationStyleSheet = document.createElement('style');
animationStyleSheet.textContent = animationKeyframes;
document.head.appendChild(animationStyleSheet);

// Export for global access
window.AnimationsController = AnimationsController;
