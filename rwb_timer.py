import rumps


class RepeatWorkBreak(rumps.App):
    def __init__(self):
        rumps.debug_mode(True)
        self.app = rumps.App("Repeat Work and Break")

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = RepeatWorkBreak()
    app.run()
