from sensors.mpu6050_simulator import get_motion_data
from detection.motion_analysis import calculate_magnitude
from detection.threshold_fall import detect_fall
from detection.posture_detection import detect_posture
from detection.inactivity import is_inactive
import time

mode = "fall"  

prev_magnitude = 0

while True:
    ax, ay, az = get_motion_data(mode)
    magnitude = calculate_magnitude(ax, ay, az)

    fall_spike = detect_fall(magnitude)
    posture = detect_posture(az)
    inactive = is_inactive(magnitude, prev_magnitude)

    print(
        f"MAG:{magnitude:.2f} | "
        f"POSTURE:{posture} | "
        f"SPIKE:{fall_spike} | "
        f"INACTIVE:{inactive}"
    )

    prev_magnitude = magnitude
    time.sleep(1)
