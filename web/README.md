# 🌐 DivyaDrishti Web Interface

## 🚀 **Next-Generation Web-Based Border Surveillance System**

A modern, responsive web application for AI-powered drone border surveillance with real-time detection, tracking, and tactical mapping capabilities.

---

## ✨ **Features**

### 🎨 **Modern UI/UX**
- **Glass Morphism Design** - Sleek, translucent interface elements
- **Smooth Animations** - 60fps animations and micro-interactions
- **Responsive Layout** - Adapts to desktop, tablet, and mobile devices
- **Dark Theme** - Professional surveillance command center aesthetic
- **Interactive Elements** - Hover effects, ripple animations, and visual feedback

### 🤖 **AI Detection Capabilities**
- **Real-time Video Processing** - Live camera feed analysis
- **Multiple AI Models** - YOLOv11n/s/m and custom FootTrail detection
- **Object Tracking** - Persistent ID tracking across video frames
- **Confidence Adjustment** - Real-time sensitivity control
- **Detection Alerts** - Instant notifications for security threats

### 📊 **Performance Monitoring**
- **Live FPS Counter** - Real-time processing speed display
- **System Metrics** - GPU usage, memory consumption, processing time
- **Performance Graphs** - Visual representation of system health
- **Optimization Controls** - Dynamic performance tuning

### 🗺️ **Tactical Mapping**
- **Interactive Map** - Real-time drone positioning and tracking
- **Border Visualization** - India-Pakistan border line display
- **Detection Markers** - Visual representation of threat locations
- **Mission Status** - Comprehensive operational information

---

## 📁 **File Structure**

```
web/
├── index.html                 # Main application interface
├── tactical-map.html          # Interactive tactical map
├── css/
│   ├── styles.css            # Main stylesheet with glass morphism
│   └── animations.css        # Animation keyframes and effects
├── js/
│   ├── main.js              # Core application logic
│   ├── video-handler.js     # Video processing and display
│   ├── detection-engine.js  # AI detection simulation
│   └── animations.js        # Animation controller
└── README.md                # This file
```

---

## 🚀 **Quick Start**

### **1. Setup**
```bash
# Clone the repository
git clone https://github.com/didaco97/DivyaDrishtiAI.git
cd DivyaDrishtiAI/web

# Serve the files (choose one method)
```

### **2. Local Server Options**

#### **Python (Recommended)**
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

#### **Node.js**
```bash
# Install serve globally
npm install -g serve

# Serve the directory
serve -s . -l 8000
```

#### **PHP**
```bash
php -S localhost:8000
```

### **3. Access Application**
Open your browser and navigate to:
```
http://localhost:8000
```

---

## 🎮 **User Interface Guide**

### **Main Dashboard Layout**

```
┌─────────────┬─────────────────────────┬─────────────┐
│   Control   │     Video Display       │ Information │
│   Panel     │     ─────────────       │   Panel     │
│             │   [Raw Feed]            │             │
│   Models    │   [AI Analysis]         │   Alerts    │
│   Settings  │                         │   Metrics   │
│   Actions   │   Detection Overlays    │   Logs      │
│             │                         │             │
└─────────────┴─────────────────────────┴─────────────┘
```

### **Control Panel Features**
- **🤖 AI Model Selection** - Switch between detection models
- **🎯 Surveillance Controls** - Start/stop detection and tracking
- **⚙️ Settings** - Confidence threshold and performance options
- **⚡ Quick Actions** - Screenshot, recording, tactical map

### **Video Display**
- **📹 Raw Feed** - Live camera input
- **🧠 AI Analysis** - Processed video with detection overlays
- **🎯 Detection Boxes** - Color-coded bounding boxes with IDs
- **📊 Performance Metrics** - Real-time FPS and processing stats

### **Information Panel**
- **🚨 Threat Alerts** - Real-time security notifications
- **📈 Performance Monitor** - System resource usage
- **🚁 Drone Status** - GPS, altitude, battery, flight time

---

## ⌨️ **Keyboard Shortcuts**

| Key | Action |
|-----|--------|
| `Space` | Start/Stop Surveillance |
| `S` | Take Screenshot |
| `T` | Toggle Tracking |
| `F` | Toggle Fullscreen |
| `Esc` | Emergency Stop |

---

## 🎨 **Customization**

### **Color Scheme**
Edit CSS variables in `css/styles.css`:
```css
:root {
    --primary-bg: #0B1426;      /* Main background */
    --accent-teal: #00E5FF;     /* Primary accent */
    --accent-green: #39FF14;    /* Success/active */
    --warning: #FFA726;         /* Warning states */
    --danger: #FF5252;          /* Error/danger */
}
```

### **Animation Settings**
Modify animation durations in `css/animations.css`:
```css
:root {
    --transition-fast: 0.2s ease;
    --transition-normal: 0.3s ease;
    --transition-slow: 0.5s ease;
}
```

---

## 🔧 **Configuration**

### **Video Settings**
Modify camera resolution in `js/video-handler.js`:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({
    video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30 }
    }
});
```

### **Detection Parameters**
Adjust AI detection settings in `js/detection-engine.js`:
```javascript
const modelConfig = {
    'yolov11n': {
        classes: ['person', 'vehicle'],
        accuracy: 0.94,
        maxDetections: 3
    }
};
```

---

## 📱 **Responsive Design**

### **Breakpoints**
- **Desktop**: 1920px+ (Full three-column layout)
- **Laptop**: 1366px-1919px (Compressed layout)
- **Tablet**: 768px-1365px (Two-column layout)
- **Mobile**: 320px-767px (Single column stack)

### **Mobile Optimizations**
- Touch-friendly controls
- Swipeable video panels
- Collapsible sidebars
- Bottom navigation

---

## 🚀 **Performance Optimization**

### **Browser Requirements**
- **Modern Browser** with ES6+ support
- **WebRTC** for camera access
- **Canvas API** for video processing
- **CSS Grid/Flexbox** support

### **Recommended Specifications**
- **RAM**: 4GB+ (8GB recommended)
- **GPU**: Hardware acceleration enabled
- **Network**: Stable internet for map tiles
- **Camera**: HD webcam or integrated camera

---

## 🔒 **Security Considerations**

### **Camera Permissions**
- Application requests camera access on first load
- Fallback to demo video if camera unavailable
- No video data transmitted externally

### **Data Privacy**
- All processing happens locally in browser
- No detection data sent to external servers
- Screenshots and recordings stored locally

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Camera Not Working**
```
Solution: Check browser permissions and camera availability
- Allow camera access when prompted
- Ensure camera not in use by other applications
- Try refreshing the page
```

#### **Poor Performance**
```
Solution: Optimize browser and system settings
- Close unnecessary browser tabs
- Enable hardware acceleration
- Lower video resolution if needed
```

#### **Animations Stuttering**
```
Solution: Check system resources
- Close resource-intensive applications
- Update graphics drivers
- Reduce animation complexity in settings
```

---

## 🔮 **Future Enhancements**

### **Planned Features**
- **WebRTC Streaming** - Multi-device video sharing
- **Cloud Integration** - Remote monitoring capabilities
- **Mobile App** - Native iOS/Android applications
- **AI Model Upload** - Custom model integration
- **Multi-language Support** - Internationalization

### **Technical Improvements**
- **WebAssembly** - Faster AI processing
- **Service Workers** - Offline functionality
- **WebGL** - Hardware-accelerated rendering
- **Progressive Web App** - App-like experience

---

## 📞 **Support**

### **Getting Help**
- **Documentation**: Check this README and code comments
- **Issues**: Create GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions

### **Contributing**
1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

<div align="center">

**🌐 DivyaDrishti Web Interface v2.0**

*Next-Generation Border Surveillance Technology*

[![GitHub Stars](https://img.shields.io/github/stars/didaco97/DivyaDrishtiAI?style=social)](https://github.com/didaco97/DivyaDrishtiAI/stargazers)

</div>
