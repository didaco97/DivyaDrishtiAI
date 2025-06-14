"""
DivyaDrishti GUI Application
Cyberpunk-themed Hiking Trail Detection System
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import threading
import time
from datetime import datetime
from PIL import Image, ImageTk
import numpy as np

import tempfile
import os

import config
import utils
from object_detector import MultiModelDetector
from detection_logger import DetectionLogger
from performance_monitor import PerformanceMonitor
from frame_processor import frame_processor, video_optimizer, performance_profiler
from optimization_panel import OptimizationPanel

class DivyaDrishtiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(bg=config.MODERN_LIGHT_THEME["bg_color"])

        # Initialize hover effects system
        self.hover_effects = {}
        self.setup_modern_styling()

        # Initialize components
        self.detector = MultiModelDetector()
        self.logger = DetectionLogger()
        self.performance_monitor = PerformanceMonitor()
        self.optimization_panel = OptimizationPanel(self.root)

        # Drone feed capture variables
        self.cap = None
        self.is_running = False
        self.video_source = config.DEFAULT_DRONE_FEED
        self.confidence_threshold = config.CONFIDENCE_THRESHOLD

        # Performance tracking
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        self.frame_count = 0

        # GUI state
        self.segmentation_enabled = False
        self.auto_save_enabled = config.AUTO_SAVE_SCREENSHOTS

        # Drone location simulation
        self.drone_lat = 32.7767
        self.drone_lon = 74.8728
        self.drone_sector = "JAMMU BORDER ZONE"

        # Create directories
        utils.create_directories()

        # Apply modern light theme
        self.setup_modern_theme()

        # Setup GUI
        self.setup_gui()

        # Start performance monitoring
        self.performance_monitor.start_monitoring()

        # Update model display
        self.update_model_display()

        # Start GUI update loop
        self.update_gui()

        # Log system info
        utils.log_system_info()

    def setup_modern_styling(self):
        """Setup modern styling system for hover effects and animations"""
        # Configure ttk styles for modern look
        try:
            import tkinter.ttk as ttk
            self.style = ttk.Style()
            self.style.theme_use('clam')  # Use clam theme as base

            # Configure modern button style
            self.style.configure('Modern.TButton',
                               background=config.MODERN_LIGHT_THEME["button_color"],
                               foreground=config.MODERN_LIGHT_THEME["text_color"],
                               borderwidth=1,
                               focuscolor='none',
                               relief='flat')

            self.style.map('Modern.TButton',
                          background=[('active', config.MODERN_LIGHT_THEME["button_hover"]),
                                    ('pressed', config.MODERN_LIGHT_THEME["button_active"])])
        except:
            pass  # Fallback to standard styling

    def setup_modern_theme(self):
        """Setup modern light theme styling"""
        # This method will be called to apply theme-specific configurations
        pass

    def add_hover_effect(self, widget, hover_bg=None, normal_bg=None, hover_fg=None, normal_fg=None):
        """Add smooth hover effects to widgets with enhanced animations"""
        if hover_bg is None:
            hover_bg = config.MODERN_LIGHT_THEME["button_hover"]
        if normal_bg is None:
            normal_bg = config.MODERN_LIGHT_THEME["button_color"]
        if hover_fg is None:
            hover_fg = config.MODERN_LIGHT_THEME["text_color"]
        if normal_fg is None:
            normal_fg = config.MODERN_LIGHT_THEME["text_color"]

        def on_enter(event):
            widget.configure(bg=hover_bg, fg=hover_fg, relief='raised', bd=1)

        def on_leave(event):
            widget.configure(bg=normal_bg, fg=normal_fg, relief='flat', bd=0)

        def on_click(event):
            widget.configure(relief='sunken', bd=1)
            widget.after(100, lambda: widget.configure(relief='raised', bd=1))

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        widget.bind("<Button-1>", on_click)

        # Store original colors
        self.hover_effects[widget] = {
            'normal_bg': normal_bg,
            'normal_fg': normal_fg,
            'hover_bg': hover_bg,
            'hover_fg': hover_fg
        }

    def add_card_shadow_effect(self, widget):
        """Add subtle shadow effect to card-like widgets"""
        # Create a shadow frame behind the widget
        shadow_frame = tk.Frame(widget.master, bg='#00000020', height=2)
        shadow_frame.place(in_=widget, x=2, y=2, relwidth=1, relheight=1)
        widget.lift()  # Bring widget to front

    def create_modern_button(self, parent, text, command=None, bg_color=None, hover_color=None, fg_color=None, **kwargs):
        """Create a modern styled button with hover effects"""
        if bg_color is None:
            bg_color = config.MODERN_LIGHT_THEME["button_color"]
        if hover_color is None:
            hover_color = config.MODERN_LIGHT_THEME["button_hover"]
        if fg_color is None:
            fg_color = config.MODERN_LIGHT_THEME["text_color"]

        # Remove fg from kwargs if present to avoid conflict
        kwargs.pop('fg', None)

        button = tk.Button(parent, text=text, command=command,
                          bg=bg_color,
                          fg=fg_color,
                          relief='flat',
                          bd=0,
                          padx=15,
                          pady=8,
                          cursor='hand2',
                          **kwargs)

        # Add hover effect
        self.add_hover_effect(button, hover_color, bg_color, fg_color, fg_color)

        return button

    def setup_gui(self):
        """Setup the main GUI layout with modern styling"""
        # Main container with modern styling
        main_frame = tk.Frame(self.root, bg=config.MODERN_LIGHT_THEME["bg_color"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header
        self.setup_header(main_frame)

        # Control panel
        self.setup_control_panel(main_frame)

        # Video panels
        self.setup_video_panels(main_frame)

        # Information panels
        self.setup_info_panels(main_frame)

        # Status bar
        self.setup_status_bar(main_frame)

    def setup_header(self, parent):
        """Setup application header with modern styling"""
        # Header container with card-like appearance
        header_frame = tk.Frame(parent, bg=config.MODERN_LIGHT_THEME["card_bg"],
                               relief='flat', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20), padx=5)

        # Add subtle border effect
        border_frame = tk.Frame(header_frame, bg=config.MODERN_LIGHT_THEME["border_color"], height=1)
        border_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Content frame with padding
        content_frame = tk.Frame(header_frame, bg=config.MODERN_LIGHT_THEME["card_bg"])
        content_frame.pack(fill=tk.X, padx=20, pady=15)

        # Title with modern typography
        title_label = tk.Label(content_frame,
                              text="🔍 DivyaDrishti",
                              font=('Segoe UI', 28, 'bold'),
                              fg=config.MODERN_LIGHT_THEME["primary_color"],
                              bg=config.MODERN_LIGHT_THEME["card_bg"])
        title_label.pack(side=tk.LEFT)

        # Subtitle with modern styling
        subtitle_label = tk.Label(content_frame,
                                 text="AI Surveillance System",
                                 font=('Segoe UI', 14),
                                 fg=config.MODERN_LIGHT_THEME["text_color"],
                                 bg=config.MODERN_LIGHT_THEME["card_bg"])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0), pady=(5, 0))

        # Version badge
        version_frame = tk.Frame(content_frame, bg=config.MODERN_LIGHT_THEME["accent_color"],
                                relief='flat')
        version_frame.pack(side=tk.RIGHT, padx=(0, 5))

        version_label = tk.Label(version_frame,
                                text=f" v{config.APP_VERSION} ",
                                font=('Segoe UI', 10, 'bold'),
                                fg='white',
                                bg=config.MODERN_LIGHT_THEME["accent_color"])
        version_label.pack(padx=8, pady=4)

    def setup_control_panel(self, parent):
        """Setup control panel with modern styling"""
        # Control panel container with card styling
        control_frame = tk.Frame(parent, bg=config.MODERN_LIGHT_THEME["card_bg"],
                                relief='flat', bd=1)
        control_frame.pack(fill=tk.X, pady=(0, 20), padx=5)

        # Header for control panel
        header_frame = tk.Frame(control_frame, bg=config.MODERN_LIGHT_THEME["primary_color"])
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="🎮 Control Panel",
                               font=('Segoe UI', 12, 'bold'),
                               fg='white',
                               bg=config.MODERN_LIGHT_THEME["primary_color"])
        header_label.pack(pady=8)

        # Main controls row with padding
        main_controls = tk.Frame(control_frame, bg=config.MODERN_LIGHT_THEME["card_bg"])
        main_controls.pack(fill=tk.X, padx=20, pady=15)

        # Model selection with modern styling
        model_frame = tk.Frame(main_controls, bg=config.MODERN_LIGHT_THEME["card_bg"])
        model_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        tk.Label(model_frame, text="🎯 Model:",
                font=('Segoe UI', 10, 'bold'),
                fg=config.MODERN_LIGHT_THEME["text_color"],
                bg=config.MODERN_LIGHT_THEME["card_bg"]).pack(side=tk.LEFT, pady=5)

        # Get model list from detector
        model_options = [display for key, display in self.detector.get_model_list_for_gui()]
        self.model_var = tk.StringVar()

        # Set default model
        current_model_info = self.detector.get_current_model_info()
        if current_model_info:
            default_display = f"{current_model_info['icon']} {current_model_info['name']} - {current_model_info['description']}"
            self.model_var.set(default_display)

        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var,
                                  values=model_options,
                                  state="readonly", width=35)
        model_combo.pack(side=tk.LEFT, padx=(10, 0))
        model_combo.bind("<<ComboboxSelected>>", self.on_model_change)

        # Drone feed source selection with modern styling
        source_frame = tk.Frame(main_controls, bg=config.MODERN_LIGHT_THEME["card_bg"])
        source_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 15))

        tk.Label(source_frame, text="📹 Video Source:",
                font=('Segoe UI', 10, 'bold'),
                fg=config.MODERN_LIGHT_THEME["text_color"],
                bg=config.MODERN_LIGHT_THEME["card_bg"]).pack(side=tk.LEFT, pady=5)

        self.source_var = tk.StringVar(value="Alpha Drone")
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_var,
                                   values=["Alpha Drone", "Video File", "Stream"],
                                   state="readonly", width=12)
        source_combo.pack(side=tk.LEFT, padx=(10, 0))
        source_combo.bind("<<ComboboxSelected>>", self.on_source_change)

        # File selection button with modern styling
        self.file_button = self.create_modern_button(source_frame, "📁 Select File",
                                                    command=self.select_video_file,
                                                    font=('Segoe UI', 9, 'bold'),
                                                    state=tk.DISABLED)
        self.file_button.pack(side=tk.LEFT, padx=(10, 0))

        # Action buttons with modern styling
        button_frame = tk.Frame(main_controls, bg=config.MODERN_LIGHT_THEME["card_bg"])
        button_frame.pack(side=tk.RIGHT, padx=(15, 0))

        self.start_button = self.create_modern_button(button_frame, "🚀 Start Detection",
                                                     command=self.start_detection,
                                                     bg_color=config.MODERN_LIGHT_THEME["success_color"],
                                                     hover_color="#229954",
                                                     fg_color='white',
                                                     font=('Segoe UI', 11, 'bold'))
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = self.create_modern_button(button_frame, "⏹️ Stop Detection",
                                                    command=self.stop_detection,
                                                    bg_color=config.MODERN_LIGHT_THEME["error_color"],
                                                    hover_color="#c0392b",
                                                    fg_color='white',
                                                    font=('Segoe UI', 11, 'bold'),
                                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        # Optimization button
        self.optimization_button = self.create_modern_button(button_frame, "⚙️ Optimize",
                                                           command=self.show_optimization_panel,
                                                           bg_color=config.MODERN_LIGHT_THEME["accent_color"],
                                                           hover_color="#8e44ad",
                                                           fg_color='white',
                                                           font=('Segoe UI', 11, 'bold'))
        self.optimization_button.pack(side=tk.LEFT, padx=(0, 10))

        # Feature toggles row with modern styling
        toggles_frame = tk.Frame(control_frame, bg=config.MODERN_LIGHT_THEME["card_bg"])
        toggles_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        # AI Analysis toggle
        self.segmentation_button = self.create_modern_button(toggles_frame,
                                                           "🤖 AI Analysis: OFF",
                                                           command=self.toggle_segmentation,
                                                           font=('Segoe UI', 10, 'bold'))
        self.segmentation_button.pack(side=tk.LEFT, padx=(0, 10))

        # Auto-record toggle
        self.autosave_button = self.create_modern_button(toggles_frame,
                                                       "📹 Auto-Record: OFF",
                                                       command=self.toggle_autosave,
                                                       font=('Segoe UI', 10, 'bold'))
        self.autosave_button.pack(side=tk.LEFT, padx=(0, 10))

        # Tracking toggle
        self.tracking_enabled = config.USE_TRACKING
        tracking_bg = config.MODERN_LIGHT_THEME["primary_color"] if self.tracking_enabled else config.MODERN_LIGHT_THEME["button_color"]
        tracking_fg = 'white' if self.tracking_enabled else config.MODERN_LIGHT_THEME["text_color"]

        self.tracking_button = self.create_modern_button(toggles_frame,
                                                       f"🎯 Tracking: {'ON' if self.tracking_enabled else 'OFF'}",
                                                       command=self.toggle_tracking,
                                                       bg_color=tracking_bg,
                                                       fg_color=tracking_fg,
                                                       font=('Segoe UI', 10, 'bold'))
        self.tracking_button.pack(side=tk.LEFT, padx=(0, 10))

        # Confidence slider with modern styling
        confidence_frame = tk.Frame(toggles_frame, bg=config.MODERN_LIGHT_THEME["card_bg"])
        confidence_frame.pack(side=tk.RIGHT, padx=(20, 0))

        tk.Label(confidence_frame, text="🎚️ Confidence:",
                font=('Segoe UI', 10, 'bold'),
                fg=config.MODERN_LIGHT_THEME["text_color"],
                bg=config.MODERN_LIGHT_THEME["card_bg"]).pack(side=tk.LEFT, pady=5)

        self.confidence_var = tk.DoubleVar(value=config.CONFIDENCE_THRESHOLD)
        confidence_scale = tk.Scale(confidence_frame, from_=0.05, to=1.0,
                                  variable=self.confidence_var, orient=tk.HORIZONTAL,
                                  length=150, resolution=0.01,
                                  bg=config.MODERN_LIGHT_THEME["card_bg"],
                                  fg=config.MODERN_LIGHT_THEME["primary_color"],
                                  activebackground=config.MODERN_LIGHT_THEME["primary_color"],
                                  troughcolor=config.MODERN_LIGHT_THEME["border_color"],
                                  highlightthickness=0,
                                  relief='flat')
        confidence_scale.pack(side=tk.LEFT, padx=(10, 0))

        self.confidence_label = tk.Label(confidence_frame, text=f"{config.CONFIDENCE_THRESHOLD:.2f}",
                                       font=('Segoe UI', 10, 'bold'),
                                       fg=config.MODERN_LIGHT_THEME["primary_color"],
                                       bg=config.MODERN_LIGHT_THEME["card_bg"])
        self.confidence_label.pack(side=tk.LEFT, padx=(8, 0))

        confidence_scale.bind("<Motion>", self.update_confidence_label)

    def setup_video_panels(self, parent):
        """Setup video display panels with modern styling"""
        video_frame = tk.Frame(parent, bg=config.MODERN_LIGHT_THEME["bg_color"])
        video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Main video feeds container with card styling
        feeds_container = tk.Frame(video_frame, bg=config.MODERN_LIGHT_THEME["card_bg"],
                                  relief='flat', bd=1)
        feeds_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # Left panel - Raw Video Feed
        left_frame = tk.LabelFrame(feeds_container, text="📹 Raw Video Feed",
                                  bg=config.MODERN_LIGHT_THEME["card_bg"],
                                  fg=config.MODERN_LIGHT_THEME["text_color"],
                                  font=('Segoe UI', 11, 'bold'))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.original_label = tk.Label(left_frame, bg='black')
        self.original_label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Right panel - AI Detection Analysis
        right_frame = tk.LabelFrame(feeds_container, text="🤖 AI Detection Analysis",
                                   bg=config.MODERN_LIGHT_THEME["card_bg"],
                                   fg=config.MODERN_LIGHT_THEME["text_color"],
                                   font=('Segoe UI', 11, 'bold'))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.processed_label = tk.Label(right_frame, bg='black')
        self.processed_label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Right side - Statistics Panel
        map_frame = tk.Frame(video_frame, bg=config.MODERN_LIGHT_THEME["card_bg"],
                            relief='flat', bd=1)
        map_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))
        map_frame.config(width=300)  # Fixed width for stats panel

        # Detection Statistics Panel with modern styling
        stats_header = tk.Frame(map_frame, bg=config.MODERN_LIGHT_THEME["primary_color"])
        stats_header.pack(fill=tk.X)

        stats_title = tk.Label(stats_header, text="📊 Detection Statistics",
                              font=('Segoe UI', 12, 'bold'),
                              fg='white',
                              bg=config.MODERN_LIGHT_THEME["primary_color"])
        stats_title.pack(pady=8)

        stats_content = tk.Label(map_frame,
                                text="Real-time YOLO\nAnalysis Dashboard\n\n🎯 Object Detection\n📈 Performance Metrics\n⚡ Live Monitoring",
                                font=('Segoe UI', 10),
                                fg=config.MODERN_LIGHT_THEME["text_color"],
                                bg=config.MODERN_LIGHT_THEME["card_bg"],
                                justify=tk.CENTER)
        stats_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def setup_info_panels(self, parent):
        """Setup information display panels with modern styling"""
        info_frame = tk.Frame(parent, bg=config.MODERN_LIGHT_THEME["bg_color"])
        info_frame.pack(fill=tk.X, pady=(0, 20))

        # Detection log panel with card styling
        log_frame = tk.Frame(info_frame, bg=config.MODERN_LIGHT_THEME["card_bg"],
                            relief='flat', bd=1)
        log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Log header
        log_header = tk.Frame(log_frame, bg=config.MODERN_LIGHT_THEME["success_color"])
        log_header.pack(fill=tk.X)

        log_title = tk.Label(log_header, text="🎯 Detection Log",
                            font=('Segoe UI', 11, 'bold'),
                            fg='white',
                            bg=config.MODERN_LIGHT_THEME["success_color"])
        log_title.pack(pady=6)

        # Create text widget for logs
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD,
                               bg=config.MODERN_LIGHT_THEME["card_bg"],
                               fg=config.MODERN_LIGHT_THEME["text_color"],
                               font=('Segoe UI', 9),
                               insertbackground=config.MODERN_LIGHT_THEME["primary_color"],
                               relief='flat',
                               bd=0)

        log_scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Performance panel with card styling
        perf_frame = tk.Frame(info_frame, bg=config.MODERN_LIGHT_THEME["card_bg"],
                             relief='flat', bd=1)
        perf_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Performance header
        perf_header = tk.Frame(perf_frame, bg=config.MODERN_LIGHT_THEME["warning_color"])
        perf_header.pack(fill=tk.X)

        perf_title = tk.Label(perf_header, text="⚡ Performance",
                             font=('Segoe UI', 11, 'bold'),
                             fg='white',
                             bg=config.MODERN_LIGHT_THEME["warning_color"])
        perf_title.pack(pady=6)

        self.perf_text = tk.Text(perf_frame, height=8, wrap=tk.WORD,
                                bg=config.MODERN_LIGHT_THEME["card_bg"],
                                fg=config.MODERN_LIGHT_THEME["text_color"],
                                font=('Segoe UI', 9),
                                insertbackground=config.MODERN_LIGHT_THEME["primary_color"],
                                relief='flat',
                                bd=0)

        perf_scrollbar = tk.Scrollbar(perf_frame, orient=tk.VERTICAL, command=self.perf_text.yview)
        self.perf_text.configure(yscrollcommand=perf_scrollbar.set)

        self.perf_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        perf_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

    def setup_status_bar(self, parent):
        """Setup status bar with modern styling"""
        status_frame = tk.Frame(parent, bg=config.MODERN_LIGHT_THEME["card_bg"],
                               relief='flat', bd=1)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        # Status label with modern styling
        self.status_label = tk.Label(status_frame, text="🟢 System Ready",
                                   font=('Segoe UI', 10, 'bold'),
                                   fg=config.MODERN_LIGHT_THEME["success_color"],
                                   bg=config.MODERN_LIGHT_THEME["card_bg"])
        self.status_label.pack(side=tk.LEFT, padx=15, pady=8)

        # Device info with modern styling
        device_info = utils.get_device_info()
        self.device_label = tk.Label(status_frame, text=f"🖥️ {device_info}",
                                   font=('Segoe UI', 9),
                                   fg=config.MODERN_LIGHT_THEME["accent_color"],
                                   bg=config.MODERN_LIGHT_THEME["card_bg"])
        self.device_label.pack(side=tk.RIGHT, padx=(10, 15), pady=8)

        # FPS display with modern styling
        self.fps_label = tk.Label(status_frame, text="📊 FPS: 0",
                                font=('Segoe UI', 9),
                                fg=config.MODERN_LIGHT_THEME["primary_color"],
                                bg=config.MODERN_LIGHT_THEME["card_bg"])
        self.fps_label.pack(side=tk.RIGHT, padx=(10, 0), pady=8)

        # Frame count with modern styling
        self.frame_label = tk.Label(status_frame, text="🎬 Frames: 0",
                                  font=('Segoe UI', 9),
                                  fg=config.MODERN_LIGHT_THEME["text_color"],
                                  bg=config.MODERN_LIGHT_THEME["card_bg"])
        self.frame_label.pack(side=tk.RIGHT, padx=(10, 0), pady=8)

    def on_model_change(self, event=None):
        """Handle model change"""
        if self.is_running:
            messagebox.showwarning("Warning", "Please stop detection before changing models.")
            # Reset to current model
            current_model_info = self.detector.get_current_model_info()
            if current_model_info:
                default_display = f"{current_model_info['icon']} {current_model_info['name']} - {current_model_info['description']}"
                self.model_var.set(default_display)
            return

        selected_display = self.model_var.get()

        # Find the model key from the display name
        model_key = None
        for key, display in self.detector.get_model_list_for_gui():
            if display == selected_display:
                model_key = key
                break

        if model_key:
            self.update_status(f"🔄 Switching to {self.detector.available_models[model_key]['name']}...")

            # Switch model in a separate thread to avoid GUI freezing
            import threading
            def switch_model_thread():
                success = self.detector.switch_model(model_key)
                if success:
                    model_info = self.detector.get_current_model_info()
                    self.update_status(f"✅ Switched to {model_info['name']}")

                    # Update status bar with new model info
                    self.root.after(100, self.update_model_display)
                else:
                    self.update_status(f"❌ Failed to switch model")
                    # Reset dropdown to previous model
                    current_model_info = self.detector.get_current_model_info()
                    if current_model_info:
                        default_display = f"{current_model_info['icon']} {current_model_info['name']} - {current_model_info['description']}"
                        self.root.after(100, lambda: self.model_var.set(default_display))

            threading.Thread(target=switch_model_thread, daemon=True).start()

    def update_model_display(self):
        """Update model information in the GUI"""
        model_info = self.detector.get_current_model_info()
        if model_info:
            # Update device label with model info
            device_info = utils.get_device_info()
            model_text = f"🎯 {model_info['name']} | 🖥️ {device_info}"
            self.device_label.config(text=model_text, fg=model_info['color'])

    def on_source_change(self, event=None):
        """Handle drone feed source change"""
        source_type = self.source_var.get()

        if source_type == "Video File":
            self.file_button.config(state=tk.NORMAL)
            self.video_source = None
        elif source_type == "Stream":
            # For now, use default stream
            self.video_source = config.DEFAULT_STREAM_URL
            self.file_button.config(state=tk.DISABLED)
        else:  # Alpha Drone
            self.video_source = config.DEFAULT_DRONE_FEED
            self.file_button.config(state=tk.DISABLED)

        self.update_status(f"🚁 Drone feed changed to: {source_type}")

    def select_video_file(self):
        """Select video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.video_source = file_path
            self.update_status(f"📁 Selected: {file_path}")

    def toggle_segmentation(self):
        """Toggle segmentation mode"""
        if self.is_running:
            messagebox.showwarning("Warning", "Please stop detection before changing modes.")
            return

        self.segmentation_enabled = not self.segmentation_enabled
        mode = "segment" if self.segmentation_enabled else "detect"

        # Update detector mode
        success = self.detector.switch_mode(mode)
        if success:
            button_text = f"🤖 AI Analysis: {'ON' if self.segmentation_enabled else 'OFF'}"
            self.segmentation_button.config(text=button_text)

            if self.segmentation_enabled:
                self.segmentation_button.config(bg=config.MODERN_LIGHT_THEME["primary_color"], fg='white')
            else:
                self.segmentation_button.config(bg=config.MODERN_LIGHT_THEME["button_color"],
                                               fg=config.MODERN_LIGHT_THEME["text_color"])

            self.update_status(f"🤖 AI analysis {'enabled' if self.segmentation_enabled else 'disabled'}")
        else:
            self.segmentation_enabled = not self.segmentation_enabled  # Revert
            messagebox.showerror("Error", "Failed to switch detection mode")



    def toggle_autosave(self):
        """Toggle auto-record surveillance"""
        self.auto_save_enabled = not self.auto_save_enabled
        button_text = f"📹 Auto-Record: {'ON' if self.auto_save_enabled else 'OFF'}"
        self.autosave_button.config(text=button_text)

        if self.auto_save_enabled:
            self.autosave_button.config(bg=config.MODERN_LIGHT_THEME["primary_color"], fg='white')
        else:
            self.autosave_button.config(bg=config.MODERN_LIGHT_THEME["button_color"],
                                       fg=config.MODERN_LIGHT_THEME["text_color"])

        self.update_status(f"📹 Auto-record {'enabled' if self.auto_save_enabled else 'disabled'}")

    def toggle_tracking(self):
        """Toggle object tracking for persistent annotations"""
        self.tracking_enabled = not self.tracking_enabled

        # Update detector tracking
        success = self.detector.enable_tracking(self.tracking_enabled)

        if success:
            button_text = f"🎯 Tracking: {'ON' if self.tracking_enabled else 'OFF'}"
            self.tracking_button.config(text=button_text)

            if self.tracking_enabled:
                self.tracking_button.config(bg=config.MODERN_LIGHT_THEME["primary_color"], fg='white')
                self.update_status("🎯 Object tracking enabled - persistent annotations activated")
            else:
                self.tracking_button.config(bg=config.MODERN_LIGHT_THEME["button_color"],
                                           fg=config.MODERN_LIGHT_THEME["text_color"])
                self.update_status("⚠️ Object tracking disabled - single-shot detection mode")
        else:
            self.tracking_enabled = not self.tracking_enabled  # Revert
            messagebox.showerror("Error", "Failed to toggle tracking mode")

    def show_optimization_panel(self):
        """Show the optimization control panel"""
        self.optimization_panel.show_optimization_panel()

    def update_confidence_label(self, event=None):
        """Update confidence threshold label"""
        value = self.confidence_var.get()
        self.confidence_label.config(text=f"{value:.2f}")
        self.confidence_threshold = value



    def update_drone_location(self):
        """Simulate drone movement and update location display"""
        if self.is_running:
            # Simulate small movements (realistic drone patrol)
            import random
            self.drone_lat += (random.random() - 0.5) * 0.0001  # Small lat change
            self.drone_lon += (random.random() - 0.5) * 0.0001  # Small lon change

            # Keep within reasonable bounds (Jammu border area)
            self.drone_lat = max(32.7, min(32.85, self.drone_lat))
            self.drone_lon = max(74.8, min(74.95, self.drone_lon))

            # Update sector based on location
            if self.drone_lat > 32.8:
                self.drone_sector = "NORTHERN PATROL ZONE"
            elif self.drone_lat < 32.75:
                self.drone_sector = "SOUTHERN BORDER ZONE"
            else:
                self.drone_sector = "JAMMU BORDER ZONE"

        # Update location tracking for surveillance monitoring

    def start_detection(self):
        """Start drone surveillance"""
        if not self.detector.is_model_loaded():
            messagebox.showerror("Error", "AI detection model not loaded!")
            return

        if self.video_source is None:
            messagebox.showwarning("Warning", "Please select a drone feed source!")
            return

        try:
            # Initialize video capture
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                messagebox.showerror("Error", f"Could not open video source: {self.video_source}")
                return

            # Optimize video capture settings
            video_optimizer.optimize_capture(self.cap)
            capture_info = video_optimizer.get_capture_info(self.cap)
            print(f"📹 Video capture info: {capture_info}")

            # Start detection
            self.is_running = True
            self.frame_count = 0
            self.fps_start_time = time.time()

            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_status("🚀 Surveillance started")

            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detection_loop, daemon=True)
            self.detection_thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start detection: {e}")
            self.is_running = False

    def stop_detection(self):
        """Stop detection"""
        self.is_running = False

        if self.cap:
            self.cap.release()
            self.cap = None

        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("⏹️ Surveillance stopped")

        # Clear video displays
        self.clear_video_displays()

    def detection_loop(self):
        """Optimized main detection loop"""
        while self.is_running and self.cap and self.cap.isOpened():
            try:
                # Capture frame with timing
                cap_start = performance_profiler.start_timing("frame_capture")
                ret, frame = self.cap.read()
                performance_profiler.end_timing("frame_capture", cap_start)

                if not ret:
                    break

                # Process frame with optimized YOLO detection
                start_time = time.time()
                processed_frame, detections = self.detector.detect(
                    frame,
                    confidence_threshold=self.confidence_threshold
                )
                inference_time = time.time() - start_time

                # Update performance monitors
                self.performance_monitor.update_fps(inference_time)
                frame_processor.update_fps(1.0 / inference_time if inference_time > 0 else 0)

                # Log detections
                for detection in detections:
                    self.logger.log_detection(detection, self.frame_count)

                # Auto-save screenshots if enabled
                if self.auto_save_enabled and detections:
                    utils.save_screenshot(processed_frame, "auto_detection")

                # Update displays
                self.update_video_displays(frame, processed_frame)

                # Update counters
                self.frame_count += 1

                # Adaptive frame rate control
                target_fps = config.MAX_FPS
                if config.ADAPTIVE_SKIP_FRAMES:
                    current_fps = frame_processor._get_current_fps()
                    if current_fps > 0:
                        sleep_time = max(0, (1.0 / target_fps) - inference_time)
                        time.sleep(sleep_time)
                else:
                    time.sleep(1.0 / target_fps)

            except Exception as e:
                print(f"Detection loop error: {e}")
                break

        # Cleanup
        if self.cap:
            self.cap.release()
        self.is_running = False

    def update_video_displays(self, original_frame, processed_frame):
        """Update video display panels"""
        try:
            # Resize frames for display (proper size for drone feeds)
            original_display = utils.resize_frame_for_display(original_frame, 580, 400)
            processed_display = utils.resize_frame_for_display(processed_frame, 580, 400)

            # Convert to PIL Images
            if original_display is not None:
                original_rgb = cv2.cvtColor(original_display, cv2.COLOR_BGR2RGB)
                original_pil = Image.fromarray(original_rgb)
                original_photo = ImageTk.PhotoImage(original_pil)

                self.original_label.configure(image=original_photo)
                self.original_label.image = original_photo

            if processed_display is not None:
                processed_rgb = cv2.cvtColor(processed_display, cv2.COLOR_BGR2RGB)
                processed_pil = Image.fromarray(processed_rgb)
                processed_photo = ImageTk.PhotoImage(processed_pil)

                self.processed_label.configure(image=processed_photo)
                self.processed_label.image = processed_photo

        except Exception as e:
            print(f"Display update error: {e}")

    def clear_video_displays(self):
        """Clear video display panels"""
        self.original_label.configure(image="")
        self.original_label.image = None
        self.processed_label.configure(image="")
        self.processed_label.image = None

    def update_status(self, message):
        """Update status message"""
        self.status_label.config(text=message)
        print(f"Status: {message}")

    def update_gui(self):
        """Update GUI elements periodically"""
        try:
            # Update FPS display
            current_fps = self.performance_monitor.get_current_fps()
            self.fps_label.config(text=f"📊 FPS: {current_fps:.1f}")

            # Update frame count
            self.frame_label.config(text=f"🎬 FRAMES: {self.frame_count:,}")

            # Update drone location
            self.update_drone_location()

            # Update detection log
            self.update_detection_log()

            # Update performance display
            self.update_performance_display()

        except Exception as e:
            print(f"GUI update error: {e}")

        # Schedule next update
        self.root.after(1000, self.update_gui)  # Update every second

    def update_detection_log(self):
        """Update detection log display"""
        try:
            summary = self.logger.get_detection_summary()

            # Clear and update log text
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, summary)

            # Auto-scroll to bottom
            self.log_text.see(tk.END)

        except Exception as e:
            print(f"Log update error: {e}")

    def update_performance_display(self):
        """Update performance display"""
        try:
            perf_summary = self.performance_monitor.get_performance_summary()

            # Clear and update performance text
            self.perf_text.delete(1.0, tk.END)
            self.perf_text.insert(tk.END, perf_summary)

            # Auto-scroll to bottom
            self.perf_text.see(tk.END)

        except Exception as e:
            print(f"Performance update error: {e}")

    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_detection()

        # Stop performance monitoring
        self.performance_monitor.stop_monitoring()

        # Export logs
        try:
            self.logger.export_logs()
            self.performance_monitor.export_performance_log()
        except Exception as e:
            print(f"Export error on closing: {e}")

        self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = DivyaDrishtiGUI(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
