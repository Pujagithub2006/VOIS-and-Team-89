"""
Quick Start Testing Script

Simple script to quickly test all features without complex setup.
Perfect for verifying the system works before detailed testing.

Usage:
    python quick_start_test.py
"""

import requests
import time
from datetime import datetime

def test_service(name, url, expected_status=200):
    """Test if a service is running."""
    try:
        response = requests.get(url, timeout=5)
        success = response.status_code == expected_status
        print(f"{'✅' if success else '❌'} {name}: {'Running' if success else 'Not Running'}")
        return success
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def test_feature(name, url, method="GET", data=None):
    """Test a specific feature."""
    try:
        if method == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        success = response.status_code in [200, 201]
        print(f"{'✅' if success else '❌'} {name}: {'Working' if success else 'Not Working'}")
        return success
    except Exception as e:
        print(f"❌ {name}: Error - {e}")
        return False

def main():
    print("🧪 Quick Start System Test")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test basic services
    print("📡 Testing Services:")
    backend_ok = test_service("Backend API", "http://localhost:5000/api/health")
    gsm_ok = test_service("GSM API", "http://localhost:5002/api/gsm/status")
    
    print()
    print("🔍 Testing Core Features:")
    
    # Test core features
    features = [
        ("Fall Detection", "http://localhost:5000/api/fall/detect", "POST", 
         {"acceleration": [0.1, 0.2, 15.0], "gyroscope": [0.0, 0.0, 0.0]}),
        ("Sensor Monitoring", "http://localhost:5000/api/sensors/current"),
        ("Alert System", "http://localhost:5000/api/alerts/test", "POST",
         {"type": "test_alert", "message": "Test alert", "priority": "low"}),
        ("Learning System", "http://localhost:5000/api/learning/data", "POST",
         {"patient_id": "test", "features": [1.2, 0.8, 9.8], "detection_result": "normal"}),
        ("Wearable Detection", "http://localhost:5000/api/wearable/status"),
        ("Connection Monitoring", "http://localhost:5000/api/connection/status"),
        ("GSM Communication", "http://localhost:5002/api/gsm/sms/send", "POST",
         {"guardian_id": "test", "message": "Test message", "priority": "normal"}),
        ("Location Monitoring", "http://localhost:5000/api/location/current"),
        ("Health Monitoring", "http://localhost:5000/api/health/current"),
        ("Battery Management", "http://localhost:5000/api/battery/status"),
    ]
    
    results = []
    for name, url, *rest in features:
        if len(rest) == 2:
            method, data = rest
        elif len(rest) == 1:
            method = rest[0]
            data = None
        else:
            method = "GET"
            data = None
        
        result = test_feature(name, url, method, data)
        results.append(result)
        time.sleep(0.2)  # Small delay
    
    print()
    print("📊 Test Summary:")
    total = len(results) + 2  # +2 for backend and gsm services
    passed = sum(results) + (1 if backend_ok else 0) + (1 if gsm_ok else 0)
    percentage = (passed / total) * 100
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {percentage:.1f}%")
    
    print()
    if percentage >= 80:
        print("🎉 System is working well!")
    elif percentage >= 60:
        print("⚠️ System partially working - some features may need attention")
    else:
        print("🚨 System has issues - check services and configuration")
    
    print()
    print("🌐 Open these URLs in your browser:")
    print("   Senior Dashboard: http://localhost:8000/senior_dashboard.html")
    print("   Guardian Dashboard: http://localhost:8000/guardian_dashboard.html")
    print("   Learning Analytics: http://localhost:8000/frontend/learning_analytics.html")
    print("   GSM Communication: http://localhost:8000/frontend/gsm_communication.html")

if __name__ == '__main__':
    main()
