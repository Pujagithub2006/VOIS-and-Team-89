import numpy as np

def load_sisfall_file(filepath):
    data = np.loadtxt(filepath, delimiter=',')
    return data[:, 1:7]  # ax, ay, az, gx, gy, gz
