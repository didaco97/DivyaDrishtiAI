// ===== VIDEO HANDLER =====
// Handles video streaming, processing, and display

class VideoHandler {
    constructor() {
        this.rawVideo = document.getElementById('rawFeed');
        this.aiCanvas = document.getElementById('aiCanvas');
        this.ctx = this.aiCanvas.getContext('2d');
        this.stream = null;
        this.isProcessing = false;
        this.detectionOverlay = document.getElementById('detectionOverlay');
        
        this.init();
    }

    async init() {
        try {
            await this.setupCamera();
            this.setupCanvas();
            this.hideVideoOverlay();
        } catch (error) {
            console.error('Failed to initialize video:', error);
            this.showVideoError('Camera access denied or not available');
        }
    }

    async setupCamera() {
        try {
            // Request camera access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    frameRate: { ideal: 30 }
                },
                audio: false
            });

            // Set video source
            this.rawVideo.srcObject = this.stream;
            
            // Wait for video to load
            await new Promise((resolve) => {
                this.rawVideo.onloadedmetadata = resolve;
            });

            console.log('Camera initialized successfully');
            
        } catch (error) {
            console.error('Camera setup failed:', error);
            // Fallback to demo video
            await this.loadDemoVideo();
        }
    }

    async loadDemoVideo() {
        // Load demo video for demonstration
        this.rawVideo.src = 'assets/demo-video.mp4';
        this.rawVideo.loop = true;
        this.rawVideo.muted = true;
        
        console.log('Demo video loaded');
    }

    setupCanvas() {
        // Set canvas dimensions to match video
        this.rawVideo.addEventListener('loadedmetadata', () => {
            this.aiCanvas.width = this.rawVideo.videoWidth;
            this.aiCanvas.height = this.rawVideo.videoHeight;
            
            // Set CSS dimensions for responsive display
            this.aiCanvas.style.width = '100%';
            this.aiCanvas.style.height = '100%';
            this.aiCanvas.style.objectFit = 'cover';
        });
    }

    startProcessing() {
        if (this.isProcessing) return;
        
        this.isProcessing = true;
        this.processFrame();
        console.log('Video processing started');
    }

    stopProcessing() {
        this.isProcessing = false;
        this.clearDetections();
        console.log('Video processing stopped');
    }

    processFrame() {
        if (!this.isProcessing) return;

        // Draw current video frame to canvas
        this.ctx.drawImage(
            this.rawVideo, 
            0, 0, 
            this.aiCanvas.width, 
            this.aiCanvas.height
        );

        // Simulate AI detection processing
        this.simulateDetections();

        // Continue processing
        requestAnimationFrame(() => this.processFrame());
    }

    simulateDetections() {
        // Clear previous detections
        this.clearDetections();

        // Simulate random detections for demo
        if (Math.random() > 0.7) { // 30% chance of detection
            const detection = this.generateRandomDetection();
            this.drawDetection(detection);
            this.addDetectionAlert(detection);
        }
    }

    generateRandomDetection() {
        const canvasRect = this.aiCanvas.getBoundingClientRect();
        
        return {
            id: Math.floor(Math.random() * 100),
            class: 'person',
            confidence: (Math.random() * 0.3 + 0.7).toFixed(2), // 70-100%
            bbox: {
                x: Math.random() * (canvasRect.width - 150),
                y: Math.random() * (canvasRect.height - 200),
                width: 100 + Math.random() * 50,
                height: 150 + Math.random() * 50
            },
            color: this.getRandomColor()
        };
    }

    drawDetection(detection) {
        // Create detection box element
        const detectionBox = document.createElement('div');
        detectionBox.className = 'detection-box new';
        detectionBox.style.cssText = `
            position: absolute;
            left: ${detection.bbox.x}px;
            top: ${detection.bbox.y}px;
            width: ${detection.bbox.width}px;
            height: ${detection.bbox.height}px;
            border: 2px solid ${detection.color};
            background: rgba(${this.hexToRgb(detection.color)}, 0.1);
            border-radius: 4px;
            pointer-events: none;
            z-index: 10;
        `;

        // Add detection label
        const label = document.createElement('div');
        label.className = 'detection-label';
        label.style.cssText = `
            position: absolute;
            top: -25px;
            left: 0;
            background: ${detection.color};
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        `;
        label.textContent = `PERSON ID:${detection.id} (${(detection.confidence * 100).toFixed(0)}%)`;

        detectionBox.appendChild(label);
        this.detectionOverlay.appendChild(detectionBox);

        // Remove 'new' class after animation
        setTimeout(() => {
            detectionBox.classList.remove('new');
        }, 600);

        // Auto-remove detection after 2 seconds
        setTimeout(() => {
            if (detectionBox.parentNode) {
                detectionBox.style.opacity = '0';
                setTimeout(() => {
                    if (detectionBox.parentNode) {
                        detectionBox.remove();
                    }
                }, 300);
            }
        }, 2000);
    }

    addDetectionAlert(detection) {
        const alertsContainer = document.getElementById('alertsContainer');
        
        // Create alert element
        const alert = document.createElement('div');
        alert.className = 'alert-item slide-in';
        alert.style.cssText = `
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: rgba(255, 82, 82, 0.1);
            border: 1px solid rgba(255, 82, 82, 0.3);
            border-radius: 8px;
            border-left: 4px solid #FF5252;
        `;

        const timestamp = new Date().toLocaleTimeString();
        alert.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                <i class="fas fa-exclamation-triangle" style="color: #FFA726;"></i>
                <span style="font-weight: 600; color: white;">${timestamp}</span>
            </div>
            <div style="font-size: 0.9rem; color: #E0E0E0;">
                Person detected in Sector Alpha-7
            </div>
            <div style="font-size: 0.8rem; color: #B0B0B0; margin-top: 0.25rem;">
                Confidence: ${(detection.confidence * 100).toFixed(0)}% | ID: ${detection.id}
            </div>
        `;

        // Add to container
        alertsContainer.insertBefore(alert, alertsContainer.firstChild);

        // Limit alerts to 5
        while (alertsContainer.children.length > 5) {
            alertsContainer.removeChild(alertsContainer.lastChild);
        }

        // Update alert count
        const alertCount = document.querySelector('.alert-count');
        alertCount.textContent = alertsContainer.children.length;
    }

    clearDetections() {
        // Clear all detection boxes
        this.detectionOverlay.innerHTML = '';
    }

    getRandomColor() {
        const colors = [
            '#00E5FF', // Teal
            '#39FF14', // Green
            '#FF5252', // Red
            '#FFA726', // Orange
            '#AB47BC', // Purple
            '#42A5F5', // Blue
            '#66BB6A', // Light Green
            '#FF7043'  // Deep Orange
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? 
            `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : 
            '255, 255, 255';
    }

    hideVideoOverlay() {
        const overlays = document.querySelectorAll('.video-overlay');
        overlays.forEach(overlay => {
            overlay.style.display = 'none';
        });
    }

    showVideoError(message) {
        const overlays = document.querySelectorAll('.video-overlay');
        overlays.forEach(overlay => {
            overlay.style.display = 'flex';
            overlay.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-exclamation-triangle" style="color: #FF5252;"></i>
                    <span>${message}</span>
                </div>
            `;
        });
    }

    captureScreenshot(type = 'ai') {
        let canvas, filename;
        
        if (type === 'raw') {
            // Create temporary canvas for raw video
            canvas = document.createElement('canvas');
            canvas.width = this.rawVideo.videoWidth;
            canvas.height = this.rawVideo.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(this.rawVideo, 0, 0);
            filename = 'divyadrishti-raw-feed.png';
        } else {
            // Use AI canvas with detections
            canvas = this.aiCanvas;
            filename = 'divyadrishti-ai-analysis.png';
        }

        // Convert to blob and download
        canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }, 'image/png');
    }

    toggleFullscreen(type) {
        const element = type === 'raw' ? 
            this.rawVideo.parentElement : 
            this.aiCanvas.parentElement;

        if (!document.fullscreenElement) {
            element.requestFullscreen().catch(err => {
                console.error('Fullscreen failed:', err);
            });
        } else {
            document.exitFullscreen();
        }
    }

    updateFPS() {
        // Calculate and update FPS
        const now = performance.now();
        if (this.lastFrameTime) {
            const fps = Math.round(1000 / (now - this.lastFrameTime));
            document.getElementById('fpsValue').textContent = fps;
        }
        this.lastFrameTime = now;
    }

    // Drone status simulation
    updateDroneStatus() {
        const statusItems = document.querySelectorAll('.status-value');
        
        // Simulate GPS coordinates with slight variations
        const baseLat = 32.79639;
        const baseLon = 74.87294;
        const latVariation = (Math.random() - 0.5) * 0.001;
        const lonVariation = (Math.random() - 0.5) * 0.001;
        
        if (statusItems[0]) {
            statusItems[0].textContent = 
                `${(baseLat + latVariation).toFixed(5)}N, ${(baseLon + lonVariation).toFixed(5)}E`;
        }

        // Simulate altitude variation
        if (statusItems[1]) {
            const altitude = 150 + Math.floor(Math.random() * 20 - 10);
            statusItems[1].textContent = `${altitude}m`;
        }

        // Update flight time
        if (statusItems[2]) {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            statusItems[2].textContent = `${hours}:${minutes}:${seconds}`;
        }

        // Simulate battery level
        if (statusItems[3]) {
            const battery = 78 + Math.floor(Math.random() * 5 - 2);
            statusItems[3].textContent = `${battery}%`;
            
            // Change color based on battery level
            if (battery < 20) {
                statusItems[3].style.color = '#FF5252';
            } else if (battery < 50) {
                statusItems[3].style.color = '#FFA726';
            } else {
                statusItems[3].style.color = '#39FF14';
            }
        }
    }

    destroy() {
        // Clean up resources
        this.stopProcessing();
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        
        this.clearDetections();
    }
}

// Initialize video handler when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.videoHandler = new VideoHandler();
    
    // Update drone status every 2 seconds
    setInterval(() => {
        if (window.videoHandler) {
            window.videoHandler.updateDroneStatus();
        }
    }, 2000);
});

// Add detection box styles
const detectionStyles = `
    .detection-box {
        transition: all 0.3s ease;
        animation: scaleIn 0.3s ease-out;
    }
    
    .detection-box.new {
        animation: bounce 0.6s ease-out;
    }
    
    .detection-label {
        font-family: 'JetBrains Mono', monospace;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
    
    .alert-item {
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;

// Inject detection styles
const detectionStyleSheet = document.createElement('style');
detectionStyleSheet.textContent = detectionStyles;
document.head.appendChild(detectionStyleSheet);
