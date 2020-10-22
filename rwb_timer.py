from typing import List
from re import match
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
            "shift_time_in_seconds": 60 * 60 * 5,  # 60 seconds * 60 = 1 hour
            "break_time_in_seconds": 60 * 5,
            'shift_setting_buttons': [
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
            'break_setting_buttons': [
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
        self.shift_setting_button = None
        self.break_setting_button = None
        self.timer = rumps.Timer(self.on_tick, 1)
        self.shift_time_in_seconds = self.config["shift_time_in_seconds"]
        self.break_time_in_seconds = self.config["break_time_in_seconds"]
        self.start_pause_button = rumps.MenuItem(
            title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(
            title=self.config["stop"], callback=None)
        self.elapsedShiftCount = 0
        self.app.menu = [
            {
                'Preferences':
                {
                    "Setting Shift": self.__initialize_shift_setting_buttons(),
                    "Setting Break / hr": self.__initialize_break_setting_buttons(),
                }
            },
            None,
            self.start_pause_button,
            self.stop_button,
        ]

    def set_up_menu(self):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = self.config['app_title']

    def convert_seconds_to_time_string(self, seconds) -> str:
        seconds = seconds % (24 * 3600)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        return "%d:%02d:%02d" % (hours, minutes, seconds)

    def on_tick(self, sender):
        time_left_in_seconds = sender.end - sender.count

        time_left_in_string = self.convert_seconds_to_time_string(
            time_left_in_seconds)
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
                self.timer.end = self.shift_time_in_seconds
            sender.title = self.config["pause"]
            self.timer.start()
        else:
            sender.title = self.config["continue"]
            self.timer.stop()

    def stop_timer(self):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]

    def __initialize_shift_setting_buttons(self) -> List[rumps.MenuItem]:
        shift_setting_buttons = [rumps.MenuItem(shift_setting_button['title'], callback=self.toggle_shift_setting_button)
                                 for shift_setting_button in self.config['shift_setting_buttons']]

        # Setting default shift setting button with the first MenuItem in shift_setting_buttons list
        self.shift_setting_button = shift_setting_buttons[0]
        self.shift_setting_button.state = 1

        return shift_setting_buttons

    def __initialize_break_setting_buttons(self) -> List[rumps.MenuItem]:
        break_setting_buttons = [rumps.MenuItem(break_setting_button['title'], callback=self.toggle_break_setting_button)
                                 for break_setting_button in self.config['break_setting_buttons']]

        # Setting default shift setting button with the first MenuItem in break_setting_buttons list
        self.break_setting_button = break_setting_buttons[0]
        self.break_setting_button.state = 1

        return break_setting_buttons

    def toggle_shift_setting_button(self, sender):
        self.shift_setting_button.state = not self.shift_setting_button.state
        self.shift_setting_button = sender
        self.shift_setting_button.state = not self.shift_setting_button.state
        hours_in_seconds = int(match(r'^\d+\s{1}', sender.title)[0]) * 3600
        self.set_shift_time_in_seconds(hours_in_seconds)

    def toggle_break_setting_button(self, sender):
        self.break_setting_button.state = not self.break_setting_button.state
        self.break_setting_button = sender
        self.break_setting_button.state = not self.break_setting_button.state
        hours_in_seconds = int(match(r'^\d+\s{1}', sender.title)[0]) * 60
        self.set_break_time_in_seconds(hours_in_seconds)

    def set_shift_time_in_seconds(self, hours_in_seconds: int):
        self.shift_time_in_seconds = hours_in_seconds
        print(self.shift_setting_button.title, self.shift_time_in_seconds)

    def set_break_time_in_seconds(self, break_time_in_seconds: int):
        self.break_time_in_seconds = break_time_in_seconds
        print(self.break_setting_button.title, self.break_time_in_seconds)

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = RepeatWorkBreak()
    app.run()
