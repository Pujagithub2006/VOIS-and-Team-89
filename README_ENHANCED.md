# Enhanced Elderly Monitoring System

A comprehensive, production-ready senior citizen monitoring system with advanced fall detection, health monitoring, multi-level alerts, and vicinity awareness.

## 🚀 Features

### Core Monitoring
- **Multi-Layer Fall Detection**: Threshold-based + ML-based + post-fall validation
- **Real-time Health Monitoring**: Heart rate, SpO₂, temperature tracking
- **Pre-Fall Instability Detection**: Early warning system
- **Posture and Activity Recognition**: Comprehensive motion analysis

### Alert System
- **Multi-Level Alerts**: Local buzzer, mobile notifications, email, SMS, voice calls
- **Intelligent Escalation**: Progressive alert escalation based on urgency
- **Rate Limiting**: Prevents alert fatigue
- **Real-time WebSocket Updates**: Live dashboard updates

### Location & Vicinity
- **Geofencing**: Safe zones and danger zones
- **Guardian Proximity Detection**: Know when guardians are nearby
- **Location-Based Risk Assessment**: Contextual risk evaluation

### AI & Intelligence
- **Explainable Decision Engine**: Understand why alerts are triggered
- **Continuous Learning**: System improves over time
- **Adaptive Thresholds**: Self-adjusting sensitivity

### Hardware Support
- **Hardware Abstraction**: Switch between simulation and real devices
- **Multiple Sensors**: MPU6050, MAX30102, DS18B20, buzzer, GSM
- **USB Pluggable**: Easy hardware integration

## 📋 System Requirements

- Python 3.8+
- Compatible with Windows, Linux, macOS
- Raspberry Pi support for embedded deployment
- Optional hardware sensors for real-world deployment

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vois-and-team-89
```

### 2. Install Dependencies
```bash
pip install -r requirements_enhanced.txt
```

### 3. Backend Setup
```bash
cd backend
python integrated_app.py
```

### 4. Frontend Access
- **Senior Interface**: `http://localhost:5000/frontend/senior_ui.html`
- **Guardian Dashboard**: `http://localhost:5000/frontend/guardian_dashboard.html`
- **Health Monitor**: `http://localhost:5000/frontend/senior_health.html`

## 🎯 Quick Start

### Demo Mode (No Hardware Required)
```bash
python src/main_enhanced.py
```

The system will start in demo mode with simulated sensor data and scenarios:
- Normal activity simulation
- Walking patterns
- Fall detection events
- Health anomaly scenarios

### Production Mode (With Hardware)
1. Connect hardware sensors via USB
2. Update configuration in `src/main_enhanced.py`
3. Set `DEMO_MODE = False`
4. Run the system

## 📊 System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Hardware      │    │   Feature        │    │   Fall          │
│   Interface     │───▶│   Extraction     │───▶│   Detection     │
│                 │    │                  │    │                 │
│ • MPU6050       │    │ • Motion         │    │ • Threshold     │
│ • MAX30102      │    │ • Vitals         │    │ • ML Classifier │
│ • DS18B20       │    │ • Temporal       │    │ • Validation    │
│ • Buzzer        │    │ • Anomaly        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vicinity      │    │   Decision       │    │   Alert         │
│   Awareness     │    │   Engine         │    │   System        │
│                 │    │                  │    │                 │
│ • Geofencing    │    │ • Explainable AI │    │ • Multi-Level   │
│ • Proximity     │    │ • Multi-Factor   │    │ • Escalation    │
│ • Location      │    │ • Adaptive       │    │ • Rate Limiting │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### System Configuration
```python
# src/main_enhanced.py
DEMO_MODE = True                    # Set False for production
BACKEND_URL = "http://localhost:5000/api"
PATIENT_ID = "demo_patient"
```

### Sensor Configuration
```python
# src/sensors/enhanced_hardware_interface.py
SERIAL_PORT = "/dev/ttyUSB0"        # Linux
# SERIAL_PORT = "COM3"              # Windows
SIMULATION_MODE = True              # Set False for real hardware
```

### Alert Configuration
```python
# src/alerts/multi_level_alert_system.py
MAX_ALERTS_PER_MINUTE = 5
MAX_ALERTS_PER_HOUR = 50
ESCALATION_DELAYS = [0, 60, 300, 600]  # Immediate, 1min, 5min, 10min
```

## 📱 User Interfaces

### Senior Citizen Interface
- **Large, accessible UI** designed for elderly users
- **SOS button** for emergency alerts
- **Medication reminders** and health status
- **Voice assistant** integration
- **Multi-language support**

### Guardian Dashboard
- **Real-time monitoring** of multiple patients
- **Alert management** and acknowledgment
- **Health metrics visualization**
- **Location tracking** and vicinity awareness
- **Communication tools**

## 🚨 Alert Types

| Alert Type | Level | Triggers | Channels |
|-------------|-------|----------|---------|
| Fall Detected | Critical | Impact + orientation change | Buzzer, Mobile, SMS, Email, Voice |
| Pre-Fall Warning | Warning | Instability patterns | Buzzer, Mobile |
| Health Anomaly | Warning | Vitals out of range | Mobile, Email |
| Device Offline | Info | No sensor data | Mobile, Email |
| Battery Low | Warning | Battery < 20% | Mobile, Email |

## 📍 Location Features

### Geofenced Zones
- **Safe Zones**: Home, medical facilities
- **Danger Zones**: Stairs, pools, restricted areas
- **Time Restrictions**: Zone access during specific hours

### Proximity Detection
- **Guardian Nearby**: Reduced alert urgency
- **Far from Guardian**: Increased alert priority
- **Location Quality**: GPS accuracy and freshness monitoring

## 🧠 AI & Machine Learning

### Fall Detection Models
- **Threshold-based**: Fast, reliable for obvious falls
- **ML Classifier**: Accurate for complex patterns
- **Post-Fall Validation**: Reduces false positives

### Decision Engine
- **Explainable AI**: Clear reasoning for decisions
- **Multi-Factor Analysis**: Combines motion, vitals, context
- **Adaptive Learning**: Improves from feedback

## 🔄 Demo Scenarios

The system includes automated demo scenarios that cycle every 60 seconds:

1. **Normal Activity**: Regular daily movements
2. **Walking**: Simulated walking patterns
3. **Sitting**: Resting posture
4. **Fall Simulation**: Various fall types
5. **Health Anomaly**: Vital sign irregularities
6. **Device Offline**: Connectivity issues

## 📊 Monitoring & Analytics

### Real-time Metrics
- Sensor data quality and freshness
- System performance and uptime
- Alert frequency and response times
- Battery levels and device status

### Historical Data
- Fall detection history
- Health trend analysis
- Alert pattern analysis
- System reliability metrics

## 🔒 Safety & Reliability

### Fail-Safes
- **Sensor Failure Detection**: Automatic fallback
- **Rate Limiting**: Prevents alert fatigue
- **Redundant Detection**: Multiple fall detection methods
- **Graceful Degradation**: System continues with partial failures

### Privacy
- **Local Processing**: Sensitive data processed locally
- **Secure Communication**: Encrypted data transmission
- **Data Minimization**: Only essential data shared
- **Consent Management**: User-controlled data sharing

## 🛠️ Development

### Project Structure
```
vois-and-team-89/
├── src/
│   ├── sensors/                 # Hardware interface
│   ├── detection/              # Fall detection & ML
│   ├── alerts/                 # Alert system
│   ├── location/               # Vicinity awareness
│   └── main_enhanced.py       # Main application
├── frontend/                   # Web interfaces
├── backend/                    # REST API
├── SilverCare/                 # Original components
└── docs/                      # Documentation
```

### Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## 🚀 Deployment

### Development
```bash
python src/main_enhanced.py
```

### Production (Raspberry Pi)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements_enhanced.txt

# Run as service
sudo systemctl enable elderly-monitoring
sudo systemctl start elderly-monitoring
```

### Docker Deployment
```bash
# Build image
docker build -t elderly-monitoring .

# Run container
docker run -d --name elderly-monitoring \
  -p 5000:5000 \
  --device /dev/ttyUSB0 \
  elderly-monitoring
```

## 📞 Support

### Troubleshooting
- **Hardware not detected**: Check USB connections and permissions
- **High false positives**: Adjust sensitivity thresholds
- **Missing alerts**: Verify backend connectivity and guardian contacts
- **Location errors**: Ensure GPS/WiFi is enabled

### Logs
```bash
# View system logs
tail -f elderly_monitoring.log

# View specific component logs
grep "Fall Detection" elderly_monitoring.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original SilverCare framework contributors
- Open-source sensor libraries
- Medical monitoring research community
- Elderly care professionals for requirements and feedback

---

**🚀 The system is now ready for end-to-end demonstration and production deployment!**
