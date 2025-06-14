"""
HickOyolo Utility Functions
Independent Hiking Trail Detection System
"""

import os
import cv2
import time
import requests
import numpy as np
from pathlib import Path
from datetime import datetime
import config

def create_directories():
    """Create necessary directories for the application"""
    directories = [
        config.SCREENSHOTS_DIR,
        config.SAVED_VIDEOS_DIR,
        config.LOGS_DIR
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory created/verified: {directory}")

def get_timestamp():
    """Get current timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

def save_screenshot(frame, prefix="detection"):
    """Save screenshot with timestamp"""
    if frame is None:
        return None

    timestamp = get_timestamp()
    filename = f"{prefix}_{timestamp}.{config.SCREENSHOT_FORMAT}"
    filepath = config.SCREENSHOTS_DIR / filename

    try:
        cv2.imwrite(str(filepath), frame)
        print(f"✓ Screenshot saved: {filename}")
        return str(filepath)
    except Exception as e:
        print(f"✗ Error saving screenshot: {e}")
        return None

def format_confidence(confidence):
    """Format confidence value for display"""
    return f"{confidence:.2%}"

def format_coordinates(x1, y1, x2, y2):
    """Format bounding box coordinates"""
    return f"({int(x1)}, {int(y1)}) - ({int(x2)}, {int(y2)})"

def calculate_box_area(x1, y1, x2, y2):
    """Calculate bounding box area"""
    return abs(x2 - x1) * abs(y2 - y1)

def calculate_box_center(x1, y1, x2, y2):
    """Calculate bounding box center point"""
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return center_x, center_y

def resize_frame_for_display(frame, max_width=640, max_height=480):
    """Resize frame for GUI display while maintaining aspect ratio"""
    if frame is None:
        return None

    height, width = frame.shape[:2]

    # Calculate scaling factor
    scale_w = max_width / width
    scale_h = max_height / height
    scale = min(scale_w, scale_h)

    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return frame

def test_camera_connection(camera_index=0):
    """Test camera connection"""
    try:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        return False
    except Exception:
        return False

def test_video_file(file_path):
    """Test video file accessibility"""
    try:
        cap = cv2.VideoCapture(file_path)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        return False
    except Exception:
        return False

def test_stream_connection(stream_url, timeout=10):
    """Test stream URL connection"""
    try:
        cap = cv2.VideoCapture(stream_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        start_time = time.time()
        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            if ret and frame is not None:
                cap.release()
                return True
            time.sleep(0.1)

        cap.release()
        return False
    except Exception:
        return False

def get_local_demo_videos():
    """Get list of local demo video files"""
    import os
    demo_videos = []

    # Check for local demo videos
    video_dirs = ["Testing Videos", "assets/videos", "demo_videos"]
    for video_dir in video_dirs:
        if os.path.exists(video_dir):
            for file in os.listdir(video_dir):
                if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    demo_videos.append(os.path.join(video_dir, file))

    return demo_videos

def get_device_info():
    """Get device information for display"""
    import torch

    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        return f"GPU: {device_name}"
    else:
        return "CPU"

def check_foottrail_model():
    """Check if foottrail model exists"""
    model_path = config.HIKING_MODEL_PATH
    if model_path.exists():
        print(f"✓ FootTrail model found: {model_path}")
        return True
    else:
        print(f"✗ FootTrail model not found: {model_path}")
        return False

def apply_cyberpunk_style(widget, widget_type="default"):
    """Apply cyberpunk styling to tkinter widgets"""
    theme = config.CYBERPUNK_THEME

    style_configs = {
        "default": {
            "bg": theme["bg_color"],
            "fg": theme["text_color"],
            "font": ("Consolas", 10)
        },
        "button": {
            "bg": theme["button_color"],
            "fg": theme["primary_color"],
            "activebackground": theme["button_hover"],
            "activeforeground": theme["accent_color"],
            "font": ("Consolas", 10, "bold"),
            "relief": "flat",
            "bd": 1
        },
        "label": {
            "bg": theme["bg_color"],
            "fg": theme["text_color"],
            "font": ("Consolas", 9)
        },
        "frame": {
            "bg": theme["bg_color"],
            "relief": "flat",
            "bd": 1
        }
    }

    if widget_type in style_configs:
        try:
            widget.config(**style_configs[widget_type])
        except Exception as e:
            print(f"Warning: Could not apply style to {widget_type}: {e}")

def log_system_info():
    """Log system information"""
    print("=" * 60)
    print(f"🎯 {config.APP_NAME} v{config.APP_VERSION}")
    print("=" * 60)
    print(f"Device: {get_device_info()}")
    print(f"FootTrail Model: {'✓ Found' if check_foottrail_model() else '✗ Missing'}")
    print(f"GPU Available: {'✓ Yes' if config.ENABLE_GPU else '✗ No'}")
    print(f"Detection Mode: {config.DETECTION_MODE.upper()}")
    print(f"Confidence Threshold: {config.CONFIDENCE_THRESHOLD}")
    print("=" * 60)
