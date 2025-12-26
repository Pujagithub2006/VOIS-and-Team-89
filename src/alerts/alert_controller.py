class AlertController:
    def __init__(self, buzzer):
        self.buzzer = buzzer
        self.alert_sent = False
        self.timer = 0

    def handle(self, state, user_response=None):
        if state == "ALERT":
            self.buzzer.start()
            self.timer += 1

            if user_response == "ok":
                self.reset()

            if self.timer == 5 and not self.alert_sent:
                from alerts.guardian_alert import send_guardian_alert
                send_guardian_alert()
                self.alert_sent = True

            if self.timer == 10:
                from alerts.gsm_alert import send_gsm_alert
                send_gsm_alert()

        else:
            self.reset()

    def reset(self):
        self.buzzer.stop()
        self.alert_sent = False
        self.timer = 0
