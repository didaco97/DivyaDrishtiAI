"""
DivyaDrishti Frame Processor
Optimized frame processing for better FPS and performance
"""

import cv2
import numpy as np
import time
from collections import deque
import threading
import config


class OptimizedFrameProcessor:
    def __init__(self):
        self.frame_buffer = deque(maxlen=config.BATCH_SIZE * 2)
        self.processed_buffer = deque(maxlen=10)
        self.last_frame = None
        self.frame_similarity_cache = deque(maxlen=5)
        self.skip_counter = 0
        self.adaptive_skip = config.SKIP_FRAMES
        self.fps_history = deque(maxlen=30)
        self.processing_lock = threading.Lock()
        
    def should_process_frame(self, frame):
        """
        Determine if frame should be processed based on optimization settings
        """
        # Always process first frame
        if self.last_frame is None:
            self.last_frame = frame.copy()
            return True
        
        # Adaptive frame skipping based on FPS
        if config.ADAPTIVE_SKIP_FRAMES:
            current_fps = self._get_current_fps()
            if current_fps < config.MAX_FPS * 0.7:  # If FPS drops below 70% of target
                self.adaptive_skip = min(self.adaptive_skip + 1, 5)
            elif current_fps > config.MAX_FPS * 0.9:  # If FPS is good
                self.adaptive_skip = max(self.adaptive_skip - 1, 1)
        
        # Frame skipping logic
        self.skip_counter += 1
        if self.skip_counter < self.adaptive_skip:
            return False
        
        self.skip_counter = 0
        
        # Smart frame selection - skip similar frames
        if config.SMART_FRAME_SELECTION:
            similarity = self._calculate_frame_similarity(frame, self.last_frame)
            if similarity > config.FRAME_SIMILARITY_THRESHOLD:
                return False
        
        self.last_frame = frame.copy()
        return True
    
    def optimize_frame(self, frame):
        """
        Optimize frame for faster processing
        """
        optimized_frame = frame.copy()
        
        # Resize frame if enabled
        if config.FRAME_RESIZE_ENABLED:
            height, width = frame.shape[:2]
            
            # Calculate new dimensions maintaining aspect ratio
            if width > config.FRAME_RESIZE_WIDTH or height > config.FRAME_RESIZE_HEIGHT:
                scale_w = config.FRAME_RESIZE_WIDTH / width
                scale_h = config.FRAME_RESIZE_HEIGHT / height
                scale = min(scale_w, scale_h)
                
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                optimized_frame = cv2.resize(
                    frame, 
                    (new_width, new_height), 
                    interpolation=cv2.INTER_LINEAR
                )
        
        # Apply additional optimizations
        optimized_frame = self._apply_preprocessing_optimizations(optimized_frame)
        
        return optimized_frame
    
    def _apply_preprocessing_optimizations(self, frame):
        """Apply preprocessing optimizations"""
        # Convert color space if needed for faster processing
        # Note: YOLO expects RGB, OpenCV uses BGR
        # This conversion is handled by ultralytics internally
        
        # Ensure frame is contiguous in memory for faster processing
        if not frame.flags['C_CONTIGUOUS']:
            frame = np.ascontiguousarray(frame)
        
        return frame
    
    def _calculate_frame_similarity(self, frame1, frame2):
        """
        Calculate similarity between two frames using histogram comparison
        """
        try:
            # Resize frames for faster comparison
            small_frame1 = cv2.resize(frame1, (64, 48))
            small_frame2 = cv2.resize(frame2, (64, 48))
            
            # Convert to grayscale for faster comparison
            gray1 = cv2.cvtColor(small_frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(small_frame2, cv2.COLOR_BGR2GRAY)
            
            # Calculate histogram correlation
            hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
            
            correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            return correlation
            
        except Exception as e:
            print(f"Frame similarity calculation error: {e}")
            return 0.0
    
    def _get_current_fps(self):
        """Get current FPS from history"""
        if not self.fps_history:
            return config.MAX_FPS
        return sum(self.fps_history) / len(self.fps_history)
    
    def update_fps(self, fps):
        """Update FPS history"""
        self.fps_history.append(fps)
    
    def prepare_batch(self, frames):
        """
        Prepare batch of frames for batch processing
        """
        if not config.BATCH_PROCESSING or len(frames) < 2:
            return frames
        
        batch = []
        for frame in frames:
            optimized_frame = self.optimize_frame(frame)
            batch.append(optimized_frame)
        
        return batch
    
    def get_processing_stats(self):
        """Get frame processing statistics"""
        return {
            "adaptive_skip": self.adaptive_skip,
            "current_fps": self._get_current_fps(),
            "frame_buffer_size": len(self.frame_buffer),
            "processed_buffer_size": len(self.processed_buffer),
            "frame_resize_enabled": config.FRAME_RESIZE_ENABLED,
            "smart_selection_enabled": config.SMART_FRAME_SELECTION,
            "batch_processing_enabled": config.BATCH_PROCESSING
        }
    
    def reset_optimization(self):
        """Reset optimization parameters"""
        self.skip_counter = 0
        self.adaptive_skip = config.SKIP_FRAMES
        self.frame_similarity_cache.clear()
        self.fps_history.clear()
        print("🔄 Frame processor optimization reset")


class VideoOptimizer:
    """Optimizes video capture settings for better performance"""
    
    @staticmethod
    def optimize_capture(cap):
        """
        Optimize video capture settings
        """
        try:
            # Set buffer size to reduce latency
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Set FPS if possible
            cap.set(cv2.CAP_PROP_FPS, config.MAX_FPS)
            
            # Set frame size for faster capture
            if config.FRAME_RESIZE_ENABLED:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_RESIZE_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_RESIZE_HEIGHT)
            
            # Disable auto-exposure for consistent performance (if supported)
            try:
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            except:
                pass
            
            # Set codec for better performance (if supported)
            try:
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            except:
                pass
            
            print("📹 Video capture optimized")
            return True
            
        except Exception as e:
            print(f"⚠️ Video capture optimization failed: {e}")
            return False
    
    @staticmethod
    def get_capture_info(cap):
        """Get video capture information"""
        try:
            info = {
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "buffer_size": cap.get(cv2.CAP_PROP_BUFFERSIZE),
                "codec": cap.get(cv2.CAP_PROP_FOURCC),
                "auto_exposure": cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
            }
            return info
        except Exception as e:
            print(f"Failed to get capture info: {e}")
            return {}


class PerformanceProfiler:
    """Profile and analyze performance bottlenecks"""
    
    def __init__(self):
        self.timings = {
            "frame_capture": deque(maxlen=100),
            "frame_optimization": deque(maxlen=100),
            "model_inference": deque(maxlen=100),
            "post_processing": deque(maxlen=100),
            "total_pipeline": deque(maxlen=100)
        }
    
    def start_timing(self, operation):
        """Start timing an operation"""
        return time.time()
    
    def end_timing(self, operation, start_time):
        """End timing and record"""
        duration = time.time() - start_time
        if operation in self.timings:
            self.timings[operation].append(duration)
        return duration
    
    def get_performance_report(self):
        """Generate performance report"""
        report = {}
        
        for operation, times in self.timings.items():
            if times:
                avg_time = sum(times) / len(times)
                report[operation] = {
                    "avg_ms": avg_time * 1000,
                    "fps": 1.0 / avg_time if avg_time > 0 else 0,
                    "samples": len(times)
                }
        
        return report
    
    def identify_bottlenecks(self):
        """Identify performance bottlenecks"""
        report = self.get_performance_report()
        bottlenecks = []
        
        for operation, stats in report.items():
            if stats["avg_ms"] > 50:  # Operations taking more than 50ms
                bottlenecks.append({
                    "operation": operation,
                    "avg_ms": stats["avg_ms"],
                    "severity": "high" if stats["avg_ms"] > 100 else "medium"
                })
        
        return sorted(bottlenecks, key=lambda x: x["avg_ms"], reverse=True)


# Global instances
frame_processor = OptimizedFrameProcessor()
video_optimizer = VideoOptimizer()
performance_profiler = PerformanceProfiler()
