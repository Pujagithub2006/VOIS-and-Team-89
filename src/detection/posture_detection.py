def detect_posture(az):
    if az < 3:
        return "lying"
    elif az < 7:
        return "sitting"
    else:
        return "standing"
