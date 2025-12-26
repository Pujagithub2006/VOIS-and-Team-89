class ComfortRules:
    def __init__(self):
        self.alert_cooldown = 0

    def can_alert(self):
        if self.alert_cooldown == 0:
            self.alert_cooldown = 10
            return True
        return False

    def update(self):
        if self.alert_cooldown > 0:
            self.alert_cooldown -= 1
