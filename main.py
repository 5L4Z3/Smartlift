from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform


class SmartLiftApp(App):
    def build(self):
        # Mobile-friendly UI settings
        if platform != 'android':
            Window.clearcolor = (0.05, 0.1, 0.2, 1)  # Dark background (desktop only)

        label = Label(
            text="Welcome to SmartLift 2.0!",
            font_size='24sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, None),
            color=(0.9, 0.9, 1, 1)
        )
        label.bind(size=label.setter('text_size'))
        return label

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    try:
        SmartLiftApp().run()
    except Exception as e:
        import logging
        logging.exception("App crashed")
        raise
