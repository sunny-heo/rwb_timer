from typing import List
from rumps import MenuItem


class ButtonGroup():

    def __init__(self, props: List[dict], callback=None):
        self.buttons = [MenuItem(title=prop['title'], callback=callback)
                        for prop in props]

        # Setting default active button that is selected by default
        self.active_button = self.buttons[0]
        self.active_button.state = 1

    def toggle(self, active_button):
        # Toggle current active button and toggle the given new active button
        self.active_button.state = not self.active_button.state
        self.active_button = active_button
        self.active_button.state = not self.active_button.state
