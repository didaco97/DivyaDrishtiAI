// ===== DIVYADRISHTI WEB APPLICATION =====
// Main JavaScript file for DivyaDrishti Web Interface

class DivyaDrishtiApp {
    constructor() {
        this.isScanning = false;
        this.isTracking = false;
        this.currentModel = 'yolov11n';
        this.confidence = 75;
        this.fps = 0;
        this.detectionCount = 0;
        this.alerts = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeUI();
        this.startPerformanceMonitoring();
        this.showWelcomeMessage();
    }

    setupEventListeners() {
        // Start/Stop Surveillance Button
        const startStopBtn = document.getElementById('startStopBtn');
        startStopBtn.addEventListener('click', () => this.toggleSurveillance());

        // Model Selection
        const modelSelect = document.getElementById('modelSelect');
        modelSelect.addEventListener('change', (e) => this.changeModel(e.target.value));

        // Tracking Toggle
        const trackingToggle = document.getElementById('trackingToggle');
        trackingToggle.addEventListener('change', (e) => this.toggleTracking(e.target.checked));

        // Confidence Slider
        const confidenceSlider = document.getElementById('confidenceSlider');
        confidenceSlider.addEventListener('input', (e) => this.updateConfidence(e.target.value));

        // Quick Action Buttons
        document.getElementById('screenshotBtn').addEventListener('click', () => this.takeScreenshot());
        document.getElementById('recordBtn').addEventListener('click', () => this.toggleRecording());
        document.getElementById('mapBtn').addEventListener('click', () => this.openTacticalMap());

        // Video Controls
        document.getElementById('fullscreenRaw').addEventListener('click', () => this.toggleFullscreen('raw'));
        document.getElementById('fullscreenAI').addEventListener('click', () => this.toggleFullscreen('ai'));
        document.getElementById('captureRaw').addEventListener('click', () => this.captureFrame('raw'));
        document.getElementById('captureAI').addEventListener('click', () => this.captureFrame('ai'));

        // Emergency Stop
        document.getElementById('emergencyStop').addEventListener('click', () => this.emergencyStop());

        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => this.handleNavigation(e));
        });

        // Keyboard Shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    initializeUI() {
        // Set initial values
        document.getElementById('confidenceValue').textContent = `${this.confidence}%`;
        
        // Initialize video streams
        this.initializeVideoStreams();
        
        // Add ripple effect to buttons
        this.addRippleEffect();
        
        // Initialize tooltips
        this.initializeTooltips();
    }

    toggleSurveillance() {
        this.isScanning = !this.isScanning;
        const btn = document.getElementById('startStopBtn');
        const icon = btn.querySelector('i');
        const text = btn.querySelector('span');

        if (this.isScanning) {
            btn.classList.add('active');
            icon.className = 'fas fa-stop';
            text.textContent = 'STOP SCAN';
            this.startSurveillance();
            this.showToast('Surveillance Started', 'success');
        } else {
            btn.classList.remove('active');
            icon.className = 'fas fa-play';
            text.textContent = 'START SCAN';
            this.stopSurveillance();
            this.showToast('Surveillance Stopped', 'info');
        }
    }

    startSurveillance() {
        // Start video processing
        this.startVideoProcessing();
        
        // Update UI state
        this.updateSystemStatus('active');
        
        // Start FPS counter
        this.startFPSCounter();
        
        // Add scanning animation to video panels
        document.querySelectorAll('.video-panel').forEach(panel => {
            panel.classList.add('glow-border');
        });
    }

    stopSurveillance() {
        // Stop video processing
        this.stopVideoProcessing();
        
        // Update UI state
        this.updateSystemStatus('idle');
        
        // Stop FPS counter
        this.stopFPSCounter();
        
        // Remove scanning animation
        document.querySelectorAll('.video-panel').forEach(panel => {
            panel.classList.remove('glow-border');
        });
    }

    toggleTracking(enabled) {
        this.isTracking = enabled;
        const status = document.querySelector('.toggle-status');
        status.textContent = enabled ? 'ON' : 'OFF';
        status.style.color = enabled ? 'var(--accent-green)' : 'var(--text-muted)';
        
        this.showToast(`Tracking ${enabled ? 'Enabled' : 'Disabled'}`, 'info');
    }

    changeModel(modelValue) {
        this.currentModel = modelValue;
        
        // Update model stats based on selection
        const stats = this.getModelStats(modelValue);
        this.updateModelStats(stats);
        
        this.showToast(`Switched to ${stats.name}`, 'success');
        
        // Add loading animation
        this.showModelLoading();
    }

    getModelStats(model) {
        const modelData = {
            'yolov11n': { name: 'YOLOv11n', performance: 'High', accuracy: '94.2%' },
            'yolov11s': { name: 'YOLOv11s', performance: 'High', accuracy: '96.1%' },
            'yolov11m': { name: 'YOLOv11m', performance: 'Medium', accuracy: '97.8%' },
            'foottrail': { name: 'FootTrail', performance: 'Medium', accuracy: '92.5%' }
        };
        return modelData[model] || modelData['yolov11n'];
    }

    updateModelStats(stats) {
        const performanceEl = document.querySelector('.performance-high');
        const accuracyEl = document.querySelector('.stat-value:last-child');
        
        performanceEl.textContent = stats.performance;
        accuracyEl.textContent = stats.accuracy;
        
        // Update performance color
        performanceEl.className = `stat-value performance-${stats.performance.toLowerCase()}`;
    }

    updateConfidence(value) {
        this.confidence = value;
        document.getElementById('confidenceValue').textContent = `${value}%`;
        
        // Update slider fill effect
        const slider = document.getElementById('confidenceSlider');
        const percentage = ((value - slider.min) / (slider.max - slider.min)) * 100;
        slider.style.background = `linear-gradient(90deg, var(--accent-teal) ${percentage}%, rgba(255,255,255,0.2) ${percentage}%)`;
    }

    takeScreenshot() {
        // Simulate screenshot capture
        this.showToast('Screenshot Captured', 'success');
        
        // Add flash effect
        this.addFlashEffect();
        
        // Update screenshot counter (if exists)
        this.updateScreenshotCounter();
    }

    toggleRecording() {
        // Toggle recording state
        const btn = document.getElementById('recordBtn');
        const isRecording = btn.classList.toggle('recording');
        
        if (isRecording) {
            btn.style.color = 'var(--danger)';
            btn.querySelector('i').className = 'fas fa-stop-circle';
            this.showToast('Recording Started', 'success');
        } else {
            btn.style.color = '';
            btn.querySelector('i').className = 'fas fa-video';
            this.showToast('Recording Stopped', 'info');
        }
    }

    openTacticalMap() {
        // Open tactical map in new window/modal
        this.showToast('Opening Tactical Map...', 'info');
        
        // Simulate map opening
        setTimeout(() => {
            window.open('tactical-map.html', '_blank', 'width=1200,height=800');
        }, 500);
    }

    emergencyStop() {
        // Emergency stop all operations
        this.isScanning = false;
        this.isTracking = false;
        
        // Reset UI
        this.resetUI();
        
        // Show emergency alert
        this.showToast('EMERGENCY STOP ACTIVATED', 'error');
        
        // Add shake animation to emergency button
        document.getElementById('emergencyStop').classList.add('shake');
        setTimeout(() => {
            document.getElementById('emergencyStop').classList.remove('shake');
        }, 500);
    }

    handleNavigation(e) {
        e.preventDefault();
        
        // Remove active class from all nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        // Add active class to clicked link
        e.target.closest('.nav-link').classList.add('active');
        
        // Handle navigation logic here
        const href = e.target.closest('.nav-link').getAttribute('href');
        this.showToast(`Navigating to ${href.replace('#', '')}...`, 'info');
    }

    handleKeyboardShortcuts(e) {
        // Prevent shortcuts when typing in inputs
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
        
        switch(e.key.toLowerCase()) {
            case ' ':
                e.preventDefault();
                this.toggleSurveillance();
                break;
            case 's':
                e.preventDefault();
                this.takeScreenshot();
                break;
            case 't':
                e.preventDefault();
                document.getElementById('trackingToggle').click();
                break;
            case 'f':
                e.preventDefault();
                this.toggleFullscreen('ai');
                break;
            case 'escape':
                this.emergencyStop();
                break;
        }
    }

    startPerformanceMonitoring() {
        // Monitor system performance
        setInterval(() => {
            this.updatePerformanceMetrics();
        }, 1000);
    }

    updatePerformanceMetrics() {
        // Simulate performance data
        const metrics = {
            fps: Math.floor(Math.random() * 10) + 20, // 20-30 FPS
            gpu: Math.floor(Math.random() * 20) + 50, // 50-70%
            memory: (Math.random() * 2 + 3).toFixed(1) // 3-5 GB
        };

        // Update FPS counter
        document.getElementById('fpsValue').textContent = metrics.fps;
        
        // Update performance bars
        this.updateMetricBar('gpu', metrics.gpu);
        this.updateMetricBar('memory', (metrics.memory / 8) * 100); // Assuming 8GB max
        
        // Update processing speed bar
        const speedPercentage = (metrics.fps / 30) * 100;
        this.updateMetricBar('speed', speedPercentage);
    }

    updateMetricBar(type, percentage) {
        const bars = document.querySelectorAll('.metric-fill');
        bars.forEach((bar, index) => {
            if (index === 0 && type === 'speed') {
                bar.style.width = `${percentage}%`;
                bar.parentElement.nextElementSibling.textContent = `${Math.floor((percentage / 100) * 30)} FPS`;
            } else if (index === 1 && type === 'gpu') {
                bar.style.width = `${percentage}%`;
                bar.parentElement.nextElementSibling.textContent = `${Math.floor(percentage)}%`;
            } else if (index === 2 && type === 'memory') {
                bar.style.width = `${percentage}%`;
                const memoryGB = ((percentage / 100) * 8).toFixed(1);
                bar.parentElement.nextElementSibling.textContent = `${memoryGB}GB`;
            }
        });
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type} toast-enter`;
        
        const icon = this.getToastIcon(type);
        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;
        
        document.getElementById('toastContainer').appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.classList.add('toast-exit');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    getToastIcon(type) {
        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        return icons[type] || icons['info'];
    }

    addRippleEffect() {
        document.querySelectorAll('.primary-button, .action-btn').forEach(button => {
            button.classList.add('btn-ripple');
        });
    }

    showWelcomeMessage() {
        setTimeout(() => {
            this.showToast('DivyaDrishti Web Interface Ready', 'success');
        }, 1000);
    }

    // Additional utility methods
    initializeVideoStreams() {
        // Initialize video stream connections
        console.log('Initializing video streams...');
    }

    startVideoProcessing() {
        // Start AI video processing
        console.log('Starting video processing...');
    }

    stopVideoProcessing() {
        // Stop AI video processing
        console.log('Stopping video processing...');
    }

    updateSystemStatus(status) {
        // Update system status indicators
        const statusDot = document.querySelector('.status-dot');
        statusDot.className = `status-dot ${status === 'active' ? 'online' : 'offline'}`;
    }

    startFPSCounter() {
        // Start FPS monitoring
        console.log('Starting FPS counter...');
    }

    stopFPSCounter() {
        // Stop FPS monitoring
        console.log('Stopping FPS counter...');
    }

    showModelLoading() {
        // Show model loading animation
        console.log('Loading model...');
    }

    addFlashEffect() {
        // Add camera flash effect
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: white;
            opacity: 0.8;
            z-index: 9999;
            pointer-events: none;
        `;
        document.body.appendChild(flash);
        
        setTimeout(() => {
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 200);
        }, 100);
    }

    updateScreenshotCounter() {
        // Update screenshot counter if exists
        console.log('Screenshot captured');
    }

    resetUI() {
        // Reset all UI elements to default state
        const startStopBtn = document.getElementById('startStopBtn');
        startStopBtn.classList.remove('active');
        startStopBtn.querySelector('i').className = 'fas fa-play';
        startStopBtn.querySelector('span').textContent = 'START SCAN';
        
        document.getElementById('trackingToggle').checked = false;
        document.querySelector('.toggle-status').textContent = 'OFF';
    }

    toggleFullscreen(type) {
        // Toggle fullscreen for video panels
        console.log(`Toggling fullscreen for ${type} panel`);
    }

    captureFrame(type) {
        // Capture frame from specific video panel
        console.log(`Capturing frame from ${type} panel`);
        this.addFlashEffect();
    }

    initializeTooltips() {
        // Initialize tooltips for UI elements
        console.log('Initializing tooltips...');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.divyaDrishtiApp = new DivyaDrishtiApp();
});

// Add CSS for toast notifications
const toastStyles = `
    .toast {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
        min-width: 250px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .toast-success { border-left: 4px solid var(--accent-green); }
    .toast-error { border-left: 4px solid var(--danger); }
    .toast-warning { border-left: 4px solid var(--warning); }
    .toast-info { border-left: 4px solid var(--accent-teal); }
`;

// Inject toast styles
const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);
