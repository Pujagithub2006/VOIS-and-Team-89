import random
import time

def normal_motion():
    ax = random.uniform(-0.5, 0.5)
    ay = random.uniform(-0.5, 0.5)
    az = random.uniform(9, 10)
    return ax, ay, az

def fall_motion():
    ax = random.uniform(-4, 4)
    ay = random.uniform(-4, 4)
    az = random.uniform(15, 25) 
    return ax, ay, az

def get_motion_data(mode="normal"):
    if mode == "fall":
        return fall_motion()
    return normal_motion()

if __name__ == "__main__":
    while True:
        print(get_motion_data("normal"))
        time.sleep(1)
