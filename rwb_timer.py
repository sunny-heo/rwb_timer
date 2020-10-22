from typing import List
import rumps


class RepeatWorkBreak(rumps.App):
    def __init__(self):
        rumps.debug_mode(True)

        self.config = {
            "app_title": "Repeat Work and Break",
            "start": "Start",
            "pause": "Pause Timer",
            "continue": "Continue Timer",
            "stop": "Stop Timer",
            "timeout_message": "Time is up! Take a break :)",
            "interval": 60 * 60 * 5,  # 60 seconds * 60 = 1 hour
            'shiftSettingButtons': [
                {
                    'title': '1 hour',
                    'duration': 60,
                },
                {
                    'title': '4 hour',
                    'duration': 240,
                },
                {
                    'title': '8 hour',
                    'duration': 480,
                }
            ],
            'breakSettingButtons': [
                {
                    'title': '5 minutes',
                    'duration': 60,
                },
                {
                    'title': '10 minutes',
                    'duration': 240,
                },
                {
                    'title': '15 minutes',
                    'duration': 480,
                }
            ],
        }
        self.app = rumps.App(self.config['app_title'])
        self.totalShiftCount = 8
        self.progressBox = '◻︎' * self.totalShiftCount
        self.shiftSettingButton = None
        self.breakSettingButton = None
        self.timer = rumps.Timer(self.on_tick, 1)
        self.interval = self.config["interval"]
        self.start_pause_button = rumps.MenuItem(
            title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(
            title=self.config["stop"], callback=None)
        self.elapsedShiftCount = 0
        self.app.menu = [
            {
                'Preferences':
                {
                    "Setting Shift": self.__initializeShiftSettingButtons(),
                    "Setting Break / hr": self.__initializeBreakSettingButtons(),
                }
            },
            None,
            self.start_pause_button,
            self.stop_button,
        ]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = self.config['appTitle']

    def convert(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def on_tick(self, sender):
        time_left_in_seconds = sender.end - sender.count

        time_left_in_string = self.convert(time_left_in_seconds)
        if sender.count != 0 and sender.count % (360) == 0:
            self.elapsedShiftCount += 1
            self.updateProgressBox()

        if time_left_in_seconds == 0:
            rumps.notification(
                title=self.config["app_title"], subtitle=self.config["timeout_message"], message='')
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)

            self.app.title = self.progressBox + ' |  ' + time_left_in_string
            sender.count += 1

    def updateProgressBox(self):
        self.progressBox = self.elapsedShiftCount * '☑︎' + \
            (self.totalShiftCount - self.elapsedShiftCount) * '◻︎'

    def start_timer(self, sender):
        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == self.config["start"]:
                self.timer.count = 0
                self.timer.end = self.interval
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    def stop_timer(self):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]

    def __initializeShiftSettingButtons(self) -> List[rumps.MenuItem]:
        shiftSettingButtons = [rumps.MenuItem(shiftSettingButton['title'], callback=self.toggleShiftSettingButton)
                               for shiftSettingButton in self.config['shiftSettingButtons']]

        # Setting default shift setting button with the first MenuItem in shiftSettingButtons list
        self.shiftSettingButton = shiftSettingButtons[0]
        self.shiftSettingButton.state = 1

        return shiftSettingButtons

    def __initializeBreakSettingButtons(self) -> List[rumps.MenuItem]:
        breakSettingButtons = [rumps.MenuItem(breakSettingButton['title'], callback=self.toggleBreakSettingButton)
                               for breakSettingButton in self.config['breakSettingButtons']]

        # Setting default shift setting button with the first MenuItem in breakSettingButtons list
        self.breakSettingButton = breakSettingButtons[0]
        self.breakSettingButton.state = 1

        return breakSettingButtons

    def toggleShiftSettingButton(self, sender):
        self.shiftSettingButton.state = not self.shiftSettingButton.state
        self.shiftSettingButton = sender
        self.shiftSettingButton.state = not self.shiftSettingButton.state

    def toggleBreakSettingButton(self, sender):
        self.breakSettingButton.state = not self.breakSettingButton.state
        self.breakSettingButton = sender
        self.breakSettingButton.state = not self.breakSettingButton.state

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = RepeatWorkBreak()
    app.run()
