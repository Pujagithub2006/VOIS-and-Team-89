def detect_fall(magnitude, threshold=15):
    if magnitude > threshold:
        return True
    return False
