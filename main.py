from kivy.app import App
from kivy.uix.label import Label

class SmartLiftApp(App):
    def build(self):
        return Label(text="Welcome to SmartLift 2.0!")

if __name__ == '__main__':
    SmartLiftApp().run()
