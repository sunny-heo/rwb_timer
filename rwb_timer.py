from typing import List
from re import match
from utility import ButtonGroup
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
            "shift_time_in_seconds": 60 * 60 * 1,  # 60 seconds * 60 = 1 hour
            "break_time_in_seconds": 60 * 5,
            'shift_setting_buttons': [
                {
                    'title': '1 hour',
                },
                {
                    'title': '4 hour',
                },
                {
                    'title': '8 hour',
                }
            ],
            'break_setting_buttons': [
                {
                    'title': '5 minutes',
                },
                {
                    'title': '10 minutes',
                },
                {
                    'title': '15 minutes',
                }
            ],
        }
        self.app = rumps.App(self.config['app_title'])
        self.timer = rumps.Timer(self.on_tick, 1)
        self.shift_setting_button_group = ButtonGroup(
            self.config['shift_setting_buttons'], callback=self.handle_shift_setting_button)
        self.break_setting_button_group = ButtonGroup(
            self.config['break_setting_buttons'], callback=self.handle_shift_setting_button)
        self.shift_time_in_seconds = self.config["shift_time_in_seconds"]
        self.break_time_in_seconds = self.config["break_time_in_seconds"]
        self.elapsed_shift_time_in_hours = 0
        self.progress_box = '◻︎' * (self.shift_time_in_seconds // 3600)
        self.start_pause_button = rumps.MenuItem(
            title=self.config["start"], callback=self.start_timer)
        self.stop_button = rumps.MenuItem(
            title=self.config["stop"], callback=None)
        self.app.menu = [
            {
                'Preferences':
                {
                    "Setting Shift": self.shift_setting_button_group.buttons,
                    "Setting Break / hr": self.break_setting_button_group.buttons,
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
        if sender.count != 0 and sender.count % 3600 == 0:
            self.elapsed_shift_time_in_hours += 1
            self.update_progress_box()
        if time_left_in_seconds == 0:
            rumps.notification(
                title=self.config["app_title"], subtitle=self.config["timeout_message"], message='')
            self.stop_timer()
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)

            self.app.title = self.progress_box + ' |  ' + time_left_in_string
            sender.count += 1

    def update_progress_box(self):
        self.progress_box = self.elapsed_shift_time_in_hours * '☑︎' + (self.shift_time_in_seconds // 3600 -
                                                                       self.elapsed_shift_time_in_hours) * '◻︎'

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

    def stop_timer(self, sender=None):
        self.set_up_menu()
        self.stop_button.set_callback(None)
        self.start_pause_button.title = self.config["start"]

    def handle_shift_setting_button(self, sender):
        self.shift_setting_button_group.toggle(sender)
        selected_hours = int(match(r'^\d+\s{1}', sender.title)[0])
        self.progress_box = "◻︎" * selected_hours  # update empty progress box
        self.shift_time_in_seconds = selected_hours * 3600  # hours in seconds

    def handle_break_setting_button(self, sender):
        self.break_setting_button_group.toggle(sender)
        selected_minutes = int(match(r'^\d+\s{1}', sender.title)[0])
        self.break_time_in_seconds = selected_minutes * 60

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = RepeatWorkBreak()
    app.run()
