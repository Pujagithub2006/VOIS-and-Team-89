from sensors.mpu6050_simulator import get_motion_data
from detection.motion_analysis import calculate_magnitude
from detection.threshold_fall import detect_fall
from detection.posture_detection import detect_posture
from detection.inactivity import is_inactive
from decision_engine.state_machine import FallStateMachine
from alerts.buzzer import Buzzer
from alerts.alert_controller import AlertController
from decision_engine.range_monitor import RangeMonitor
import time

mode = "fall" 

fsm = FallStateMachine()
buzzer = Buzzer()
alerts = AlertController(buzzer)
range_monitor = RangeMonitor()

prev_magnitude = 0

while True:
    phone_connected = True 
    ax, ay, az = get_motion_data(mode)
    magnitude = calculate_magnitude(ax, ay, az)

    spike = detect_fall(magnitude)
    posture = detect_posture(az)
    inactive = is_inactive(magnitude, prev_magnitude)
    range_state = range_monitor.update(phone_connected)

    state = fsm.update(spike, posture, inactive)

    alerts.handle(state)

    print(
        f"MAG:{magnitude:.2f} | "
        f"POSTURE:{posture} | "
        f"STATE:{state}"
    )

    prev_magnitude = magnitude
    time.sleep(1)  

    if range_state == "OUT_OF_RANGE":
        print("USER OUT OF RANGE")
