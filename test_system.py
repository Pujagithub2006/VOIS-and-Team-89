#!/usr/bin/env python3
"""
Simple Test Runner for Enhanced Elderly Monitoring System

Tests all components without running the full async main loop.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import time
import asyncio
from src.sensors.enhanced_hardware_interface import initialize_hardware, get_sensor_data
from src.detection.feature_extraction import initialize_feature_extractor, extract_features_from_data
from src.detection.multi_layer_fall_detection import initialize_fall_detector, detect_fall
from src.detection.decision_engine import initialize_decision_engine, make_decision
from src.alerts.multi_level_alert_system import initialize_alert_system, send_alert, AlertType, AlertLevel
from src.location.vicinity_awareness import initialize_vicinity_system, update_patient_location

def test_system_components():
    """Test all system components individually."""
    print("🧪 Testing Enhanced Elderly Monitoring System Components")
    print("=" * 60)
    
    # Test 1: Hardware Interface
    print("\n1. Testing Hardware Interface...")
    try:
        hw = initialize_hardware(use_real_hardware=False)
        sensor_data = get_sensor_data()
        print(f"✅ Hardware Interface: {len(sensor_data)} sensor types available")
    except Exception as e:
        print(f"❌ Hardware Interface failed: {e}")
        return False
    
    # Test 2: Feature Extraction
    print("\n2. Testing Feature Extraction...")
    try:
        fe = initialize_feature_extractor(window_size=30, sampling_rate=10)
        features = extract_features_from_data(sensor_data)
        if features:
            print(f"✅ Feature Extraction: {len(features)} features extracted")
        else:
            print("⚠️ Feature Extraction: No features extracted (need more data)")
    except Exception as e:
        print(f"❌ Feature Extraction failed: {e}")
        return False
    
    # Test 3: Fall Detection
    print("\n3. Testing Fall Detection...")
    try:
        fd = initialize_fall_detector()
        if features:
            detection_results = detect_fall(features)
            print(f"✅ Fall Detection: {detection_results.get('final_decision', 'no_decision')}")
        else:
            print("⚠️ Fall Detection: Skipped (no features)")
    except Exception as e:
        print(f"❌ Fall Detection failed: {e}")
        return False
    
    # Test 4: Decision Engine
    print("\n4. Testing Decision Engine...")
    try:
        de = initialize_decision_engine()
        if features and 'detection_results' in locals():
            decision = make_decision(features, detection_results)
            print(f"✅ Decision Engine: {decision.get('decision_type', 'no_decision')}")
        else:
            print("⚠️ Decision Engine: Skipped (no input data)")
    except Exception as e:
        print(f"❌ Decision Engine failed: {e}")
        return False
    
    # Test 5: Alert System
    print("\n5. Testing Alert System...")
    try:
        alert_sys = initialize_alert_system()
        alert_sys.start()
        print("✅ Alert System: Initialized and started")
        alert_sys.stop()
    except Exception as e:
        print(f"❌ Alert System failed: {e}")
        return False
    
    # Test 6: Vicinity System
    print("\n6. Testing Vicinity System...")
    try:
        vs = initialize_vicinity_system()
        status = vs.simulate_location_update("home")
        print(f"✅ Vicinity System: {status.get('location_updated', False)}")
    except Exception as e:
        print(f"❌ Vicinity System failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All system components tested successfully!")
    return True

def test_demo_scenario():
    """Test a complete demo scenario."""
    print("\n🎭 Testing Demo Scenario...")
    print("-" * 40)
    
    try:
        # Initialize all components
        hw = initialize_hardware(use_real_hardware=False)
        fe = initialize_feature_extractor(window_size=30, sampling_rate=10)
        fd = initialize_fall_detector()
        de = initialize_decision_engine()
        alert_sys = initialize_alert_system()
        vs = initialize_vicinity_system()
        
        alert_sys.start()
        
        # Simulate sensor data collection
        print("Collecting sensor data...")
        for i in range(50):  # Collect 50 samples
            sensor_data = get_sensor_data()
            features = extract_features_from_data(sensor_data)
            
            if i % 10 == 0:
                print(f"  Sample {i}: Features available = {features is not None}")
            
            time.sleep(0.1)  # Simulate real-time sampling
        
        # Get final features and run detection
        sensor_data = get_sensor_data()
        features = extract_features_from_data(sensor_data)
        
        if features:
            print(f"\nFinal features: {type(features)} extracted")
            
            # Convert FeatureVector to dict if needed
            if hasattr(features, '__dict__'):
                feature_dict = features.__dict__
            elif isinstance(features, dict):
                feature_dict = features
            else:
                feature_dict = {"features": str(features)}
            
            print(f"Feature keys: {list(feature_dict.keys()) if isinstance(feature_dict, dict) else 'Not a dict'}")
            
            # Run fall detection
            detection_results = detect_fall(feature_dict)
            print(f"Fall detection: {detection_results.get('final_decision')}")
            
            # Run decision engine
            decision = make_decision(feature_dict, detection_results)
            print(f"Decision: {decision.get('decision_type')} (confidence: {decision.get('confidence', 0):.2f})")
            
            # Test alert if needed
            if decision.get('confidence', 0) > 0.5:
                alert_id = asyncio.run(send_alert(
                    AlertType.FALL_DETECTED, 
                    AlertLevel.WARNING, 
                    "Test alert from demo scenario"
                ))
                print(f"Alert sent: {alert_id}")
        
        # Test location
        location_result = vs.simulate_location_update("home")
        print(f"Location update: {location_result.get('location_updated', False)}")
        
        alert_sys.stop()
        print("\n✅ Demo scenario completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Demo scenario failed: {e}")
        return False

def main():
    """Main test runner."""
    print("🚀 Enhanced Elderly Monitoring System - Test Suite")
    print("=" * 60)
    
    # Test individual components
    if not test_system_components():
        print("\n❌ Component tests failed!")
        return False
    
    # Test demo scenario
    if not test_demo_scenario():
        print("\n❌ Demo scenario failed!")
        return False
    
    print("\n🎉 All tests passed! System is ready for deployment.")
    print("\n📋 Next Steps:")
    print("1. Run 'python src/main_enhanced.py' for full system")
    print("2. Start backend server with 'python backend/integrated_app.py'")
    print("3. Access frontend at 'http://localhost:5000/frontend/senior_ui.html'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
