"""
Simple Backend API for Testing

Basic Flask API for testing the elderly monitoring system without complex dependencies.
Provides mock endpoints for all major features.
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# Mock data storage
sensor_data = {
    'motion': {'ax': 0.12, 'ay': 0.08, 'az': 9.81, 'gx': 0.01, 'gy': 0.02, 'gz': 0.00},
    'vitals': {'heart_rate': 72, 'temperature': 36.8, 'spo2': 98},
    'battery': {'level': 85, 'voltage': 3.7, 'charging': False},
    'device_status': {'worn': True, 'connected': True, 'sensors_ok': True}
}

alerts = []
learning_data = []

@app.route('/api/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/fall/detect', methods=['POST'])
def detect_fall():
    """Mock fall detection endpoint."""
    data = request.get_json()
    acceleration = data.get('acceleration', [0, 0, 9.8])
    
    # Simple fall detection logic
    fall_detected = abs(acceleration[2]) > 15.0
    
    if fall_detected:
        alert = {
            'id': len(alerts) + 1,
            'type': 'fall',
            'message': 'Fall detected!',
            'severity': 'high',
            'timestamp': datetime.now().isoformat()
        }
        alerts.append(alert)
    
    return jsonify({
        'fall_detected': fall_detected,
        'confidence': 0.95 if fall_detected else 0.05,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/sensors/current', methods=['GET'])
def get_sensor_data():
    """Get current sensor data."""
    # Simulate realistic sensor variations
    sensor_data['motion']['ax'] = round(random.uniform(-2, 2), 2)
    sensor_data['motion']['ay'] = round(random.uniform(-2, 2), 2)
    sensor_data['motion']['az'] = round(random.uniform(8, 12), 2)
    sensor_data['vitals']['heart_rate'] = random.randint(65, 85)
    sensor_data['vitals']['temperature'] = round(random.uniform(36.0, 37.5), 1)
    sensor_data['battery']['level'] = max(0, sensor_data['battery']['level'] - random.uniform(0, 0.1))
    
    return jsonify(sensor_data)

@app.route('/api/alerts/test', methods=['POST'])
def test_alert():
    """Test alert system."""
    data = request.get_json()
    alert = {
        'id': len(alerts) + 1,
        'type': data.get('type', 'test'),
        'message': data.get('message', 'Test alert'),
        'priority': data.get('priority', 'low'),
        'timestamp': datetime.now().isoformat()
    }
    alerts.append(alert)
    
    return jsonify({
        'success': True,
        'alert_id': alert['id'],
        'message': 'Test alert created'
    })

@app.route('/api/alerts/send', methods=['POST'])
def send_alert():
    """Send alert with priority."""
    data = request.get_json()
    alert = {
        'id': len(alerts) + 1,
        'type': data.get('type', 'alert'),
        'message': data.get('message', 'Alert message'),
        'priority': data.get('priority', 'medium'),
        'timestamp': datetime.now().isoformat()
    }
    alerts.append(alert)
    
    return jsonify({
        'success': True,
        'alert_id': alert['id'],
        'message': 'Alert sent successfully'
    })

@app.route('/api/learning/data', methods=['POST'])
def add_learning_data():
    """Add learning data point."""
    data = request.get_json()
    learning_point = {
        'patient_id': data.get('patient_id', 'demo_patient'),
        'features': data.get('features', []),
        'detection_result': data.get('detection_result', 'normal'),
        'timestamp': data.get('timestamp', datetime.now().isoformat())
    }
    learning_data.append(learning_point)
    
    return jsonify({
        'success': True,
        'data_points': len(learning_data),
        'message': 'Learning data added'
    })

@app.route('/api/wearable/status', methods=['GET'])
def wearable_status():
    """Get wearable detection status."""
    confidence = random.uniform(0.6, 0.95)
    status = 'worn' if confidence > 0.7 else 'uncertain'
    
    return jsonify({
        'status': status,
        'confidence': round(confidence, 2),
        'factors': {
            'skin_temperature': round(random.uniform(0.7, 0.9), 2),
            'heart_rate': round(random.uniform(0.8, 0.95), 2),
            'motion': round(random.uniform(0.5, 0.8), 2),
            'orientation': round(random.uniform(0.7, 0.9), 2),
            'body_contact': round(random.uniform(0.8, 0.95), 2)
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/connection/status', methods=['GET'])
def connection_status():
    """Get connection status."""
    return jsonify({
        'connected': True,
        'signal_strength': random.randint(-30, -70),
        'ping_ms': random.randint(5, 50),
        'last_seen': datetime.now().isoformat(),
        'in_range': True
    })

@app.route('/api/location/current', methods=['GET'])
def current_location():
    """Get current location."""
    return jsonify({
        'latitude': round(random.uniform(40.7, 40.8), 6),
        'longitude': round(random.uniform(-74.0, -73.9), 6),
        'address': '123 Main St, New York, NY',
        'accuracy': round(random.uniform(5, 20), 1),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health/current', methods=['GET'])
def current_health():
    """Get current health status."""
    return jsonify({
        'heart_rate': random.randint(65, 85),
        'temperature': round(random.uniform(36.0, 37.5), 1),
        'spo2': random.randint(95, 100),
        'activity_level': random.choice(['low', 'moderate', 'high']),
        'status': 'normal',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/battery/status', methods=['GET'])
def battery_status():
    """Get battery status."""
    current_level = sensor_data['battery']['level']
    return jsonify({
        'level': round(current_level, 1),
        'percentage': int(current_level),
        'voltage': round(3.0 + (current_level / 100) * 1.2, 2),
        'charging': random.choice([True, False]),
        'estimated_hours': round(current_level / 20, 1),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/dashboard/realtime', methods=['GET'])
def realtime_dashboard():
    """Get real-time dashboard data."""
    return jsonify({
        'sensor_data': sensor_data,
        'alerts': alerts[-5:],  # Last 5 alerts
        'system_status': 'operational',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analytics/historical', methods=['GET'])
def historical_analytics():
    """Get historical analytics."""
    return jsonify({
        'data': {
            'falls': random.randint(0, 5),
            'alerts': len(alerts),
            'uptime_hours': 24,
            'battery_cycles': random.randint(100, 200)
        },
        'analytics': {
            'avg_heart_rate': 72,
            'avg_temperature': 36.8,
            'activity_distribution': {'low': 40, 'moderate': 35, 'high': 25}
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/users/profile', methods=['GET'])
def user_profile():
    """Get user profile."""
    return jsonify({
        'patient_id': 'demo_patient',
        'name': 'John Doe',
        'age': 75,
        'guardians': ['guardian_001', 'guardian_002'],
        'medical_conditions': ['Hypertension', 'Diabetes'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/config/settings', methods=['GET'])
def config_settings():
    """Get configuration settings."""
    return jsonify({
        'alert_thresholds': {
            'fall_sensitivity': 0.8,
            'heart_rate_min': 60,
            'heart_rate_max': 100,
            'temperature_min': 36.0,
            'temperature_max': 37.5
        },
        'notification_settings': {
            'sms_enabled': True,
            'email_enabled': True,
            'push_enabled': True
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/emergency/test', methods=['POST'])
def test_emergency():
    """Test emergency response."""
    data = request.get_json()
    alert = {
        'id': len(alerts) + 1,
        'type': 'emergency',
        'message': f"Emergency test: {data.get('type', 'Unknown')}",
        'priority': 'emergency',
        'location': data.get('location', {}),
        'medical_info': data.get('medical_info', {}),
        'timestamp': datetime.now().isoformat()
    }
    alerts.append(alert)
    
    return jsonify({
        'success': True,
        'alert_id': alert['id'],
        'message': 'Emergency test processed'
    })

@app.route('/api/system/health', methods=['GET'])
def system_health():
    """Get system health."""
    return jsonify({
        'status': 'healthy',
        'components': {
            'sensors': 'operational',
            'alerts': 'operational',
            'learning': 'operational',
            'communication': 'operational'
        },
        'performance': {
            'cpu_usage': round(random.uniform(10, 30), 1),
            'memory_usage': round(random.uniform(20, 40), 1),
            'disk_usage': round(random.uniform(5, 15), 1)
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analytics/advanced', methods=['GET'])
def advanced_analytics():
    """Get advanced analytics."""
    return jsonify({
        'insights': {
            'fall_risk': round(random.uniform(0.1, 0.3), 2),
            'health_score': round(random.uniform(0.7, 0.95), 2),
            'activity_trend': 'stable',
            'compliance_rate': round(random.uniform(0.8, 0.95), 2)
        },
        'metrics': {
            'model_accuracy': round(random.uniform(0.85, 0.95), 2),
            'false_positive_rate': round(random.uniform(0.05, 0.15), 2),
            'response_time_avg': round(random.uniform(1.0, 3.0), 1)
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all alerts."""
    return jsonify({
        'alerts': alerts,
        'total': len(alerts),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/learning/insights', methods=['GET'])
def learning_insights():
    """Get learning insights."""
    return jsonify({
        'patient_insights': {
            'fall_risk_score': 0.25,
            'health_trend': 'stable',
            'activity_pattern': 'normal',
            'recommendations': [
                'Continue regular monitoring',
                'Maintain current medication schedule',
                'Daily light exercise recommended'
            ]
        },
        'model_performance': {
            'accuracy': 0.92,
            'precision': 0.89,
            'recall': 0.94,
            'data_points': len(learning_data)
        },
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Backend API for Testing...")
    print("📡 Available on: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("📊 Sensor data: http://localhost:5000/api/sensors/current")
    print("🚨 Fall detection: http://localhost:5000/api/fall/detect")
    print("📚 Learning data: http://localhost:5000/api/learning/data")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
