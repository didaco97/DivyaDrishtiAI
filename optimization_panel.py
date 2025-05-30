"""
DivyaDrishti Optimization Control Panel
GUI for controlling performance optimization settings
"""

import tkinter as tk
from tkinter import ttk, messagebox
import config
from frame_processor import frame_processor, performance_profiler
from model_optimizer import model_optimizer


class OptimizationPanel:
    def __init__(self, parent):
        self.parent = parent
        self.optimization_window = None
        
    def show_optimization_panel(self):
        """Show the optimization control panel"""
        if self.optimization_window and self.optimization_window.winfo_exists():
            self.optimization_window.lift()
            return
            
        self.optimization_window = tk.Toplevel(self.parent)
        self.optimization_window.title("🚀 Performance Optimization")
        self.optimization_window.geometry("600x700")
        self.optimization_window.configure(bg=config.CYBERPUNK_THEME["bg_color"])
        
        # Make window resizable
        self.optimization_window.resizable(True, True)
        
        # Create main frame with scrollbar
        main_frame = tk.Frame(self.optimization_window, bg=config.CYBERPUNK_THEME["bg_color"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🚀 Performance Optimization Control",
            font=("Consolas", 16, "bold"),
            fg=config.CYBERPUNK_THEME["primary_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Model Optimization Tab
        model_frame = tk.Frame(notebook, bg=config.CYBERPUNK_THEME["bg_color"])
        notebook.add(model_frame, text="Model Optimization")
        self._create_model_optimization_tab(model_frame)
        
        # Frame Processing Tab
        frame_frame = tk.Frame(notebook, bg=config.CYBERPUNK_THEME["bg_color"])
        notebook.add(frame_frame, text="Frame Processing")
        self._create_frame_processing_tab(frame_frame)
        
        # Performance Monitor Tab
        perf_frame = tk.Frame(notebook, bg=config.CYBERPUNK_THEME["bg_color"])
        notebook.add(perf_frame, text="Performance Monitor")
        self._create_performance_monitor_tab(perf_frame)
        
        # Advanced Settings Tab
        advanced_frame = tk.Frame(notebook, bg=config.CYBERPUNK_THEME["bg_color"])
        notebook.add(advanced_frame, text="Advanced")
        self._create_advanced_settings_tab(advanced_frame)
        
    def _create_model_optimization_tab(self, parent):
        """Create model optimization controls"""
        # Model Optimization Section
        opt_frame = tk.LabelFrame(
            parent,
            text="Model Optimization",
            font=("Consolas", 12, "bold"),
            fg=config.CYBERPUNK_THEME["primary_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        )
        opt_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # TensorRT Toggle
        self.tensorrt_var = tk.BooleanVar(value=config.ENABLE_TENSORRT)
        tensorrt_check = tk.Checkbutton(
            opt_frame,
            text="Enable TensorRT Optimization (NVIDIA GPU)",
            variable=self.tensorrt_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_tensorrt
        )
        tensorrt_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # ONNX Toggle
        self.onnx_var = tk.BooleanVar(value=config.ENABLE_ONNX)
        onnx_check = tk.Checkbutton(
            opt_frame,
            text="Enable ONNX Optimization",
            variable=self.onnx_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_onnx
        )
        onnx_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Half Precision Toggle
        self.half_precision_var = tk.BooleanVar(value=config.ENABLE_HALF_PRECISION)
        half_check = tk.Checkbutton(
            opt_frame,
            text="Enable Half Precision (FP16)",
            variable=self.half_precision_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_half_precision
        )
        half_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Model Precision Selection
        precision_frame = tk.Frame(opt_frame, bg=config.CYBERPUNK_THEME["bg_color"])
        precision_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            precision_frame,
            text="Model Precision:",
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        ).pack(side=tk.LEFT)
        
        self.precision_var = tk.StringVar(value=config.MODEL_PRECISION)
        precision_combo = ttk.Combobox(
            precision_frame,
            textvariable=self.precision_var,
            values=["fp32", "fp16", "int8"],
            state="readonly",
            width=10
        )
        precision_combo.pack(side=tk.LEFT, padx=(10, 0))
        precision_combo.bind("<<ComboboxSelected>>", self._update_precision)
        
        # Optimize Models Button
        optimize_btn = tk.Button(
            opt_frame,
            text="🚀 Optimize All Models",
            font=("Consolas", 10, "bold"),
            fg=config.CYBERPUNK_THEME["bg_color"],
            bg=config.CYBERPUNK_THEME["primary_color"],
            command=self._optimize_all_models
        )
        optimize_btn.pack(pady=10)
        
    def _create_frame_processing_tab(self, parent):
        """Create frame processing controls"""
        # Frame Processing Section
        frame_opt_frame = tk.LabelFrame(
            parent,
            text="Frame Processing Optimization",
            font=("Consolas", 12, "bold"),
            fg=config.CYBERPUNK_THEME["primary_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        )
        frame_opt_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Frame Resize Toggle
        self.resize_var = tk.BooleanVar(value=config.FRAME_RESIZE_ENABLED)
        resize_check = tk.Checkbutton(
            frame_opt_frame,
            text="Enable Frame Resizing",
            variable=self.resize_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_frame_resize
        )
        resize_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Frame Size Controls
        size_frame = tk.Frame(frame_opt_frame, bg=config.CYBERPUNK_THEME["bg_color"])
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            size_frame,
            text="Resize Width:",
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        ).grid(row=0, column=0, sticky=tk.W)
        
        self.width_var = tk.IntVar(value=config.FRAME_RESIZE_WIDTH)
        width_spin = tk.Spinbox(
            size_frame,
            from_=320,
            to=1920,
            increment=32,
            textvariable=self.width_var,
            width=10,
            command=self._update_frame_size
        )
        width_spin.grid(row=0, column=1, padx=(10, 0))
        
        tk.Label(
            size_frame,
            text="Resize Height:",
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        ).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        self.height_var = tk.IntVar(value=config.FRAME_RESIZE_HEIGHT)
        height_spin = tk.Spinbox(
            size_frame,
            from_=240,
            to=1080,
            increment=24,
            textvariable=self.height_var,
            width=10,
            command=self._update_frame_size
        )
        height_spin.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        
        # Smart Frame Selection
        self.smart_selection_var = tk.BooleanVar(value=config.SMART_FRAME_SELECTION)
        smart_check = tk.Checkbutton(
            frame_opt_frame,
            text="Enable Smart Frame Selection",
            variable=self.smart_selection_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_smart_selection
        )
        smart_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Adaptive Frame Skipping
        self.adaptive_skip_var = tk.BooleanVar(value=config.ADAPTIVE_SKIP_FRAMES)
        adaptive_check = tk.Checkbutton(
            frame_opt_frame,
            text="Enable Adaptive Frame Skipping",
            variable=self.adaptive_skip_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_adaptive_skip
        )
        adaptive_check.pack(anchor=tk.W, padx=10, pady=5)
        
    def _create_performance_monitor_tab(self, parent):
        """Create performance monitoring display"""
        # Performance Stats
        stats_frame = tk.LabelFrame(
            parent,
            text="Real-time Performance Stats",
            font=("Consolas", 12, "bold"),
            fg=config.CYBERPUNK_THEME["primary_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        )
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stats display
        self.stats_text = tk.Text(
            stats_frame,
            height=15,
            font=("Consolas", 9),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["button_color"],
            state=tk.DISABLED
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            stats_frame,
            text="🔄 Refresh Stats",
            font=("Consolas", 10, "bold"),
            fg=config.CYBERPUNK_THEME["bg_color"],
            bg=config.CYBERPUNK_THEME["accent_color"],
            command=self._refresh_stats
        )
        refresh_btn.pack(pady=5)
        
        # Auto-refresh
        self._refresh_stats()
        self.optimization_window.after(2000, self._auto_refresh_stats)
        
    def _create_advanced_settings_tab(self, parent):
        """Create advanced optimization settings"""
        # Advanced Settings
        advanced_frame = tk.LabelFrame(
            parent,
            text="Advanced Optimization",
            font=("Consolas", 12, "bold"),
            fg=config.CYBERPUNK_THEME["primary_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        )
        advanced_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Batch Processing
        self.batch_var = tk.BooleanVar(value=config.BATCH_PROCESSING)
        batch_check = tk.Checkbutton(
            advanced_frame,
            text="Enable Batch Processing (Experimental)",
            variable=self.batch_var,
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"],
            selectcolor=config.CYBERPUNK_THEME["button_color"],
            command=self._update_batch_processing
        )
        batch_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Warm-up iterations
        warmup_frame = tk.Frame(advanced_frame, bg=config.CYBERPUNK_THEME["bg_color"])
        warmup_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            warmup_frame,
            text="Model Warm-up Iterations:",
            font=("Consolas", 10),
            fg=config.CYBERPUNK_THEME["text_color"],
            bg=config.CYBERPUNK_THEME["bg_color"]
        ).pack(side=tk.LEFT)
        
        self.warmup_var = tk.IntVar(value=config.WARM_UP_ITERATIONS)
        warmup_spin = tk.Spinbox(
            warmup_frame,
            from_=1,
            to=50,
            textvariable=self.warmup_var,
            width=10,
            command=self._update_warmup
        )
        warmup_spin.pack(side=tk.LEFT, padx=(10, 0))
        
        # Reset optimizations button
        reset_btn = tk.Button(
            advanced_frame,
            text="🔄 Reset All Optimizations",
            font=("Consolas", 10, "bold"),
            fg=config.CYBERPUNK_THEME["bg_color"],
            bg=config.CYBERPUNK_THEME["secondary_color"],
            command=self._reset_optimizations
        )
        reset_btn.pack(pady=10)
        
    # Event handlers
    def _update_tensorrt(self):
        config.ENABLE_TENSORRT = self.tensorrt_var.get()
        
    def _update_onnx(self):
        config.ENABLE_ONNX = self.onnx_var.get()
        
    def _update_half_precision(self):
        config.ENABLE_HALF_PRECISION = self.half_precision_var.get()
        
    def _update_precision(self, event=None):
        config.MODEL_PRECISION = self.precision_var.get()
        
    def _update_frame_resize(self):
        config.FRAME_RESIZE_ENABLED = self.resize_var.get()
        
    def _update_frame_size(self):
        config.FRAME_RESIZE_WIDTH = self.width_var.get()
        config.FRAME_RESIZE_HEIGHT = self.height_var.get()
        
    def _update_smart_selection(self):
        config.SMART_FRAME_SELECTION = self.smart_selection_var.get()
        
    def _update_adaptive_skip(self):
        config.ADAPTIVE_SKIP_FRAMES = self.adaptive_skip_var.get()
        
    def _update_batch_processing(self):
        config.BATCH_PROCESSING = self.batch_var.get()
        
    def _update_warmup(self):
        config.WARM_UP_ITERATIONS = self.warmup_var.get()
        
    def _optimize_all_models(self):
        """Optimize all available models"""
        try:
            messagebox.showinfo("Optimization", "Starting model optimization...\nThis may take a few minutes.")
            # This would trigger optimization in the background
            print("🚀 Starting model optimization...")
        except Exception as e:
            messagebox.showerror("Error", f"Optimization failed: {e}")
            
    def _refresh_stats(self):
        """Refresh performance statistics"""
        try:
            # Get performance report
            perf_report = performance_profiler.get_performance_report()
            frame_stats = frame_processor.get_processing_stats()
            
            # Update stats display
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            
            stats_text = "=== PERFORMANCE STATISTICS ===\n\n"
            
            # Pipeline performance
            stats_text += "Pipeline Performance:\n"
            for operation, stats in perf_report.items():
                stats_text += f"  {operation}: {stats['avg_ms']:.2f}ms ({stats['fps']:.1f} FPS)\n"
            
            stats_text += "\nFrame Processing:\n"
            for key, value in frame_stats.items():
                stats_text += f"  {key}: {value}\n"
            
            # Bottleneck analysis
            bottlenecks = performance_profiler.identify_bottlenecks()
            if bottlenecks:
                stats_text += "\n🚨 Performance Bottlenecks:\n"
                for bottleneck in bottlenecks:
                    stats_text += f"  {bottleneck['operation']}: {bottleneck['avg_ms']:.2f}ms ({bottleneck['severity']})\n"
            
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state=tk.DISABLED)
            
        except Exception as e:
            print(f"Stats refresh error: {e}")
            
    def _auto_refresh_stats(self):
        """Auto-refresh stats every 2 seconds"""
        if self.optimization_window and self.optimization_window.winfo_exists():
            self._refresh_stats()
            self.optimization_window.after(2000, self._auto_refresh_stats)
            
    def _reset_optimizations(self):
        """Reset all optimizations to default"""
        if messagebox.askyesno("Reset", "Reset all optimizations to default settings?"):
            frame_processor.reset_optimization()
            model_optimizer.clear_optimization_cache()
            messagebox.showinfo("Reset", "Optimizations reset successfully!")
