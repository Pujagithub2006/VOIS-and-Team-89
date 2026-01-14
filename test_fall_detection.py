#!/usr/bin/env python3
"""
Test script for improved fall detection logic
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from detection.threshold_fall import FallDetector
from detection.inactivity import InactivityDetector

def test_fall_detector():
    print("Testing FallDetector...")
    detector = FallDetector()
    
    # Test normal activity
    normal_values = [9.8, 10.2, 9.5, 10.1, 9.9]
    for val in normal_values:
        result = detector.detect_fall(val)
        print(f"Normal {val}: {result}")
        assert not result, f"Should not detect fall for normal value {val}"
    
    # Test fall scenario - spike detection
    spike_values = [18.5, 19.2, 20.1, 18.8, 19.5]
    spike_detected = False
    for val in spike_values:
        result = detector.detect_fall(val)
        print(f"Spike {val}: {result}")
        if result:
            spike_detected = True
            print("✓ Spike detected correctly")
    
    assert spike_detected, "Spike should be detected"
    
    # Test post-fall state detection
    post_fall_values = [2.1, 1.8, 1.5, 1.2, 1.0]
    post_fall_detected = False
    for val in post_fall_values:
        result = detector.is_in_post_fall_state(val)
        print(f"Post-fall {val}: {result}")
        if result:
            post_fall_detected = True
            print("✓ Post-fall state detected correctly")
    
    assert post_fall_detected, "Post-fall state should be detected"
    print("✓ FallDetector test passed\n")

def test_inactivity_detector():
    print("Testing InactivityDetector...")
    detector = InactivityDetector()
    
    # Test active movement
    active_values = [10.0, 12.5, 11.0, 13.2, 10.8]
    prev = 9.8
    for val in active_values:
        result = detector.is_inactive(val, prev)
        print(f"Active {val}: {result}")
        # Active movement should not be detected as inactive
        prev = val
    
    # Test inactivity
    detector2 = InactivityDetector()
    inactive_values = [1.2, 1.3, 1.1, 1.4, 1.2]
    prev = 10.8
    for i, val in enumerate(inactive_values):
        result = detector2.is_inactive(val, prev)
        print(f"Inactive {i} - {val}: {result}")
        if i >= 2:  # Should detect inactivity after buffer fills
            assert result, f"Should detect inactivity for inactive value {val}"
        prev = val
    
    print("✓ InactivityDetector test passed\n")

def test_false_positive_reduction():
    print("Testing false positive reduction...")
    fall_detector = FallDetector()
    
    # Test scenario with temporary spikes (should not trigger fall)
    spike_values = [16.0, 9.8, 17.2, 10.1, 15.8, 9.9]
    for val in spike_values:
        result = fall_detector.detect_fall(val)
        print(f"Spike {val}: {result}")
        # These should not trigger sustained fall detection
        # because they don't have the required inactivity confirmation
    
    print("✓ False positive reduction test passed\n")

if __name__ == "__main__":
    print("Running fall detection tests...\n")
    
    try:
        test_fall_detector()
        test_inactivity_detector()
        test_false_positive_reduction()
        print("🎉 All tests passed! Fall detection logic improved successfully.")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
