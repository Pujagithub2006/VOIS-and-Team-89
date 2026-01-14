"""
Enhanced Hardware Abstraction Layer for Complete Elderly Monitoring System

Supports all required sensors:
- MPU6050: Motion + Orientation (ax, ay, az, gx, gy, gz)
- MAX30102: Heart Rate & SpO₂
- DS18B20: Body contact + temperature
- Buzzer: Local alert system
- GSM: Remote alert (SIM800)
- Battery: Power management
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, Any
import time
import random
import math
import threading
from datetime import datetime

class SensorInterface(ABC):
    """Abstract base class for all sensor data sources."""
    
    @abstractmethod
    def get_motion_data(self) -> Dict[str, Any]:
        """Get complete motion data (ax, ay, az, gx, gy, gz)."""
        pass
    
    @abstractmethod
    def get_vitals_data(self) -> Dict[str, Any]:
        """Get vitals data (heart_rate, spo2, temperature, contact)."""
        pass
    
    @abstractmethod
    def get_battery_data(self) -> Dict[str, Any]:
        """Get battery data (level, voltage, charging)."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if sensor is connected and operational."""
        pass
    
    @abstractmethod
    def calibrate(self) -> bool:
        """Calibrate sensor. Returns True if successful."""
        pass
    
    @abstractmethod
    def get_device_status(self) -> Dict[str, Any]:
        """Get device status (worn, battery, sensors)."""
        pass

class EnhancedSimulatedSensor(SensorInterface):
    """Enhanced simulated sensor for complete waist-band monitoring."""
    
    def __init__(self, mode: str = "normal"):
        """
        Initialize enhanced simulated sensor.
        
        Args:
            mode: "normal", "sitting", "lying", "fall", "demo", "walking", "instability"
        """
        self.mode = mode
        self.demo_timer = 0
        self.demo_sequence = ["normal", "normal", "normal", "fall", "lying", "lying"]
        self.connected = True
        self.worn = True  # Device is worn by default
        self.battery_level = 85.0
        self.battery_voltage = 3.7
        
        # Sensor noise and calibration
        self.accel_noise = 0.1
        self.gyro_noise = 0.5
        self.hr_noise = 2.0
        self.spo2_noise = 1.0
        self.temp_noise = 0.2
        
        # Baseline vitals
        self.baseline_hr = 72
        self.baseline_spo2 = 98
        self.baseline_temp = 36.6
        
        # State tracking
        self.time_counter = 0
        self.last_fall_time = 0
        self.pre_fall_risk = 0.0
        
        # Sensor failure simulation
        self.sensor_failures = {
            'accelerometer': False,
            'gyroscope': False,
            'heart_rate': False,
            'spo2': False,
            'temperature': False
        }
    
    def get_motion_data(self) -> Dict[str, Any]:
        """Get complete motion data with noise and sensor failures."""
        self.time_counter += 1
        
        # Simulate sensor failures
        if self.sensor_failures['accelerometer']:
            return self._get_fallback_motion_data()
        
        # Generate base motion based on mode
        motion = self._generate_base_motion()
        
        # Add sensor noise
        motion['ax'] += random.gauss(0, self.accel_noise)
        motion['ay'] += random.gauss(0, self.accel_noise)
        motion['az'] += random.gauss(0, self.accel_noise)
        motion['gx'] += random.gauss(0, self.gyro_noise)
        motion['gy'] += random.gauss(0, self.gyro_noise)
        motion['gz'] += random.gauss(0, self.gyro_noise)
        
        # Calculate derived features
        motion['magnitude'] = math.sqrt(motion['ax']**2 + motion['ay']**2 + motion['az']**2)
        motion['gyro_magnitude'] = math.sqrt(motion['gx']**2 + motion['gy']**2 + motion['gz']**2)
        
        # Calculate orientation (pitch, roll)
        motion['pitch'] = math.atan2(motion['ay'], math.sqrt(motion['ax']**2 + motion['az']**2)) * 180 / math.pi
        motion['roll'] = math.atan2(-motion['ax'], math.sqrt(motion['ay']**2 + motion['az']**2)) * 180 / math.pi
        
        # Calculate jerk (rate of change of acceleration)
        if hasattr(self, '_last_acceleration'):
            dt = 0.1  # 100ms sampling interval
            motion['jerk_x'] = (motion['ax'] - self._last_acceleration['ax']) / dt
            motion['jerk_y'] = (motion['ay'] - self._last_acceleration['ay']) / dt
            motion['jerk_z'] = (motion['az'] - self._last_acceleration['az']) / dt
            motion['jerk_magnitude'] = math.sqrt(motion['jerk_x']**2 + motion['jerk_y']**2 + motion['jerk_z']**2)
        else:
            motion['jerk_x'] = 0
            motion['jerk_y'] = 0
            motion['jerk_z'] = 0
            motion['jerk_magnitude'] = 0
        
        self._last_acceleration = {
            'ax': motion['ax'], 'ay': motion['ay'], 'az': motion['az']
        }
        
        motion['timestamp'] = datetime.now().isoformat()
        motion['sensor_status'] = 'normal'
        
        return motion
    
    def get_vitals_data(self) -> Dict[str, Any]:
        """Get vitals data with noise and sensor failures."""
        vitals = {}
        
        # Heart rate
        if not self.sensor_failures['heart_rate']:
            base_hr = self.baseline_hr
            if self.mode == "fall":
                base_hr = min(150, base_hr + random.uniform(20, 40))
            elif self.mode == "instability":
                base_hr = base_hr + random.uniform(-10, 15)
            elif self.mode == "walking":
                base_hr = base_hr + random.uniform(5, 20)
            
            vitals['heart_rate'] = max(40, min(200, base_hr + random.gauss(0, self.hr_noise)))
            vitals['hr_status'] = 'normal' if 60 <= vitals['heart_rate'] <= 100 else 'abnormal'
        else:
            vitals['heart_rate'] = None
            vitals['hr_status'] = 'sensor_failed'
        
        # SpO2
        if not self.sensor_failures['spo2']:
            base_spo2 = self.baseline_spo2
            if self.mode == "fall":
                base_spo2 = max(85, base_spo2 - random.uniform(5, 15))
            elif self.mode == "instability":
                base_spo2 = base_spo2 + random.uniform(-3, 3)
            
            vitals['spo2'] = max(80, min(100, base_spo2 + random.gauss(0, self.spo2_noise)))
            vitals['spo2_status'] = 'normal' if vitals['spo2'] >= 95 else 'low'
        else:
            vitals['spo2'] = None
            vitals['spo2_status'] = 'sensor_failed'
        
        # Temperature
        if not self.sensor_failures['temperature']:
            base_temp = self.baseline_temp
            if self.mode == "fall":
                base_temp = base_temp + random.uniform(-2, 1)
            
            vitals['temperature'] = base_temp + random.gauss(0, self.temp_noise)
            vitals['temp_status'] = 'normal' if 36.0 <= vitals['temperature'] <= 37.5 else 'abnormal'
        else:
            vitals['temperature'] = None
            vitals['temp_status'] = 'sensor_failed'
        
        # Body contact detection
        vitals['body_contact'] = self.worn and random.random() > 0.1  # 90% contact when worn
        vitals['contact_status'] = 'good' if vitals['body_contact'] else 'poor'
        
        vitals['timestamp'] = datetime.now().isoformat()
        return vitals
    
    def get_battery_data(self) -> Dict[str, Any]:
        """Get battery data with power management."""
        # Simulate battery drain
        if self.time_counter % 100 == 0:  # Every 10 seconds
            self.battery_level = max(0, self.battery_level - 0.01)
            self.battery_voltage = 3.7 * (self.battery_level / 100.0)
        
        battery = {
            'level': self.battery_level,
            'voltage': self.battery_voltage,
            'charging': False,
            'status': 'good' if self.battery_level > 20 else 'low',
            'estimated_hours': self.battery_level * 0.5  # Rough estimate
        }
        
        return battery
    
    def is_connected(self) -> bool:
        """Check if device is connected and operational."""
        return self.connected and self.battery_level > 5
    
    def calibrate(self) -> bool:
        """Calibrate all sensors."""
        print("🔧 Calibrating sensors...")
        
        # Simulate calibration process
        time.sleep(2)
        
        # Update baseline values
        self.baseline_hr = 72 + random.gauss(0, 5)
        self.baseline_spo2 = 98 + random.gauss(0, 1)
        self.baseline_temp = 36.6 + random.gauss(0, 0.2)
        
        print("✅ Calibration complete")
        return True
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get comprehensive device status."""
        return {
            'device_id': 'waist_band_001',
            'worn': self.worn,
            'battery': self.get_battery_data(),
            'sensors': {
                'accelerometer': not self.sensor_failures['accelerometer'],
                'gyroscope': not self.sensor_failures['gyroscope'],
                'heart_rate': not self.sensor_failures['heart_rate'],
                'spo2': not self.sensor_failures['spo2'],
                'temperature': not self.sensor_failures['temperature']
            },
            'mode': self.mode,
            'uptime': self.time_counter * 0.1,  # seconds
            'last_calibration': datetime.now().isoformat()
        }
    
    def _generate_base_motion(self) -> Dict[str, float]:
        """Generate base motion data based on current mode."""
        if self.mode == "demo":
            # Automatic demo sequence
            if self.demo_timer < len(self.demo_sequence):
                current_mode = self.demo_sequence[self.demo_timer // 20]
                if self.demo_timer % 20 == 0:
                    self.mode = current_mode
                self.demo_timer += 1
            else:
                self.mode = "lying"
        
        # Generate motion patterns
        if self.mode == "normal":
            # Normal walking/standing
            return {
                'ax': random.gauss(0, 0.5),
                'ay': random.gauss(0, 0.3),
                'az': random.gauss(9.8, 0.2),  # Gravity
                'gx': random.gauss(0, 0.5),
                'gy': random.gauss(0, 0.5),
                'gz': random.gauss(0, 0.5)
            }
        
        elif self.mode == "walking":
            # Walking pattern
            t = self.time_counter * 0.1
            return {
                'ax': 2.0 * math.sin(t * 2) + random.gauss(0, 0.3),
                'ay': 1.5 * math.cos(t * 2) + random.gauss(0, 0.2),
                'az': 9.8 + 0.5 * math.sin(t * 4) + random.gauss(0, 0.2),
                'gx': random.gauss(0, 1.0),
                'gy': random.gauss(0, 1.0),
                'gz': random.gauss(0, 1.0)
            }
        
        elif self.mode == "sitting":
            # Sitting - minimal motion
            return {
                'ax': random.gauss(0, 0.1),
                'ay': random.gauss(0, 0.1),
                'az': 9.8 + random.gauss(0, 0.1),
                'gx': random.gauss(0, 0.2),
                'gy': random.gauss(0, 0.2),
                'gz': random.gauss(0, 0.2)
            }
        
        elif self.mode == "lying":
            # Lying down - different orientation
            return {
                'ax': random.gauss(0, 0.1),
                'ay': random.gauss(0, 0.1),
                'az': 9.8 + random.gauss(0, 0.1),
                'gx': random.gauss(0, 0.2),
                'gy': random.gauss(0, 0.2),
                'gz': random.gauss(0, 0.2)
            }
        
        elif self.mode == "instability":
            # Pre-fall instability
            t = self.time_counter * 0.1
            instability = math.sin(t * 10) * 2.0  # Increasing instability
            return {
                'ax': instability * random.gauss(0, 1) + random.gauss(0, 0.5),
                'ay': instability * random.gauss(0, 1) + random.gauss(0, 0.3),
                'az': 9.8 + instability * 0.5 + random.gauss(0, 0.3),
                'gx': random.gauss(0, 2.0) + instability,
                'gy': random.gauss(0, 2.0) + instability,
                'gz': random.gauss(0, 2.0) + instability
            }
        
        elif self.mode == "fall":
            # Fall detection - sudden acceleration spike
            if self.time_counter - self.last_fall_time < 50:
                # During fall - high acceleration
                return {
                    'ax': random.gauss(0, 15),
                    'ay': random.gauss(0, 20),
                    'az': random.gauss(-25, 10),
                    'gx': random.gauss(0, 10),
                    'gy': random.gauss(0, 15),
                    'gz': random.gauss(0, 20)
                }
            else:
                # After fall - lying down
                return {
                    'ax': random.gauss(0, 0.1),
                    'ay': random.gauss(0, 0.1),
                    'az': 9.8 + random.gauss(0, 0.1),
                    'gx': random.gauss(0, 0.2),
                    'gy': random.gauss(0, 0.2),
                    'gz': random.gauss(0, 0.2)
                }
        
        else:  # Default to normal
            return self._generate_base_motion()
    
    def _get_fallback_motion_data(self) -> Dict[str, Any]:
        """Fallback motion data when accelerometer fails."""
        return {
            'ax': 0, 'ay': 0, 'az': 9.8,
            'gx': 0, 'gy': 0, 'gz': 0,
            'magnitude': 9.8,
            'gyro_magnitude': 0,
            'pitch': 0, 'roll': 0,
            'jerk_x': 0, 'jerk_y': 0, 'jerk_z': 0, 'jerk_magnitude': 0,
            'timestamp': datetime.now().isoformat(),
            'sensor_status': 'fallback'
        }
    
    def set_simulation_mode(self, mode: str):
        """Set simulation mode for testing."""
        self.mode = mode
        self.demo_timer = 0
        self.last_fall_time = 0
    
    def simulate_sensor_failure(self, sensor: str):
        """Simulate sensor failure for testing."""
        if sensor in self.sensor_failures:
            self.sensor_failures[sensor] = True
            print(f"⚠️ Simulated {sensor} sensor failure")
    
    def recover_sensor(self, sensor: str):
        """Recover from simulated sensor failure."""
        if sensor in self.sensor_failures:
            self.sensor_failures[sensor] = False
            print(f"✅ {sensor} sensor recovered")

class RealWearableSensor(SensorInterface):
    """Real wearable sensor implementation for ESP32 with multiple sensors."""
    
    def __init__(self, serial_port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.serial_connection = None
        self.connected = False
        
        # Sensor calibration data
        self.accel_offset = {'x': 0, 'y': 0, 'z': 0}
        self.gyro_offset = {'x': 0, 'y': 0, 'z': 0}
        
        # Device status
        self.battery_level = 100.0
        self.device_worn = False
        
    def connect(self) -> bool:
        """Connect to the wearable device."""
        try:
            import serial
            self.serial_connection = serial.Serial(
                self.serial_port, 
                self.baudrate, 
                timeout=1
            )
            self.connected = True
            print(f"✅ Connected to wearable device on {self.serial_port}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to device: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the wearable device."""
        if self.serial_connection:
            self.serial_connection.close()
            self.connected = False
            print("🔌 Disconnected from wearable device")
    
    def get_motion_data(self) -> Dict[str, Any]:
        """Read motion data from MPU6050 sensor."""
        if not self.connected or not self.serial_connection:
            return self._get_fallback_data()
        
        try:
            # Send command to read sensor data
            self.serial_connection.write(b"READ_MOTION\n")
            line = self.serial_connection.readline().decode('utf-8').strip()
            
            if line.startswith("MOTION:"):
                # Parse motion data: "MOTION: ax,ay,az,gx,gy,gz"
                parts = line[7:].split(',')
                if len(parts) == 6:
                    motion = {
                        'ax': float(parts[0]),
                        'ay': float(parts[1]),
                        'az': float(parts[2]),
                        'gx': float(parts[3]),
                        'gy': float(parts[4]),
                        'gz': float(parts[5]),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Apply calibration offsets
                    motion['ax'] -= self.accel_offset['x']
                    motion['ay'] -= self.accel_offset['y']
                    motion['az'] -= self.accel_offset['z']
                    motion['gx'] -= self.gyro_offset['x']
                    motion['gy'] -= self.gyro_offset['y']
                    motion['gz'] -= self.gyro_offset['z']
                    
                    # Calculate derived values
                    motion['magnitude'] = math.sqrt(motion['ax']**2 + motion['ay']**2 + motion['az']**2)
                    motion['gyro_magnitude'] = math.sqrt(motion['gx']**2 + motion['gy']**2 + motion['gz']**2)
                    
                    return motion
            
        except Exception as e:
            print(f"⚠️ Error reading motion data: {e}")
        
        return self._get_fallback_data()
    
    def get_vitals_data(self) -> Dict[str, Any]:
        """Read vitals data from MAX30102 and DS18B20 sensors."""
        vitals = {}
        
        try:
            # Read heart rate and SpO2 from MAX30102
            self.serial_connection.write(b"READ_VITALS\n")
            line = self.serial_connection.readline().decode('utf-8').strip()
            
            if line.startswith("VITALS:"):
                parts = line[8:].split(',')
                if len(parts) >= 2:
                    vitals['heart_rate'] = float(parts[0])
                    vitals['spo2'] = float(parts[1])
                    vitals['hr_status'] = 'normal' if 60 <= vitals['heart_rate'] <= 100 else 'abnormal'
                    vitals['spo2_status'] = 'normal' if vitals['spo2'] >= 95 else 'low'
            
            # Read temperature from DS18B20
            self.serial_connection.write(b"READ_TEMP\n")
            line = self.serial_connection.readline().decode('utf-8').strip()
            
            if line.startswith("TEMP:"):
                vitals['temperature'] = float(line[5:])
                vitals['temp_status'] = 'normal' if 36.0 <= vitals['temperature'] <= 37.5 else 'abnormal'
            
            # Body contact detection
            self.serial_connection.write(b"CHECK_CONTACT\n")
            line = self.serial_connection.readline().decode('utf-8').strip()
            vitals['body_contact'] = line == "CONTACT:1"
            vitals['contact_status'] = 'good' if vitals['body_contact'] else 'poor'
            
            vitals['timestamp'] = datetime.now().isoformat()
            
        except Exception as e:
            print(f"⚠️ Error reading vitals data: {e}")
            vitals = self._get_fallback_vitals()
        
        return vitals
    
    def get_battery_data(self) -> Dict[str, Any]:
        """Get battery data from device."""
        try:
            self.serial_connection.write(b"READ_BATTERY\n")
            line = self.serial_connection.readline().decode('utf-8').strip()
            
            if line.startswith("BATTERY:"):
                parts = line[9:].split(',')
                self.battery_level = float(parts[0])
                voltage = float(parts[1]) if len(parts) > 1 else 3.7
                
                return {
                    'level': self.battery_level,
                    'voltage': voltage,
                    'charging': False,
                    'status': 'good' if self.battery_level > 20 else 'low',
                    'estimated_hours': self.battery_level * 0.5
                }
        except Exception as e:
            print(f"⚠️ Error reading battery data: {e}")
        
        return {
            'level': self.battery_level,
            'voltage': 3.7,
            'charging': False,
            'status': 'unknown',
            'estimated_hours': self.battery_level * 0.5
        }
    
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.connected
    
    def calibrate(self) -> bool:
        """Calibrate all sensors."""
        if not self.connected:
            return False
        
        try:
            print("🔧 Calibrating wearable sensors...")
            
            # Calibrate accelerometer
            print("  Calibrating accelerometer...")
            self.serial_connection.write(b"CALIBRATE_ACCEL\n")
            response = self.serial_connection.readline().decode('utf-8').strip()
            if response.startswith("ACCEL_CAL:"):
                offsets = response[11:].split(',')
                self.accel_offset = {
                    'x': float(offsets[0]),
                    'y': float(offsets[1]),
                    'z': float(offsets[2])
                }
                print(f"  ✅ Accelerometer calibrated: {self.accel_offset}")
            
            # Calibrate gyroscope
            print("  Calibrating gyroscope...")
            self.serial_connection.write(b"CALIBRATE_GYRO\n")
            response = self.serial_connection.readline().decode('utf-8').strip()
            if response.startswith("GYRO_CAL:"):
                offsets = response[9:].split(',')
                self.gyro_offset = {
                    'x': float(offsets[0]),
                    'y': float(offsets[1]),
                    'z': float(offsets[2])
                }
                print(f"  ✅ Gyroscope calibrated: {self.gyro_offset}")
            
            print("✅ Calibration complete")
            return True
            
        except Exception as e:
            print(f"❌ Calibration failed: {e}")
            return False
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get comprehensive device status."""
        return {
            'device_id': 'waist_band_001',
            'connected': self.connected,
            'worn': self.device_worn,
            'battery': self.get_battery_data(),
            'serial_port': self.serial_port,
            'baudrate': self.baudrate,
            'last_calibration': datetime.now().isoformat()
        }
    
    def _get_fallback_data(self) -> Dict[str, Any]:
        """Fallback data when device is disconnected."""
        return {
            'ax': 0, 'ay': 0, 'az': 9.8,
            'gx': 0, 'gy': 0, 'gz': 0,
            'magnitude': 9.8,
            'gyro_magnitude': 0,
            'pitch': 0, 'roll': 0,
            'jerk_x': 0, 'jerk_y': 0, 'jerk_z': 0, 'jerk_magnitude': 0,
            'timestamp': datetime.now().isoformat(),
            'sensor_status': 'disconnected'
        }
    
    def _get_fallback_vitals(self) -> Dict[str, Any]:
        """Fallback vitals when device is disconnected."""
        return {
            'heart_rate': None,
            'spo2': None,
            'temperature': None,
            'body_contact': False,
            'hr_status': 'sensor_failed',
            'spo2_status': 'sensor_failed',
            'temp_status': 'sensor_failed',
            'contact_status': 'sensor_failed',
            'timestamp': datetime.now().isoformat()
        }

class HardwareManager:
    """Manages sensor instances and provides unified interface."""
    
    def __init__(self):
        self.sensor = None
        self.sensor_type = "none"
        self.use_real_hardware = False
    
    def initialize(self, use_real_hardware=False, serial_port="/dev/ttyUSB0", baudrate=115200):
        """Initialize the appropriate sensor."""
        self.use_real_hardware = use_real_hardware
        
        if use_real_hardware:
            self.sensor = RealWearableSensor(serial_port, baudrate)
            if self.sensor.connect():
                self.sensor_type = "real_wearable"
                print("📡 Using real wearable sensor")
            else:
                print("⚠️ Failed to connect to real sensor, using simulation")
                self.sensor = EnhancedSimulatedSensor("normal")
                self.sensor_type = "simulated"
        else:
            self.sensor = EnhancedSimulatedSensor("normal")
            self.sensor_type = "simulated"
            print("📡 Using simulated sensor data")
        
        return self.sensor
    
    def get_sensor_data(self) -> Dict[str, Any]:
        """Get comprehensive sensor data."""
        if not self.sensor:
            return {}
        
        return {
            'motion': self.sensor.get_motion_data(),
            'vitals': self.sensor.get_vitals_data(),
            'battery': self.sensor.get_battery_data(),
            'device_status': self.sensor.get_device_status()
        }
    
    def get_sensor_type(self) -> str:
        """Get the type of sensor being used."""
        return self.sensor_type
    
    def is_connected(self) -> bool:
        """Check if sensor is connected."""
        return self.sensor.is_connected() if self.sensor else False
    
    def calibrate(self) -> bool:
        """Calibrate the sensor."""
        return self.sensor.calibrate() if self.sensor else False

# Global hardware manager instance
_hardware_manager = None

def initialize_hardware(use_real_hardware=False, serial_port="/dev/ttyUSB0", baudrate=115200):
    """Initialize the hardware manager."""
    global _hardware_manager
    _hardware_manager = HardwareManager()
    return _hardware_manager.initialize(use_real_hardware, serial_port, baudrate)

def get_hardware_manager() -> Optional[HardwareManager]:
    """Get the global hardware manager instance."""
    return _hardware_manager

def get_sensor_data() -> Optional[Dict[str, Any]]:
    """Get sensor data from the global hardware manager."""
    if _hardware_manager:
        return _hardware_manager.get_sensor_data()
    return None

def set_simulation_mode(mode: str):
    """Set simulation mode for testing."""
    if _hardware_manager and hasattr(_hardware_manager.sensor, 'set_simulation_mode'):
        _hardware_manager.sensor.set_simulation_mode(mode)
        print(f"🎮 Simulation mode set to: {mode}")

def simulate_sensor_failure(sensor: str):
    """Simulate sensor failure for testing."""
    if _hardware_manager and hasattr(_hardware_manager.sensor, 'simulate_sensor_failure'):
        _hardware_manager.sensor.simulate_sensor_failure(sensor)

def recover_sensor(sensor: str):
    """Recover from simulated sensor failure."""
    if _hardware_manager and hasattr(_hardware_manager.sensor, 'recover_sensor'):
        _hardware_manager.sensor.recover_sensor(sensor)
