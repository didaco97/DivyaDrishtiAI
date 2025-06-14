"""
DivyaDrishti Configuration Settings
Independent Hiking Trail Detection System
"""

import os
from pathlib import Path

# Application Info
APP_NAME = "DivyaDrishti"
APP_VERSION = "1.0.0"
WINDOW_TITLE = f"{APP_NAME} - AI Drone Surveillance System v{APP_VERSION}"

# Paths
BASE_DIR = Path(__file__).parent
HIKING_MODEL_PATH = BASE_DIR / "foottrail.pt"  # Simplified path - model now in DivyaDrishti folder
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
SAVED_VIDEOS_DIR = BASE_DIR / "saved_videos"
LOGS_DIR = BASE_DIR / "logs"

# Multi-Model Configuration
AVAILABLE_MODELS = {
    "foottrail": {
        "name": "FootTrail Detection Model",
        "description": "Custom foottrail/hiking detection",
        "path": str(HIKING_MODEL_PATH),
        "type": "custom",
        "classes": ["trail", "path", "hiking_trail", "walkway", "footpath", "person", "hiker", "backpack", "tent", "camping_gear"],
        "icon": "🥾",
        "color": "#00ff41"
    },
    "yolov11n": {
        "name": "YOLOv11n",
        "description": "Fast general detection (nano)",
        "path": "yolo11n.pt",
        "type": "coco",
        "classes": ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light"],
        "icon": "⚡",
        "color": "#00d4ff"
    },
    "yolov11s": {
        "name": "YOLOv11s",
        "description": "Balanced performance (small)",
        "path": "yolo11s.pt",
        "type": "coco",
        "classes": ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light"],
        "icon": "⚖️",
        "color": "#ff8000"
    },
    "yolov11m": {
        "name": "YOLOv11m",
        "description": "High accuracy (medium)",
        "path": "yolo11m.pt",
        "type": "coco",
        "classes": ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light"],
        "icon": "🎯",
        "color": "#ff0080"
    },
    "yolov11s_seg": {
        "name": "YOLOv11s-seg",
        "description": "Segmentation mode",
        "path": "yolo11s-seg.pt",
        "type": "segmentation",
        "classes": ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light"],
        "icon": "🎨",
        "color": "#8000ff"
    }
}

# Default Model Settings
DEFAULT_MODEL_KEY = "yolov11n"  # Changed to YOLOv11n for person detection
CURRENT_MODEL = DEFAULT_MODEL_KEY
CONFIDENCE_THRESHOLD = 0.15  # Lowered for better person detection
IOU_THRESHOLD = 0.45
MAX_DETECTIONS = 1000

# Detection Settings
DETECTION_MODE = "detect"  # "detect" or "segment"

# Performance Settings
SKIP_FRAMES = 1  # Process every frame for best quality
MAX_FPS = 30
ENABLE_GPU = True
DEVICE = "auto"  # "auto", "cpu", "cuda", "mps"

# Optimization Settings
ENABLE_TENSORRT = True  # Enable TensorRT optimization for NVIDIA GPUs
ENABLE_ONNX = True      # Enable ONNX optimization for CPU/other devices
MODEL_PRECISION = "fp16"  # "fp32", "fp16", "int8" - lower precision = faster inference
OPTIMIZE_MODELS_ON_LOAD = True  # Auto-optimize models when loading

# Video Processing Optimization
FRAME_RESIZE_ENABLED = True  # Resize frames for faster processing
FRAME_RESIZE_WIDTH = 640     # Resize width (maintains aspect ratio)
FRAME_RESIZE_HEIGHT = 480    # Resize height
BATCH_PROCESSING = False     # Enable batch processing (experimental)
BATCH_SIZE = 4              # Batch size for processing multiple frames

# Advanced Performance Settings
WARM_UP_ITERATIONS = 10     # Number of warm-up iterations for model
ENABLE_HALF_PRECISION = True  # Use half precision (FP16) for faster inference
OPTIMIZE_FOR_MOBILE = False  # Optimize for mobile/edge devices
ENABLE_DYNAMIC_BATCHING = False  # Dynamic batch sizing based on GPU memory

# Frame Processing Strategy
SMART_FRAME_SELECTION = False  # DISABLED for tracking - breaks continuity
FRAME_SIMILARITY_THRESHOLD = 0.95  # Threshold for frame similarity (0-1)
ADAPTIVE_SKIP_FRAMES = False  # DISABLED for tracking - breaks continuity

# GUI Settings - Modern Light Theme
MODERN_LIGHT_THEME = {
    "bg_color": "#f8f9fa",           # Light gray background
    "card_bg": "#ffffff",            # White card background
    "text_color": "#2c3e50",        # Dark blue-gray text
    "primary_color": "#3498db",      # Modern blue
    "secondary_color": "#e74c3c",    # Modern red
    "accent_color": "#9b59b6",       # Purple accent
    "success_color": "#27ae60",      # Green
    "warning_color": "#f39c12",      # Orange
    "error_color": "#e74c3c",        # Red
    "button_color": "#ffffff",       # White button
    "button_hover": "#e3f2fd",       # Light blue hover
    "button_active": "#bbdefb",      # Blue active
    "border_color": "#dee2e6",       # Light border
    "shadow_color": "#00000010",     # Subtle shadow
    "gradient_start": "#74b9ff",     # Gradient start
    "gradient_end": "#0984e3",       # Gradient end
    "input_bg": "#ffffff",           # Input background
    "input_border": "#ced4da",       # Input border
    "input_focus": "#80bdff"         # Input focus
}

# Window Settings
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000
RESIZABLE = True

# Drone Video Settings
DEFAULT_DRONE_FEED = 0
DEFAULT_STREAM_URL = "sample_video.mp4"  # Local sample video
SUPPORTED_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"]

# Logging Settings
LOG_DETECTIONS = True
LOG_LEVEL = "INFO"
MAX_LOG_ENTRIES = 1000

# Screenshot Settings
SCREENSHOT_FORMAT = "jpg"
SCREENSHOT_QUALITY = 95
AUTO_SAVE_SCREENSHOTS = False

# Performance Monitoring
MONITOR_PERFORMANCE = True
PERFORMANCE_LOG_INTERVAL = 5  # seconds

# Advanced Features
ENABLE_SEGMENTATION = True
ENABLE_POSE_ESTIMATION = False
ENABLE_CLASSIFICATION = True

# Hiking Trail Specific Settings
TRAIL_CLASSES = [
    "trail", "path", "hiking_trail", "walkway", "footpath",
    "person", "hiker", "backpack", "tent", "camping_gear"
]

# Detection Zones (for trail-specific detection)
DETECTION_ZONES = {
    "trail_center": {"enabled": True, "weight": 1.0},
    "trail_edges": {"enabled": True, "weight": 0.8},
    "off_trail": {"enabled": False, "weight": 0.3}
}

# Alert Settings
ENABLE_ALERTS = True
ALERT_CONFIDENCE_THRESHOLD = 0.7
ALERT_SOUND = True

# Export Settings
EXPORT_FORMAT = "csv"
INCLUDE_TIMESTAMPS = True
INCLUDE_COORDINATES = True
INCLUDE_CONFIDENCE = True

# Tracking Settings
USE_TRACKING = True
ENABLE_SINGLE_SHOT_DETECTION = True
CUSTOM_TRACKER_CONFIG = "divyadrishti_tracker.yaml"
