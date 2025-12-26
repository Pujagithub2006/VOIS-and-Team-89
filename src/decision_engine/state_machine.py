class FallStateMachine:
    def __init__(self):
        self.state = "NORMAL"
        self.fall_timer = 0

    def update(self, spike, posture, inactive):
        if self.state == "NORMAL":
            if spike:
                self.state = "POSSIBLE_FALL"
                self.fall_timer = 0

        elif self.state == "POSSIBLE_FALL":
            self.fall_timer += 1
            if posture == "lying" and inactive:
                self.state = "CONFIRMED_FALL"
            elif self.fall_timer > 3:
                self.state = "NORMAL"

        elif self.state == "CONFIRMED_FALL":
            self.state = "ALERT"

        return self.state
