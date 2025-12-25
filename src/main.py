from sensors.mpu6050_simulator import get_motion_data
from detection.motion_analysis import calculate_magnitude
from detection.threshold_fall import detect_fall
import time

mode = "normal"

while True:
    ax, ay, az = get_motion_data(mode)
    magnitude = calculate_magnitude(ax, ay, az)
    fall = detect_fall(magnitude)

    print(f"MAG:{magnitude:.2f} | FALL:{fall}")

    time.sleep(1)
