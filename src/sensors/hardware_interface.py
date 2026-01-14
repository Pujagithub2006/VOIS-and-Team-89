"""
Hardware Abstraction Layer for Fall Detection System

Provides unified interface for both simulated and real sensor data.
Enables seamless transition from simulation to hardware deployment.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
import time
import random

class SensorInterface(ABC):
    """Abstract base class for sensor data sources."""
    
    @abstractmethod
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Get acceleration data (ax, ay, az) in m/s²."""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if sensor is connected and operational."""
        pass
    
    @abstractmethod
    def calibrate(self) -> bool:
        """Calibrate sensor. Returns True if successful."""
        pass

class SimulatedSensor(SensorInterface):
    """Simulated MPU6050 sensor for testing and demo."""
    
    def __init__(self, mode: str = "normal"):
        """
        Initialize simulated sensor.
        
        Args:
            mode: "normal", "sitting", "lying", "fall", or "demo"
        """
        self.mode = mode
        self.demo_timer = 0
        self.demo_sequence = ["normal", "normal", "normal", "fall", "lying", "lying"]
        self.connected = True
        
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Get simulated acceleration data."""
        # Demo mode: automatic sequence for demonstration
        if self.mode == "demo":
            self.demo_timer += 1
            if self.demo_timer % 20 == 0:  # Change every 20 cycles
                idx = (self.demo_timer // 20) % len(self.demo_sequence)
                current_mode = self.demo_sequence[idx]
            else:
                current_mode = self.demo_sequence[(self.demo_timer // 20) % len(self.demo_sequence)]
        else:
            current_mode = self.mode
            
        if current_mode == "fall":
            # High acceleration during impact
            ax = random.uniform(-15, 15)
            ay = random.uniform(-15, 15)
            az = random.uniform(15, 25)
        elif current_mode == "sitting":
            # Moderate tilt
            ax = random.uniform(2, 4)
            ay = random.uniform(-0.5, 0.5)
            az = random.uniform(8, 10)
        elif current_mode == "lying":
            # Device horizontal
            ax = 9.8 + random.uniform(-0.3, 0.3)
            ay = random.uniform(-0.2, 0.2)
            az = random.uniform(-0.2, 0.2)
        else:  # normal
            # Standing upright
            ax = random.uniform(-0.5, 0.5)
            ay = random.uniform(-0.5, 0.5)
            az = random.uniform(9.3, 10.3)
            
        return ax, ay, az
    
    def is_connected(self) -> bool:
        """Simulated sensor is always connected."""
        return self.connected
    
    def calibrate(self) -> bool:
        """Simulated calibration always succeeds."""
        time.sleep(0.1)  # Simulate calibration delay
        return True
    
    def set_mode(self, mode: str):
        """Change simulation mode."""
        self.mode = mode

class RealMPU6050(SensorInterface):
    """Real MPU6050 sensor interface for hardware deployment."""
    
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        """
        Initialize real sensor connection.
        
        Args:
            port: Serial port for ESP32 communication
            baudrate: Communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.connected = False
        
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Get real acceleration data from MPU6050."""
        if not self.is_connected():
            # Fallback to safe values if disconnected
            return 0.0, 0.0, 9.8
            
        try:
            # Request data from ESP32
            if self.serial_connection:
                self.serial_connection.write(b"GET_DATA\n")
                line = self.serial_connection.readline().decode().strip()
                
                if line.startswith("ACC:"):
                    # Parse acceleration data: "ACC:ax,ay,az"
                    parts = line[4:].split(",")
                    if len(parts) == 3:
                        ax, ay, az = map(float, parts)
                        return ax, ay, az
                        
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            self.connected = False
            
        # Fallback values
        return 0.0, 0.0, 9.8
    
    def is_connected(self) -> bool:
        """Check if real sensor is connected."""
        if self.connected and self.serial_connection:
            try:
                # Test connection with ping
                self.serial_connection.write(b"PING\n")
                response = self.serial_connection.readline().decode().strip()
                self.connected = response == "PONG"
            except:
                self.connected = False
        return self.connected
    
    def calibrate(self) -> bool:
        """Calibrate real MPU6050 sensor."""
        if not self.is_connected():
            return False
            
        try:
            self.serial_connection.write(b"CALIBRATE\n")
            response = self.serial_connection.readline().decode().strip()
            return response == "CALIBRATED"
        except:
            return False
    
    def connect(self) -> bool:
        """Establish connection to real sensor."""
        try:
            import serial
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for connection to stabilize
            
            # Test connection
            if self.is_connected():
                print(f"Connected to MPU6050 on {self.port}")
                return True
            else:
                print("Failed to establish connection")
                return False
                
        except Exception as e:
            print(f"Failed to connect to sensor: {e}")
            self.connected = False
            return False

class HardwareManager:
    """
    Hardware manager that handles sensor selection and fallback.
    Provides unified interface for the main application.
    """
    
    def __init__(self, use_real_hardware: bool = False, port: str = "/dev/ttyUSB0"):
        """
        Initialize hardware manager.
        
        Args:
            use_real_hardware: Whether to use real sensor or simulation
            port: Serial port for real sensor connection
        """
        self.use_real_hardware = use_real_hardware
        self.sensor = None
        self.fallback_sensor = SimulatedSensor("normal")
        
        if use_real_hardware:
            self.sensor = RealMPU6050(port)
            if not self.sensor.connect():
                print("Failed to connect to real sensor, using simulation")
                self.sensor = self.fallback_sensor
                self.use_real_hardware = False
        else:
            self.sensor = self.fallback_sensor
            print("Using simulated sensor data")
    
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Get acceleration data with automatic fallback."""
        try:
            if self.sensor and self.sensor.is_connected():
                return self.sensor.get_acceleration()
            else:
                # Fallback to simulation if real sensor fails
                if self.use_real_hardware:
                    print("Real sensor disconnected, using simulation fallback")
                    self.use_real_hardware = False
                    self.sensor = self.fallback_sensor
                return self.sensor.get_acceleration()
        except Exception as e:
            print(f"Error getting acceleration data: {e}")
            return 0.0, 0.0, 9.8  # Safe fallback
    
    def set_simulation_mode(self, mode: str):
        """Set simulation mode when using simulated sensor."""
        if isinstance(self.sensor, SimulatedSensor):
            self.sensor.set_mode(mode)
    
    def is_connected(self) -> bool:
        """Check if current sensor is connected."""
        return self.sensor and self.sensor.is_connected()
    
    def get_sensor_type(self) -> str:
        """Get current sensor type."""
        if isinstance(self.sensor, RealMPU6050):
            return "Real MPU6050"
        elif isinstance(self.sensor, SimulatedSensor):
            return "Simulated MPU6050"
        else:
            return "Unknown"

# Global hardware manager instance
_hardware_manager = None

def initialize_hardware(use_real_hardware: bool = False, port: str = "/dev/ttyUSB0") -> HardwareManager:
    """
    Initialize the hardware manager.
    
    Args:
        use_real_hardware: Whether to use real sensor
        port: Serial port for real sensor
        
    Returns:
        HardwareManager instance
    """
    global _hardware_manager
    _hardware_manager = HardwareManager(use_real_hardware, port)
    return _hardware_manager

def get_hardware_manager() -> Optional[HardwareManager]:
    """Get the global hardware manager instance."""
    return _hardware_manager

def get_motion_data(mode: str = "normal") -> Tuple[float, float, float]:
    """
    Legacy compatibility function.
    
    Args:
        mode: Simulation mode (ignored if using real hardware)
        
    Returns:
        Acceleration data (ax, ay, az)
    """
    manager = get_hardware_manager()
    if manager:
        if not manager.use_real_hardware:
            manager.set_simulation_mode(mode)
        return manager.get_acceleration()
    else:
        # Fallback to direct simulation
        sensor = SimulatedSensor(mode)
        return sensor.get_acceleration()
