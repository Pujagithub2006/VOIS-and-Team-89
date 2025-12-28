import numpy as np

def instability_score(window):
    accel = window[:, :3]
    jerk = np.diff(accel, axis=0)

    var_score = np.mean(np.var(accel, axis=0))
    jerk_score = np.mean(np.abs(jerk))
    
    score = 0.6 * var_score + 0.4 * jerk_score
    return min(score, 1.0)

def aggregate_instability(scores, threshold=0.7):
    recent = scores[-5:]
    return sum(s > threshold for s in recent)
