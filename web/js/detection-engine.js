// ===== DETECTION ENGINE =====
// Handles AI detection logic and tracking

class DetectionEngine {
    constructor() {
        this.isActive = false;
        this.trackingEnabled = false;
        this.currentModel = 'yolov11n';
        this.confidence = 0.75;
        this.detectedObjects = new Map();
        this.trackingId = 1;
        this.detectionHistory = [];
        this.performanceMetrics = {
            fps: 0,
            processingTime: 0,
            detectionCount: 0
        };
        
        this.init();
    }

    init() {
        console.log('Detection Engine initialized');
        this.setupPerformanceMonitoring();
    }

    start() {
        this.isActive = true;
        this.startDetectionLoop();
        console.log('Detection engine started');
    }

    stop() {
        this.isActive = false;
        this.clearAllDetections();
        console.log('Detection engine stopped');
    }

    setModel(modelName) {
        this.currentModel = modelName;
        console.log(`Switched to model: ${modelName}`);
        
        // Simulate model loading time
        this.showModelLoading();
        
        setTimeout(() => {
            this.hideModelLoading();
            this.updateModelPerformance(modelName);
        }, 2000);
    }

    setConfidence(confidence) {
        this.confidence = confidence / 100; // Convert percentage to decimal
        console.log(`Confidence threshold set to: ${confidence}%`);
    }

    enableTracking(enabled) {
        this.trackingEnabled = enabled;
        console.log(`Tracking ${enabled ? 'enabled' : 'disabled'}`);
        
        if (!enabled) {
            this.clearTrackingData();
        }
    }

    startDetectionLoop() {
        if (!this.isActive) return;

        const startTime = performance.now();
        
        // Simulate AI detection processing
        this.processFrame();
        
        const endTime = performance.now();
        this.performanceMetrics.processingTime = endTime - startTime;
        
        // Continue loop
        requestAnimationFrame(() => this.startDetectionLoop());
    }

    processFrame() {
        // Simulate detection results based on current model
        const detections = this.simulateDetections();
        
        // Process each detection
        detections.forEach(detection => {
            if (detection.confidence >= this.confidence) {
                this.handleDetection(detection);
            }
        });

        // Update performance metrics
        this.updatePerformanceMetrics();
    }

    simulateDetections() {
        const detections = [];
        const modelConfig = this.getModelConfig(this.currentModel);
        
        // Random number of detections based on model
        const numDetections = Math.random() > 0.8 ? 
            Math.floor(Math.random() * modelConfig.maxDetections) + 1 : 0;

        for (let i = 0; i < numDetections; i++) {
            detections.push(this.generateDetection(modelConfig));
        }

        return detections;
    }

    getModelConfig(modelName) {
        const configs = {
            'yolov11n': {
                classes: ['person', 'vehicle'],
                accuracy: 0.94,
                speed: 'fast',
                maxDetections: 3
            },
            'yolov11s': {
                classes: ['person', 'vehicle', 'animal'],
                accuracy: 0.96,
                speed: 'medium',
                maxDetections: 4
            },
            'yolov11m': {
                classes: ['person', 'vehicle', 'animal', 'object'],
                accuracy: 0.98,
                speed: 'slow',
                maxDetections: 5
            },
            'foottrail': {
                classes: ['person', 'unauthorized-trail', 'vegetation', 'structure'],
                accuracy: 0.92,
                speed: 'medium',
                maxDetections: 2
            }
        };
        
        return configs[modelName] || configs['yolov11n'];
    }

    generateDetection(config) {
        const classIndex = Math.floor(Math.random() * config.classes.length);
        const className = config.classes[classIndex];
        
        return {
            class: className,
            confidence: Math.random() * (1 - this.confidence) + this.confidence,
            bbox: this.generateBoundingBox(),
            timestamp: Date.now(),
            id: this.trackingEnabled ? this.getTrackingId(className) : null
        };
    }

    generateBoundingBox() {
        // Generate realistic bounding box coordinates
        const canvasWidth = 1280; // Assuming HD resolution
        const canvasHeight = 720;
        
        const width = Math.random() * 200 + 80; // 80-280px width
        const height = Math.random() * 300 + 120; // 120-420px height
        const x = Math.random() * (canvasWidth - width);
        const y = Math.random() * (canvasHeight - height);
        
        return { x, y, width, height };
    }

    getTrackingId(className) {
        // Simple tracking ID assignment
        if (this.trackingEnabled) {
            // In a real implementation, this would use sophisticated tracking algorithms
            return this.trackingId++;
        }
        return null;
    }

    handleDetection(detection) {
        // Store detection
        this.storeDetection(detection);
        
        // Update UI
        this.updateDetectionDisplay(detection);
        
        // Log detection event
        this.logDetectionEvent(detection);
        
        // Check for alerts
        this.checkAlerts(detection);
    }

    storeDetection(detection) {
        const key = `${detection.class}_${detection.id || Date.now()}`;
        this.detectedObjects.set(key, detection);
        
        // Add to history
        this.detectionHistory.push({
            ...detection,
            timestamp: new Date().toISOString()
        });
        
        // Limit history size
        if (this.detectionHistory.length > 100) {
            this.detectionHistory.shift();
        }
    }

    updateDetectionDisplay(detection) {
        // This would integrate with the video handler to display detections
        if (window.videoHandler) {
            // Trigger detection visualization
            const event = new CustomEvent('newDetection', { detail: detection });
            document.dispatchEvent(event);
        }
    }

    logDetectionEvent(detection) {
        const logEntry = {
            timestamp: new Date().toLocaleTimeString(),
            class: detection.class,
            confidence: (detection.confidence * 100).toFixed(1),
            id: detection.id,
            model: this.currentModel
        };
        
        console.log('Detection:', logEntry);
    }

    checkAlerts(detection) {
        // Define alert conditions
        const alertConditions = {
            'person': detection.confidence > 0.8,
            'unauthorized-trail': detection.confidence > 0.7,
            'vehicle': detection.confidence > 0.85
        };
        
        if (alertConditions[detection.class]) {
            this.triggerAlert(detection);
        }
    }

    triggerAlert(detection) {
        const alertData = {
            type: 'detection',
            class: detection.class,
            confidence: detection.confidence,
            timestamp: new Date(),
            severity: this.getAlertSeverity(detection)
        };
        
        // Dispatch alert event
        const event = new CustomEvent('securityAlert', { detail: alertData });
        document.dispatchEvent(event);
    }

    getAlertSeverity(detection) {
        const severityMap = {
            'person': 'high',
            'unauthorized-trail': 'critical',
            'vehicle': 'medium',
            'animal': 'low'
        };
        
        return severityMap[detection.class] || 'medium';
    }

    updatePerformanceMetrics() {
        // Calculate FPS
        const now = performance.now();
        if (this.lastFrameTime) {
            const frameDelta = now - this.lastFrameTime;
            this.performanceMetrics.fps = Math.round(1000 / frameDelta);
        }
        this.lastFrameTime = now;
        
        // Update detection count
        this.performanceMetrics.detectionCount = this.detectedObjects.size;
        
        // Dispatch performance update event
        const event = new CustomEvent('performanceUpdate', { 
            detail: this.performanceMetrics 
        });
        document.dispatchEvent(event);
    }

    setupPerformanceMonitoring() {
        // Listen for performance update requests
        document.addEventListener('requestPerformanceUpdate', () => {
            this.updatePerformanceMetrics();
        });
    }

    clearAllDetections() {
        this.detectedObjects.clear();
        this.trackingId = 1;
        
        // Clear UI detections
        const event = new CustomEvent('clearDetections');
        document.dispatchEvent(event);
    }

    clearTrackingData() {
        // Reset tracking IDs while keeping detections
        this.trackingId = 1;
        this.detectedObjects.forEach((detection, key) => {
            detection.id = null;
        });
    }

    showModelLoading() {
        // Show loading indicator
        const event = new CustomEvent('modelLoading', { detail: { loading: true } });
        document.dispatchEvent(event);
    }

    hideModelLoading() {
        // Hide loading indicator
        const event = new CustomEvent('modelLoading', { detail: { loading: false } });
        document.dispatchEvent(event);
    }

    updateModelPerformance(modelName) {
        const config = this.getModelConfig(modelName);
        
        // Update UI with model performance info
        const event = new CustomEvent('modelPerformanceUpdate', { 
            detail: {
                model: modelName,
                accuracy: config.accuracy,
                speed: config.speed,
                classes: config.classes
            }
        });
        document.dispatchEvent(event);
    }

    getDetectionStatistics() {
        const stats = {
            totalDetections: this.detectionHistory.length,
            activeDetections: this.detectedObjects.size,
            averageConfidence: this.calculateAverageConfidence(),
            detectionsByClass: this.getDetectionsByClass(),
            currentFPS: this.performanceMetrics.fps
        };
        
        return stats;
    }

    calculateAverageConfidence() {
        if (this.detectionHistory.length === 0) return 0;
        
        const sum = this.detectionHistory.reduce((acc, detection) => {
            return acc + detection.confidence;
        }, 0);
        
        return (sum / this.detectionHistory.length * 100).toFixed(1);
    }

    getDetectionsByClass() {
        const classCounts = {};
        
        this.detectionHistory.forEach(detection => {
            classCounts[detection.class] = (classCounts[detection.class] || 0) + 1;
        });
        
        return classCounts;
    }

    exportDetectionData() {
        const exportData = {
            timestamp: new Date().toISOString(),
            model: this.currentModel,
            confidence: this.confidence,
            trackingEnabled: this.trackingEnabled,
            statistics: this.getDetectionStatistics(),
            detectionHistory: this.detectionHistory.slice(-50) // Last 50 detections
        };
        
        // Create and download JSON file
        const blob = new Blob([JSON.stringify(exportData, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `divyadrishti-detections-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    // Real-time threat assessment
    assessThreatLevel() {
        const recentDetections = this.detectionHistory.slice(-10); // Last 10 detections
        let threatLevel = 'low';
        
        const personDetections = recentDetections.filter(d => d.class === 'person').length;
        const trailDetections = recentDetections.filter(d => d.class === 'unauthorized-trail').length;
        
        if (trailDetections > 0 && personDetections > 0) {
            threatLevel = 'critical';
        } else if (personDetections > 2) {
            threatLevel = 'high';
        } else if (personDetections > 0) {
            threatLevel = 'medium';
        }
        
        return threatLevel;
    }

    destroy() {
        this.stop();
        this.detectedObjects.clear();
        this.detectionHistory = [];
        console.log('Detection engine destroyed');
    }
}

// Initialize detection engine
document.addEventListener('DOMContentLoaded', () => {
    window.detectionEngine = new DetectionEngine();
    
    // Set up event listeners for integration with main app
    document.addEventListener('startSurveillance', () => {
        window.detectionEngine.start();
    });
    
    document.addEventListener('stopSurveillance', () => {
        window.detectionEngine.stop();
    });
    
    document.addEventListener('modelChanged', (e) => {
        window.detectionEngine.setModel(e.detail.model);
    });
    
    document.addEventListener('confidenceChanged', (e) => {
        window.detectionEngine.setConfidence(e.detail.confidence);
    });
    
    document.addEventListener('trackingToggled', (e) => {
        window.detectionEngine.enableTracking(e.detail.enabled);
    });
});

// Export detection engine for global access
window.DetectionEngine = DetectionEngine;
