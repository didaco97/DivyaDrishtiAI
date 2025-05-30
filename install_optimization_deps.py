"""
DivyaDrishti Optimization Dependencies Installer
Installs additional packages required for model optimization
"""

import subprocess
import sys
import os


def install_package(package):
    """Install a package using pip"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False


def check_gpu_support():
    """Check if NVIDIA GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🎮 NVIDIA GPU detected: {gpu_name}")
            return True
        else:
            print("⚠️ No NVIDIA GPU detected - TensorRT optimization will be disabled")
            return False
    except ImportError:
        print("⚠️ PyTorch not found - please install PyTorch first")
        return False


def install_optimization_dependencies():
    """Install optimization dependencies"""
    print("🚀 Installing DivyaDrishti Optimization Dependencies")
    print("=" * 60)
    
    # Check GPU support first
    gpu_available = check_gpu_support()
    
    # Core optimization packages
    core_packages = [
        "onnx>=1.12.0",
        "onnxruntime>=1.13.0",
        "onnxsim>=0.4.0",
    ]
    
    # GPU-specific packages
    gpu_packages = [
        "onnxruntime-gpu>=1.13.0",
        "tensorrt>=8.5.0",  # May require manual installation
    ]
    
    # Install core packages
    print("\n📦 Installing core optimization packages...")
    for package in core_packages:
        install_package(package)
    
    # Install GPU packages if GPU is available
    if gpu_available:
        print("\n🎮 Installing GPU optimization packages...")
        for package in gpu_packages:
            if "tensorrt" in package:
                print(f"⚠️ TensorRT requires manual installation from NVIDIA")
                print("   Visit: https://developer.nvidia.com/tensorrt")
                continue
            install_package(package)
    
    # Additional performance packages
    performance_packages = [
        "psutil>=5.9.0",  # For system monitoring
        "numpy>=1.21.0",  # Ensure latest numpy
    ]
    
    print("\n⚡ Installing performance monitoring packages...")
    for package in performance_packages:
        install_package(package)
    
    print("\n✅ Optimization dependencies installation complete!")
    print("\n📋 Summary:")
    print("   ✅ ONNX optimization support")
    print("   ✅ Performance monitoring")
    if gpu_available:
        print("   ✅ GPU acceleration support")
        print("   ⚠️ TensorRT requires manual installation")
    else:
        print("   ⚠️ GPU optimization disabled (no NVIDIA GPU)")
    
    print("\n🚀 You can now use the optimization features in DivyaDrishti!")


def verify_installation():
    """Verify that optimization dependencies are properly installed"""
    print("\n🔍 Verifying installation...")
    
    try:
        import onnx
        print(f"✅ ONNX: {onnx.__version__}")
    except ImportError:
        print("❌ ONNX not found")
    
    try:
        import onnxruntime
        print(f"✅ ONNX Runtime: {onnxruntime.__version__}")
    except ImportError:
        print("❌ ONNX Runtime not found")
    
    try:
        import psutil
        print(f"✅ PSUtil: {psutil.__version__}")
    except ImportError:
        print("❌ PSUtil not found")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ PyTorch CUDA: {torch.version.cuda}")
        else:
            print("⚠️ PyTorch CUDA not available")
    except ImportError:
        print("❌ PyTorch not found")


if __name__ == "__main__":
    try:
        install_optimization_dependencies()
        verify_installation()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
