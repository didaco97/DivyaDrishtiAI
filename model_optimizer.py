"""
DivyaDrishti Model Optimizer
Handles TensorRT, ONNX, and other model optimizations for faster inference
"""

import os
import time
import torch
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import config


class ModelOptimizer:
    def __init__(self):
        self.optimized_models = {}
        self.optimization_cache = {}
        self.device = self._get_device()
        
    def _get_device(self):
        """Get the best available device"""
        if config.DEVICE == "auto":
            if torch.cuda.is_available() and config.ENABLE_GPU:
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return config.DEVICE
    
    def optimize_model(self, model_path, model_key):
        """
        Optimize a YOLO model for faster inference
        Returns optimized model path or original if optimization fails
        """
        try:
            print(f"🚀 Optimizing model: {model_key}")
            
            # Check if already optimized
            cache_key = f"{model_key}_{self.device}_{config.MODEL_PRECISION}"
            if cache_key in self.optimization_cache:
                print(f"✅ Using cached optimized model for {model_key}")
                return self.optimization_cache[cache_key]
            
            # Load original model
            model = YOLO(model_path)
            
            # Try TensorRT optimization for NVIDIA GPUs
            if self.device == "cuda" and config.ENABLE_TENSORRT:
                optimized_path = self._optimize_tensorrt(model, model_key)
                if optimized_path:
                    self.optimization_cache[cache_key] = optimized_path
                    return optimized_path
            
            # Try ONNX optimization
            if config.ENABLE_ONNX:
                optimized_path = self._optimize_onnx(model, model_key)
                if optimized_path:
                    self.optimization_cache[cache_key] = optimized_path
                    return optimized_path
            
            # Apply in-memory optimizations
            optimized_model = self._apply_memory_optimizations(model)
            if optimized_model:
                return model_path  # Return original path with optimized model in memory
                
            return model_path
            
        except Exception as e:
            print(f"⚠️ Model optimization failed for {model_key}: {e}")
            return model_path
    
    def _optimize_tensorrt(self, model, model_key):
        """Optimize model using TensorRT"""
        try:
            print(f"🔧 Applying TensorRT optimization to {model_key}...")
            
            # Create optimized model directory
            opt_dir = Path("Models/optimized/tensorrt")
            opt_dir.mkdir(parents=True, exist_ok=True)
            
            # TensorRT export path
            tensorrt_path = opt_dir / f"{model_key}_tensorrt.engine"
            
            # Skip if already exists and is recent
            if tensorrt_path.exists():
                print(f"✅ TensorRT model already exists: {tensorrt_path}")
                return str(tensorrt_path)
            
            # Export to TensorRT
            success = model.export(
                format="engine",
                device=self.device,
                half=config.ENABLE_HALF_PRECISION,
                dynamic=False,
                simplify=True,
                workspace=4,  # 4GB workspace
                verbose=False
            )
            
            if success and tensorrt_path.exists():
                print(f"✅ TensorRT optimization successful: {tensorrt_path}")
                return str(tensorrt_path)
            
        except Exception as e:
            print(f"⚠️ TensorRT optimization failed: {e}")
        
        return None
    
    def _optimize_onnx(self, model, model_key):
        """Optimize model using ONNX"""
        try:
            print(f"🔧 Applying ONNX optimization to {model_key}...")
            
            # Create optimized model directory
            opt_dir = Path("Models/optimized/onnx")
            opt_dir.mkdir(parents=True, exist_ok=True)
            
            # ONNX export path
            onnx_path = opt_dir / f"{model_key}_optimized.onnx"
            
            # Skip if already exists
            if onnx_path.exists():
                print(f"✅ ONNX model already exists: {onnx_path}")
                return str(onnx_path)
            
            # Export to ONNX
            success = model.export(
                format="onnx",
                device=self.device,
                half=config.ENABLE_HALF_PRECISION,
                dynamic=False,
                simplify=True,
                opset=12,
                verbose=False
            )
            
            if success and onnx_path.exists():
                print(f"✅ ONNX optimization successful: {onnx_path}")
                return str(onnx_path)
                
        except Exception as e:
            print(f"⚠️ ONNX optimization failed: {e}")
        
        return None
    
    def _apply_memory_optimizations(self, model):
        """Apply in-memory optimizations"""
        try:
            print("🔧 Applying memory optimizations...")
            
            # Move to device and optimize
            if self.device != "cpu":
                model.to(self.device)
            
            # Enable half precision if supported
            if config.ENABLE_HALF_PRECISION and self.device == "cuda":
                model.half()
            
            # Set to evaluation mode
            model.eval()
            
            # Warm up the model
            self._warm_up_model(model)
            
            print("✅ Memory optimizations applied")
            return model
            
        except Exception as e:
            print(f"⚠️ Memory optimization failed: {e}")
            return None
    
    def _warm_up_model(self, model):
        """Warm up model with dummy inputs"""
        try:
            print("🔥 Warming up model...")
            
            # Create dummy input
            dummy_input = torch.randn(1, 3, 640, 640)
            if self.device != "cpu":
                dummy_input = dummy_input.to(self.device)
            
            if config.ENABLE_HALF_PRECISION and self.device == "cuda":
                dummy_input = dummy_input.half()
            
            # Warm up iterations
            with torch.no_grad():
                for i in range(config.WARM_UP_ITERATIONS):
                    _ = model(dummy_input, verbose=False)
            
            print(f"✅ Model warmed up with {config.WARM_UP_ITERATIONS} iterations")
            
        except Exception as e:
            print(f"⚠️ Model warm-up failed: {e}")
    
    def get_optimization_info(self, model_key):
        """Get optimization information for a model"""
        cache_key = f"{model_key}_{self.device}_{config.MODEL_PRECISION}"
        
        info = {
            "model_key": model_key,
            "device": self.device,
            "precision": config.MODEL_PRECISION,
            "tensorrt_enabled": config.ENABLE_TENSORRT and self.device == "cuda",
            "onnx_enabled": config.ENABLE_ONNX,
            "half_precision": config.ENABLE_HALF_PRECISION,
            "optimized": cache_key in self.optimization_cache,
            "optimized_path": self.optimization_cache.get(cache_key, None)
        }
        
        return info
    
    def clear_optimization_cache(self):
        """Clear optimization cache"""
        self.optimization_cache.clear()
        print("🗑️ Optimization cache cleared")
    
    def benchmark_model(self, model_path, iterations=100):
        """Benchmark model performance"""
        try:
            print(f"📊 Benchmarking model: {model_path}")
            
            model = YOLO(model_path)
            if self.device != "cpu":
                model.to(self.device)
            
            # Create test input
            test_input = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
            
            # Warm up
            for _ in range(10):
                _ = model(test_input, verbose=False)
            
            # Benchmark
            times = []
            for i in range(iterations):
                start_time = time.time()
                _ = model(test_input, verbose=False)
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            fps = 1.0 / avg_time
            
            benchmark_results = {
                "avg_inference_time": avg_time * 1000,  # ms
                "fps": fps,
                "min_time": min(times) * 1000,
                "max_time": max(times) * 1000,
                "iterations": iterations
            }
            
            print(f"📊 Benchmark Results:")
            print(f"   Average FPS: {fps:.2f}")
            print(f"   Average Inference Time: {avg_time*1000:.2f}ms")
            
            return benchmark_results
            
        except Exception as e:
            print(f"⚠️ Benchmarking failed: {e}")
            return None


# Global optimizer instance
model_optimizer = ModelOptimizer()
