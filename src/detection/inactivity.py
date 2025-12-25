def is_inactive(magnitude, prev_magnitude, tolerance=0.3):
    if abs(magnitude - prev_magnitude) < tolerance:
        return True
    return False
