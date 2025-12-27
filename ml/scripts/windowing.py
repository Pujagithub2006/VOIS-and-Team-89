import numpy as np

def sliding_window(data, window_size=100, step_size=50):
    windows = []
    for start in range(0, len(data) - window_size, step_size):
        window = data[start:start + window_size]
        windows.append(window)
    return np.array(windows)
