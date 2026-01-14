"""
Advanced Sensor Simulation Layer for Elderly Monitoring System

Pattern-based, time-based, realistic sensor simulation with multiple activity states.
Supports both SIMULATION and REAL_HARDWARE modes.
"""

import time
import math
import random
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import json

class ActivityState(Enum):
    """Different activity states for realistic simulation."""
    NORMAL_WALKING = "normal_walking"
    SITTING = "sitting"
    SLEEPING = "sleeping"
    FALL_FORWARD = "fall_forward"
    FALL_SIDEWAYS = "fall_sideways"
    SUDDEN_COLLAPSE = "sudden_collapse"
    NO_MOVEMENT = "no_movement"
    PANIC_BUTTON = "panic_button"
    LOW_BATTERY = "low_battery"
    RECOVERY = "recovery"

class SensorSimulationMode(Enum):
    """Simulation mode selection."""
    SIMULATION = "SIMULATION"
    REAL_HARDWARE = "REAL_HARDWARE"

class AdvancedSensorSimulator:
    """Advanced sensor simulator with pattern-based realistic data."""
    
    def __init__(self, mode: str = "SIMULATION"):
        self.mode = SensorSimulationMode(mode)
        self.current_state = ActivityState.NORMAL_WALKING
        self.state_start_time = time.time()
        self.simulation_time = 0
        self.is_running = False
        self.simulation_thread = None
        
        # Base sensor values for different states
        self.state_patterns = {
            ActivityState.NORMAL_WALKING: {
                'duration': (30, 120),  # 30-120 seconds
                'acceleration': {'x': (-0.5, 0.5), 'y': (-0.3, 0.3), 'z': (8.5, 10.5)},
                'gyroscope': {'x': (-0.5, 0.5), 'y': (-0.3, 0.3), 'z': (-0.1, 0.1)},
                'heart_rate': (70, 90),
                'temperature': (36.5, 37.0),
                'spo2': (95, 100),
                'battery_drain': 0.01
            },
            ActivityState.SITTING: {
                'duration': (60, 300),  # 1-5 minutes
                'acceleration': {'x': (-0.1, 0.1), 'y': (-0.1, 0.1), 'z': (9.5, 10.0)},
                'gyroscope': {'x': (-0.05, 0.05), 'y': (-0.05, 0.05), 'z': (-0.02, 0.02)},
                'heart_rate': (60, 75),
                'temperature': (36.3, 36.8),
                'spo2': (96, 100),
                'battery_drain': 0.005
            },
            ActivityState.SLEEPING: {
                'duration': (300, 600),  # 5-10 minutes
                'acceleration': {'x': (-0.05, 0.05), 'y': (-0.05, 0.05), 'z': (9.7, 10.0)},
                'gyroscope': {'x': (-0.02, 0.02), 'y': (-0.02, 0.02), 'z': (-0.01, 0.01)},
                'heart_rate': (55, 70),
                'temperature': (36.0, 36.5),
                'spo2': (97, 100),
                'battery_drain': 0.003
            },
            ActivityState.FALL_FORWARD: {
                'duration': (2, 5),  # 2-5 seconds
                'acceleration': {'x': (2.0, 4.0), 'y': (-1.0, 1.0), 'z': (-5.0, -15.0)},
                'gyroscope': {'x': (3.0, 6.0), 'y': (1.0, 3.0), 'z': (2.0, 4.0)},
                'heart_rate': (80, 120),
                'temperature': (36.5, 37.0),
                'spo2': (90, 98),
                'battery_drain': 0.05
            },
            ActivityState.FALL_SIDEWAYS: {
                'duration': (2, 5),  # 2-5 seconds
                'acceleration': {'x': (-4.0, -2.0), 'y': (2.0, 4.0), 'z': (-5.0, -15.0)},
                'gyroscope': {'x': (1.0, 3.0), 'y': (3.0, 6.0), 'z': (2.0, 4.0)},
                'heart_rate': (80, 120),
                'temperature': (36.5, 37.0),
                'spo2': (90, 98),
                'battery_drain': 0.05
            },
            ActivityState.SUDDEN_COLLAPSE: {
                'duration': (1, 3),  # 1-3 seconds
                'acceleration': {'x': (-6.0, -3.0), 'y': (-6.0, -3.0), 'z': (-8.0, -20.0)},
                'gyroscope': {'x': (5.0, 8.0), 'y': (5.0, 8.0), 'z': (4.0, 7.0)},
                'heart_rate': (90, 140),
                'temperature': (36.5, 37.0),
                'spo2': (85, 95),
                'battery_drain': 0.08
            },
            ActivityState.NO_MOVEMENT: {
                'duration': (60, 180),  # 1-3 minutes
                'acceleration': {'x': (-0.02, 0.02), 'y': (-0.02, 0.02), 'z': (9.8, 10.0)},
                'gyroscope': {'x': (-0.01, 0.01), 'y': (-0.01, 0.01), 'z': (-0.005, 0.005)},
                'heart_rate': (50, 65),
                'temperature': (35.5, 36.0),
                'spo2': (88, 95),
                'battery_drain': 0.004
            },
            ActivityState.PANIC_BUTTON: {
                'duration': (5, 10),  # 5-10 seconds
                'acceleration': {'x': (-0.2, 0.2), 'y': (-0.2, 0.2), 'z': (9.5, 10.0)},
                'gyroscope': {'x': (-0.1, 0.1), 'y': (-0.1, 0.1), 'z': (-0.05, 0.05)},
                'heart_rate': (100, 140),
                'temperature': (36.5, 37.0),
                'spo2': (95, 100),
                'battery_drain': 0.02
            },
            ActivityState.LOW_BATTERY: {
                'duration': (120, 300),  # 2-5 minutes
                'acceleration': {'x': (-0.1, 0.1), 'y': (-0.1, 0.1), 'z': (9.5, 10.0)},
                'gyroscope': {'x': (-0.05, 0.05), 'y': (-0.05, 0.05), 'z': (-0.02, 0.02)},
                'heart_rate': (60, 75),
                'temperature': (36.3, 36.8),
                'spo2': (96, 100),
                'battery_drain': 0.1
            },
            ActivityState.RECOVERY: {
                'duration': (30, 90),  # 30-90 seconds
                'acceleration': {'x': (-0.2, 0.2), 'y': (-0.2, 0.2), 'z': (9.0, 10.0)},
                'gyroscope': {'x': (-0.1, 0.1), 'y': (-0.1, 0.1), 'z': (-0.05, 0.05)},
                'heart_rate': (75, 95),
                'temperature': (36.5, 37.0),
                'spo2': (94, 99),
                'battery_drain': 0.02
            }
        }
        
        # Current sensor values
        self.current_values = {
            'acceleration': {'x': 0.0, 'y': 0.0, 'z': 9.8},
            'gyroscope': {'x': 0.0, 'y': 0.0, 'z': 0.0},
            'heart_rate': 72,
            'temperature': 36.8,
            'spo2': 98,
            'battery_level': 85.0,
            'is_worn': True,
            'panic_pressed': False,
            'device_connected': True
        }
        
        # State transition probabilities
        self.state_transitions = {
            ActivityState.NORMAL_WALKING: [
                (ActivityState.SITTING, 0.3),
                (ActivityState.FALL_FORWARD, 0.05),
                (ActivityState.FALL_SIDEWAYS, 0.05),
                (ActivityState.PANIC_BUTTON, 0.02)
            ],
            ActivityState.SITTING: [
                (ActivityState.NORMAL_WALKING, 0.4),
                (ActivityState.SLEEPING, 0.2),
                (ActivityState.FALL_FORWARD, 0.02),
                (ActivityState.PANIC_BUTTON, 0.01)
            ],
            ActivityState.SLEEPING: [
                (ActivityState.SITTING, 0.3),
                (ActivityState.NORMAL_WALKING, 0.2),
                (ActivityState.NO_MOVEMENT, 0.05)
            ],
            ActivityState.FALL_FORWARD: [
                (ActivityState.NO_MOVEMENT, 0.4),
                (ActivityState.RECOVERY, 0.6)
            ],
            ActivityState.FALL_SIDEWAYS: [
                (ActivityState.NO_MOVEMENT, 0.4),
                (ActivityState.RECOVERY, 0.6)
            ],
            ActivityState.SUDDEN_COLLAPSE: [
                (ActivityState.NO_MOVEMENT, 0.7),
                (ActivityState.RECOVERY, 0.3)
            ],
            ActivityState.NO_MOVEMENT: [
                (ActivityState.RECOVERY, 0.3),
                (ActivityState.NORMAL_WALKING, 0.2)
            ],
            ActivityState.PANIC_BUTTON: [
                (ActivityState.NORMAL_WALKING, 0.8),
                (ActivityState.SITTING, 0.2)
            ],
            ActivityState.LOW_BATTERY: [
                (ActivityState.NORMAL_WALKING, 0.3),
                (ActivityState.SITTING, 0.5)
            ],
            ActivityState.RECOVERY: [
                (ActivityState.NORMAL_WALKING, 0.6),
                (ActivityState.SITTING, 0.4)
            ]
        }
        
        # Callbacks for real-time updates
        self.callbacks = []
        
    def add_callback(self, callback):
        """Add callback function for real-time sensor updates."""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove callback function."""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_callbacks(self, sensor_data):
        """Notify all callbacks with new sensor data."""
        for callback in self.callbacks:
            try:
                callback(sensor_data)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def _generate_sensor_value(self, base_range, current_value, smooth_factor=0.3):
        """Generate smooth sensor value within range."""
        min_val, max_val = base_range
        target = random.uniform(min_val, max_val)
        # Smooth transition
        new_value = current_value + (target - current_value) * smooth_factor
        return new_value
    
    def _update_sensor_values(self):
        """Update sensor values based on current state."""
        pattern = self.state_patterns[self.current_state]
        
        # Update acceleration
        for axis in ['x', 'y', 'z']:
            range_val = pattern['acceleration'][axis]
            self.current_values['acceleration'][axis] = self._generate_sensor_value(
                range_val, self.current_values['acceleration'][axis], 0.4
            )
        
        # Update gyroscope
        for axis in ['x', 'y', 'z']:
            range_val = pattern['gyroscope'][axis]
            self.current_values['gyroscope'][axis] = self._generate_sensor_value(
                range_val, self.current_values['gyroscope'][axis], 0.4
            )
        
        # Update vitals
        self.current_values['heart_rate'] = int(self._generate_sensor_value(
            pattern['heart_rate'], self.current_values['heart_rate'], 0.2
        ))
        self.current_values['temperature'] = round(self._generate_sensor_value(
            pattern['temperature'], self.current_values['temperature'], 0.1
        ), 1)
        self.current_values['spo2'] = int(self._generate_sensor_value(
            pattern['spo2'], self.current_values['spo2'], 0.15
        ))
        
        # Update battery
        self.current_values['battery_level'] = max(0, 
            self.current_values['battery_level'] - pattern['battery_drain']
        )
        
        # Update state-specific values
        if self.current_state == ActivityState.PANIC_BUTTON:
            self.current_values['panic_pressed'] = True
        else:
            self.current_values['panic_pressed'] = False
        
        if self.current_state == ActivityState.NO_MOVEMENT:
            self.current_values['is_worn'] = False
        else:
            self.current_values['is_worn'] = True
        
        if self.current_state == ActivityState.LOW_BATTERY:
            self.current_values['battery_level'] = min(15, self.current_values['battery_level'])
    
    def _should_transition_state(self):
        """Check if current state should transition."""
        elapsed = time.time() - self.state_start_time
        min_duration, max_duration = self.state_patterns[self.current_state]['duration']
        
        if elapsed < min_duration:
            return False, None
        
        if elapsed > max_duration:
            transitions = self.state_transitions.get(self.current_state, [])
            if transitions:
                # Weighted random selection
                total_weight = sum(weight for _, weight in transitions)
                rand_val = random.uniform(0, total_weight)
                cumulative = 0
                for state, weight in transitions:
                    cumulative += weight
                    if rand_val <= cumulative:
                        return True, state
        
        return False, None
    
    def _transition_to_state(self, new_state):
        """Transition to new activity state."""
        self.current_state = new_state
        self.state_start_time = time.time()
        print(f"🔄 State transition: {new_state.value}")
    
    def _simulation_loop(self):
        """Main simulation loop."""
        while self.is_running:
            try:
                # Update sensor values
                self._update_sensor_values()
                
                # Check for state transitions
                should_transition, new_state = self._should_transition_state()
                if should_transition and new_state:
                    self._transition_to_state(new_state)
                
                # Create sensor data packet
                sensor_data = {
                    'timestamp': datetime.now().isoformat(),
                    'state': self.current_state.value,
                    'acceleration': self.current_values['acceleration'].copy(),
                    'gyroscope': self.current_values['gyroscope'].copy(),
                    'heart_rate': self.current_values['heart_rate'],
                    'temperature': self.current_values['temperature'],
                    'spo2': self.current_values['spo2'],
                    'battery_level': round(self.current_values['battery_level'], 1),
                    'is_worn': self.current_values['is_worn'],
                    'panic_pressed': self.current_values['panic_pressed'],
                    'device_connected': self.current_values['device_connected']
                }
                
                # Notify callbacks
                self._notify_callbacks(sensor_data)
                
                # Sleep for realistic update rate
                time.sleep(0.1)  # 10Hz update rate
                
            except Exception as e:
                print(f"Simulation error: {e}")
                time.sleep(1)
    
    def start_simulation(self):
        """Start the sensor simulation."""
        if self.mode != SensorSimulationMode.SIMULATION:
            print("❌ Simulation mode not enabled")
            return False
        
        if self.is_running:
            print("⚠️ Simulation already running")
            return True
        
        self.is_running = True
        self.simulation_thread = threading.Thread(target=self._simulation_loop, daemon=True)
        self.simulation_thread.start()
        print("🚀 Sensor simulation started")
        return True
    
    def stop_simulation(self):
        """Stop the sensor simulation."""
        self.is_running = False
        if self.simulation_thread:
            self.simulation_thread.join(timeout=2)
        print("⏹️ Sensor simulation stopped")
    
    def force_state(self, state: ActivityState):
        """Force transition to specific state (for demo control)."""
        self._transition_to_state(state)
    
    def get_current_state(self) -> ActivityState:
        """Get current activity state."""
        return self.current_state
    
    def get_sensor_data(self) -> Dict[str, Any]:
        """Get current sensor data."""
        return {
            'timestamp': datetime.now().isoformat(),
            'state': self.current_state.value,
            'acceleration': self.current_values['acceleration'].copy(),
            'gyroscope': self.current_values['gyroscope'].copy(),
            'heart_rate': self.current_values['heart_rate'],
            'temperature': self.current_values['temperature'],
            'spo2': self.current_values['spo2'],
            'battery_level': round(self.current_values['battery_level'], 1),
            'is_worn': self.current_values['is_worn'],
            'panic_pressed': self.current_values['panic_pressed'],
            'device_connected': self.current_values['device_connected']
        }

# Global simulator instance
_simulator = None

def initialize_sensor_simulator(mode: str = "SIMULATION") -> AdvancedSensorSimulator:
    """Initialize the global sensor simulator."""
    global _simulator
    _simulator = AdvancedSensorSimulator(mode)
    return _simulator

def get_sensor_simulator() -> Optional[AdvancedSensorSimulator]:
    """Get the global sensor simulator instance."""
    return _simulator

def simulate_fall_forward():
    """Simulate a forward fall."""
    if _simulator:
        _simulator.force_state(ActivityState.FALL_FORWARD)

def simulate_fall_sideways():
    """Simulate a sideways fall."""
    if _simulator:
        _simulator.force_state(ActivityState.FALL_SIDEWAYS)

def simulate_sudden_collapse():
    """Simulate sudden collapse."""
    if _simulator:
        _simulator.force_state(ActivityState.SUDDEN_COLLAPSE)

def simulate_panic_button():
    """Simulate panic button press."""
    if _simulator:
        _simulator.force_state(ActivityState.PANIC_BUTTON)

def simulate_low_battery():
    """Simulate low battery."""
    if _simulator:
        _simulator.force_state(ActivityState.LOW_BATTERY)

def simulate_no_movement():
    """Simulate no movement (unconscious)."""
    if _simulator:
        _simulator.force_state(ActivityState.NO_MOVEMENT)

def reset_to_normal():
    """Reset to normal walking state."""
    if _simulator:
        _simulator.force_state(ActivityState.NORMAL_WALKING)
