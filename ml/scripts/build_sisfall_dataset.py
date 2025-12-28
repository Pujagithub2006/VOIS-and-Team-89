import glob
import numpy as np
from load_sisfall import load_sisfall_file
from windowing import sliding_window
from features import extract_features_tiny

X, y = [], []

fall_files = glob.glob("ml/data/raw/sisfall/FALL/*.txt")
normal_files = glob.glob("ml/data/raw/sisfall/ADL/*.txt")

for f in fall_files:
    data = load_sisfall_file(f)
    windows = sliding_window(data)
    for w in windows:
        X.append(extract_features_tiny(w))
        y.append(1)

for f in normal_files:
    data = load_sisfall_file(f)
    windows = sliding_window(data)
    for w in windows:
        X.append(extract_features_tiny(w))
        y.append(0)

X = np.array(X)
y = np.array(y)

np.save("ml/data/processed/X.npy", X)
np.save("ml/data/processed/y.npy", y)

print("Dataset built:", X.shape, y.shape)
