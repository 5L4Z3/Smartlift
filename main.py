import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from datetime import datetime

kivy.require('2.1.0')

class WorkoutPlan:
    def __init__(self, name, days):
        self.name = name
        self.days = days

    def to_dict(self):
        return {'name': self.name, 'days': self.days}

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['days'])

class SmartLiftApp(App):
    def build(self):
        self.current_plan = None
        self.current_plan_key = "sample_plan_key"
        self.root = BoxLayout(orientation='vertical')
        self.title = "SmartLift 2.0"
        self.root.padding = [10, 10, 10, 10]
        return self.root

    def init_data(self):
        # Use writable directory on Android
        data_dir = App.get_running_app().user_data_dir
        self.store = JsonStore(f'{data_dir}/workout_plans.json')

        # Initialize default plan
        if not hasattr(self, 'current_plan') or self.current_plan is None:
            self.current_plan = WorkoutPlan(name="Sample Plan", days=[
                {"name": "Chest & Triceps", "rest": False, "exercises": []},
                {"name": "Back & Biceps", "rest": False, "exercises": []},
                {"name": "Rest Day", "rest": True, "exercises": []}
            ])

        # Load from storage
        if self.store.exists(self.current_plan_key):
            self.current_plan = WorkoutPlan.from_dict(self.store.get(self.current_plan_key))
        else:
            self.store.put(self.current_plan_key, **self.current_plan.to_dict())

        # Load sound safely
        try:
            self.bell_sound = SoundLoader.load('bell_sound.mp3')
            if not self.bell_sound:
                print("Warning: bell_sound.mp3 not found or unsupported format")
                self.bell_sound = None
        except Exception as e:
            print(f"Error loading sound: {e}")
            self.bell_sound = None

    def refresh_ui(self):
        self.root.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        label = Label(text="Your Workout Plans", size_hint_y=None, height=50, font_size='18sp')
        layout.add_widget(label)

        for index, day in enumerate(self.current_plan.days):
            name = day.get('name', f'Day {index+1}')
            btn = Button(
                text=f"Day {index + 1}: {name}",
                size_hint_y=None,
                height=50,
                background_color=(0.2, 0.6, 1, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda instance, idx=index: self.edit_day(idx))
            layout.add_widget(btn)

        self.root.add_widget(layout)

    def on_start(self):
        self.init_data()
        self.refresh_ui()

    def on_pause(self):
        self.save_workout_plan()
        return True

    def on_resume(self):
        pass

    def save_workout_plan(self):
        self.store.put(self.current_plan_key, **self.current_plan.to_dict())

    def edit_day(self, index):
        day = self.current_plan.days[index]
        content = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=400)
        content.padding = [10, 10, 10, 10]

        input_name = TextInput(text=day['name'], multiline=False, size_hint_y=None, height=40)
        input_rest = TextInput(text="yes" if day.get("rest") else "no", multiline=False, size_hint_y=None, height=40)

        def auto_save(*args):
            day['name'] = input_name.text
            day['rest'] = input_rest.text.strip().lower() == 'yes'
            self.save_workout_plan()

        input_name.bind(on_text_validate=auto_save)
        input_rest.bind(on_text_validate=auto_save)

        content.add_widget(Label(text="Edit Day Name:", size_hint_y=None, height=30))
        content.add_widget(input_name)
        content.add_widget(Label(text="Is Rest Day (yes/no):", size_hint_y=None, height=30))
        content.add_widget(input_rest)

        for i, exercise in enumerate(day.get("exercises", [])):
            ex_name = TextInput(text=exercise['name'], multiline=False, size_hint_y=None, height=40)
            ex_sets = TextInput(text=str(exercise.get('sets', 3)), hint_text="Sets", size_hint_y=None, height=40)
            ex_reps = TextInput(text=str(exercise.get('reps', 10)), hint_text="Reps", size_hint_y=None, height=40)
            ex_weight = TextInput(text=str(exercise.get('weight', 0)), hint_text="Weight (kg)", size_hint_y=None, height=40)
            ex_rest_time = TextInput(text=str(exercise.get('rest_time', 60)), hint_text="Rest time (seconds)", size_hint_y=None, height=40)

            last_sets = exercise['history'][-1]['sets'] if exercise['history'] else "N/A"
            last_reps = exercise['history'][-1]['reps'] if exercise['history'] else "N/A"
            last_weight = exercise['history'][-1]['weight'] if exercise['history'] else "N/A"

            last_used_label = Label(text=f"Last Used - Sets: {last_sets}, Reps: {last_reps}, Weight: {last_weight}", size_hint_y=None, height=40)
            content.add_widget(last_used_label)

            def save_exercise(*args):
                exercise['name'] = ex_name.text
                exercise['sets'] = int(ex_sets.text) if ex_sets.text.isdigit() else 3
                exercise['reps'] = int(ex_reps.text) if ex_reps.text.isdigit() else 10
                exercise['weight'] = float(ex_weight.text) if ex_weight.text.replace('.', '', 1).isdigit() else 0
                exercise['rest_time'] = int(ex_rest_time.text) if ex_rest_time.text.isdigit() else 60
                exercise.setdefault('history', []).append({
                    "sets": exercise['sets'],
                    "reps": exercise['reps'],
                    "weight": exercise['weight'],
                    "date": str(datetime.now())
                })
                self.save_workout_plan()

            ex_name.bind(on_text_validate=save_exercise)
            ex_sets.bind(on_text_validate=save_exercise)
            ex_reps.bind(on_text_validate=save_exercise)
            ex_weight.bind(on_text_validate=save_exercise)
            ex_rest_time.bind(on_text_validate=save_exercise)

            content.add_widget(Label(text="Exercise:", size_hint_y=None, height=30))
            content.add_widget(ex_name)
            content.add_widget(ex_sets)
            content.add_widget(ex_reps)
            content.add_widget(ex_weight)
            content.add_widget(ex_rest_time)

            def start_rest_countdown(instance):
                rest_time = exercise.get('rest_time', 60)
                self.start_countdown(rest_time)

            rest_button = Button(text="Start Rest", on_press=start_rest_countdown, size_hint_y=None, height=40)
            content.add_widget(rest_button)

        def add_exercise(instance):
            day['exercises'].append({"name": "New Exercise", "sets": 3, "reps": 10, "weight": 0, "rest_time": 60, "history": []})
            self.edit_day(index)
            self.save_workout_plan()

        content.add_widget(Button(text="+ Add Exercise", on_press=add_exercise, size_hint_y=None, height=40))

        popup = Popup(title="Edit Workout Day", content=ScrollView(size_hint=(1, None), size=(400, 500)), size_hint=(0.9, 0.9))
        popup.content.add_widget(content)
        popup.open()

    def start_countdown(self, rest_time):
        self.rest_time_remaining = rest_time
        self.countdown_label = Label(text=f"Rest Time: {self.rest_time_remaining}s", size_hint_y=None, height=40)
        self.root.add_widget(self.countdown_label)
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def update_countdown(self, dt):
        if self.rest_time_remaining > 0:
            self.rest_time_remaining -= 1
            self.countdown_label.text = f"Rest Time: {self.rest_time_remaining}s"
        else:
            Clock.unschedule(self.countdown_event)
            self.countdown_label.text = "Rest Over!"
            if self.bell_sound:
                self.bell_sound.play()

if __name__ == '__main__':
    SmartLiftApp().run()
