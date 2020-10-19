from typing import List
import rumps


class RepeatWorkBreak(rumps.App):
    def __init__(self):
        rumps.debug_mode(True)
        self.app = rumps.App("Repeat Work and Break")
        self.config = {
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
        self.shiftSettingButton = None
        self.breakSettingButton = None
        self.app.menu = [
            {
                'Preferences':
                {
                    "Setting Shift": self.__initializeShiftSettingButtons(),
                    "Setting Break / hr": self.__initializeBreakSettingButtons(),
                }
            },
            None,
            "Silly button",
            "Say hi",
        ]

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

    def prefs(self):
        self.window = rumps.Window(
            title="Please select your shift", dimensions=(320, 20))
        self.window.add_buttons(["8 hours", "4 hours",  "1 hour"])
        print(self.window.run())

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = RepeatWorkBreak()
    app.run()
