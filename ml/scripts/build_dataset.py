import numpy as np
from windowing import sliding_window
from features import extract_features

def build_dataset(data, label):
    windows = sliding_window(data)
    X = np.array([extract_features(w) for w in windows])
    y = np.ones(len(X)) * label
    return X, y

if __name__ == "__main__":
    fall_data = np.random.randn(1000, 6)
    normal_data = np.random.randn(1000, 6)

    X_fall, y_fall = build_dataset(fall_data, 1)
    X_norm, y_norm = build_dataset(normal_data, 0)

    X = np.vstack((X_fall, X_norm))
    y = np.concatenate((y_fall, y_norm))

    print(X.shape, y.shape)
