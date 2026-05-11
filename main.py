import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.switch import Switch
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from datetime import datetime
from plyer import vibration
import re
import json
import os

# Match your build environment
kivy.require('2.2.1')

# =============================================================================
# UTILS & VALIDATION
# =============================================================================

def safe_numeric_input(text, allow_negative=False, allow_decimal=True, default=0):
    """Robust numeric parser for weights, reps, etc."""
    if not text or not text.strip():
        return default
    try:
        cleaned = text.strip().replace(',', '.')
        if allow_decimal:
            value = float(cleaned)
        else:
            value = int(float(cleaned))  # Handle "10.9" → 10 for reps
        if not allow_negative and value < 0:
            return default
        return value
    except (ValueError, TypeError):
        return default

def format_weight(value, unit='kg'):
    """Display weight with unit suffix"""
    return f"{value:.1f} {unit}" if value else f"0 {unit}"

# =============================================================================
# DATA MODELS
# =============================================================================

class ExerciseLibrary:
    """Simple in-memory + JSON exercise library"""
    def __init__(self, store_path):
        self.store_path = store_path
        self.exercises = self._load()
    
    def _load(self):
        if os.path.exists(self.store_path):
            with open(self.store_path, 'r') as f:
                return json.load(f)
        # Default starter library
        return {
            "bench_press": {"name": "Bench Press", "muscle": "Chest", "equipment": "Barbell"},
            "squat": {"name": "Squat", "muscle": "Legs", "equipment": "Barbell"},
            "deadlift": {"name": "Deadlift", "muscle": "Back", "equipment": "Barbell"},
            "pull_up": {"name": "Pull Up", "muscle": "Back", "equipment": "Bodyweight"},
            "shoulder_press": {"name": "Shoulder Press", "muscle": "Shoulders", "equipment": "Dumbbell"},
        }
    
    def save(self):
        with open(self.store_path, 'w') as f:
            json.dump(self.exercises, f, indent=2)
    
    def add(self, key, name, muscle="", equipment=""):
        self.exercises[key] = {"name": name, "muscle": muscle, "equipment": equipment}
        self.save()
    
    def search(self, query):
        """Case-insensitive partial match on name or key"""
        query = query.lower()
        results = []
        for key, ex in self.exercises.items():
            if query in key.lower() or query in ex['name'].lower():
                results.append((key, ex))
        return results

class WorkoutPlan:
    def __init__(self, name, days, unit='kg'):
        self.name = name
        self.days = days  # List of day dicts
        self.unit = unit  # 'kg' or 'lb'
    
    def to_dict(self):
        return {'name': self.name, 'days': self.days, 'unit': self.unit}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['days'], data.get('unit', 'kg'))

# =============================================================================
# CUSTOM WIDGETS
# =============================================================================

class LongPressButton(ButtonBehavior, Label):
    """Label that triggers on long press (for delete gestures)"""
    long_press_time = 0.5  # seconds
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trigger = Clock.create_trigger(self._on_long_press, self.long_press_time)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self._trigger()
            return True
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self._trigger.cancel()
            touch.ungrab(self)
        return super().on_touch_up(touch)
    
    def _on_long_press(self, dt):
        # Override in parent
        pass

# =============================================================================
# MAIN APP
# =============================================================================

class SmartLiftApp(App):
    title = "SmartLift Pro"
    
    def build(self):
        self.current_plan = None
        self.current_plan_key = "active_plan"
        self.workout_mode = False  # Planning vs Logging mode
        self.unit = 'kg'  # Default unit
        self.exercise_lib = None
        self.root = BoxLayout(orientation='vertical')
        self.root.padding = [dp(10), dp(10), dp(10), dp(10)]
        return self.root
    
    def on_start(self):
        self.init_data()
        self.refresh_ui()
    
    def init_data(self):
        data_dir = self.user_data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize stores
        self.store = JsonStore(f'{data_dir}/workout_plans.json')
        lib_path = f'{data_dir}/exercise_library.json'
        self.exercise_lib = ExerciseLibrary(lib_path)
        
        # Load or create default plan
        if not self.store.exists(self.current_plan_key):
            default_plan = WorkoutPlan(
                name="Starter Plan",
                days=[
                    {"name": "Push Day", "rest": False, "exercises": []},
                    {"name": "Pull Day", "rest": False, "exercises": []},
                    {"name": "Rest", "rest": True, "exercises": []}
                ],
                unit='kg'
            )
            self.store.put(self.current_plan_key, **default_plan.to_dict())
        
        plan_data = self.store.get(self.current_plan_key)
        self.current_plan = WorkoutPlan.from_dict(plan_data)
        self.unit = self.current_plan.unit
        
        # Load sound with fallback
        try:
            self.bell_sound = SoundLoader.load('bell_sound.mp3')
        except:
            self.bell_sound = None
    
    def save_plan(self):
        self.current_plan.unit = self.unit
        self.store.put(self.current_plan_key, **self.current_plan.to_dict())
    
    def refresh_ui(self):
        self.root.clear_widgets()
        
        # Header with mode toggle + settings
        header = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
        
        # Mode toggle
        mode_label = Label(text="📝 Planning" if not self.workout_mode else "🏋️ Workout Mode", 
                          size_hint_x=None, width=dp(150))
        mode_switch = Switch(active=self.workout_mode, size_hint_x=None, width=dp(100))
        mode_switch.bind(active=self.toggle_workout_mode)
        
        # Unit toggle
        unit_label = Label(text=f"Unit: {self.unit.upper()}", size_hint_x=None, width=dp(100))
        unit_switch = Switch(active=(self.unit == 'lb'), size_hint_x=None, width=dp(80))
        unit_switch.bind(active=self.toggle_unit)
        
        # Settings button
        settings_btn = Button(text="⚙️", size_hint_x=None, width=dp(50))
        settings_btn.bind(on_press=self.open_settings)
        
        header.add_widget(mode_label)
        header.add_widget(mode_switch)
        header.add_widget(unit_label)
        header.add_widget(unit_switch)
        header.add_widget(settings_btn)
        self.root.add_widget(header)
        
        # Main content
        if self.workout_mode:
            self.build_workout_screen()
        else:
            self.build_planning_screen()
    
    def toggle_workout_mode(self, instance, value):
        self.workout_mode = value
        self.refresh_ui()
    
    def toggle_unit(self, instance, value):
        self.unit = 'lb' if value else 'kg'
        self.save_plan()
        self.refresh_ui()  # Refresh to update displayed weights
    
    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        content.add_widget(Label(text="⚙️ Settings", font_size='20sp', size_hint_y=None, height=dp(40)))
        
        # Exercise library manager
        lib_btn = Button(text="📚 Manage Exercise Library", size_hint_y=None, height=dp(50))
        lib_btn.bind(on_press=self.open_exercise_library)
        content.add_widget(lib_btn)
        
        # Export data
        export_btn = Button(text="💾 Export Plan", size_hint_y=None, height=dp(50))
        export_btn.bind(on_press=self.export_plan)
        content.add_widget(export_btn)
        
        # Progress charts
        chart_btn = Button(text="📈 View Progress", size_hint_y=None, height=dp(50))
        chart_btn.bind(on_press=self.show_progress_charts)
        content.add_widget(chart_btn)
        
        popup = Popup(title="Settings", content=ScrollView(size_hint=(1, None), size=(400, 300)), 
                     size_hint=(0.9, 0.8))
        popup.content.add_widget(content)
        popup.open()
    
    # =============================================================================
    # PLANNING MODE UI
    # =============================================================================
    
    def build_planning_screen(self):
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(5), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for idx, day in enumerate(self.current_plan.days):
            day_card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), 
                                canvas.before=[
                                    kivy.graphics.Color(rgba=(0.95, 0.95, 0.95, 1)),
                                    kivy.graphics.Rectangle(pos=self.root.pos, size=self.root.size)
                                ])
            
            # Day header with delete gesture
            header = BoxLayout(size_hint_y=None, height=dp(40))
            day_title = LongPressButton(
                text=f"🗓️ {day.get('name', f'Day {idx+1}')}",
                font_size='18sp',
                color=(0, 0, 0, 1)
            )
            # Override long press to delete day
            def make_delete_day(i):
                def _delete(*args):
                    self.delete_day(i)
                return _delete
            day_title._on_long_press = make_delete_day(idx)
            
            edit_btn = Button(text="✏️ Edit", size_hint_x=None, width=dp(80))
            edit_btn.bind(on_press=lambda _, i=idx: self.edit_day(i))
            
            header.add_widget(day_title)
            header.add_widget(edit_btn)
            day_card.add_widget(header)
            
            # Exercise preview
            ex_count = len(day.get('exercises', []))
            ex_label = Label(text=f"{ex_count} exercises • Tap to plan", 
                           size_hint_y=None, height=dp(30), color=(0.3, 0.3, 0.3, 1))
            day_card.add_widget(ex_label)
            
            layout.add_widget(day_card)
        
        # Add day button
        add_day_btn = Button(text="+ Add Training Day", size_hint_y=None, height=dp(50),
                           background_color=(0.2, 0.8, 0.2, 1))
        add_day_btn.bind(on_press=self.add_new_day)
        layout.add_widget(add_day_btn)
        
        scroll.add_widget(layout)
        self.root.add_widget(scroll)
    
    def delete_day(self, index):
        # Confirmation popup
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        content.add_widget(Label(text=f"Delete '{self.current_plan.days[index].get('name')}'?", 
                               size_hint_y=None, height=dp(40)))
        
        btn_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        cancel_btn = Button(text="Cancel")
        delete_btn = Button(text="Delete", background_color=(1, 0.3, 0.3, 1))
        
        def confirm_delete(*args):
            self.current_plan.days.pop(index)
            self.save_plan()
            self.refresh_ui()
            popup.dismiss()
        
        cancel_btn.bind(on_press=lambda *a: popup.dismiss())
        delete_btn.bind(on_press=confirm_delete)
        
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(delete_btn)
        content.add_widget(btn_row)
        
        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.8, 0.4))
        popup.open()
    
    def add_new_day(self, instance):
        self.current_plan.days.append({
            "name": f"New Day {len(self.current_plan.days) + 1}",
            "rest": False,
            "exercises": []
        })
        self.save_plan()
        self.refresh_ui()
    
    def edit_day(self, index):
        day = self.current_plan.days[index]
        content = ScrollView(size_hint=(1, None), size=(400, 500))
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Day name editor
        layout.add_widget(Label(text="Day Name:", size_hint_y=None, height=dp(30)))
        name_input = TextInput(text=day['name'], multiline=False, size_hint_y=None, height=dp(40))
        name_input.bind(text=lambda inst, val: self._update_day_name(index, val))
        layout.add_widget(name_input)
        
        # Rest day toggle
        rest_row = BoxLayout(size_hint_y=None, height=dp(40))
        rest_row.add_widget(Label(text="Rest Day:", size_hint_x=None, width=dp(100)))
        rest_switch = Switch(active=day.get('rest', False))
        rest_switch.bind(active=lambda inst, val: self._update_day_rest(index, val))
        rest_row.add_widget(rest_switch)
        layout.add_widget(rest_row)
        
        # Exercises list
        layout.add_widget(Label(text="\nExercises:", size_hint_y=None, height=dp(40), font_size='16sp'))
        
        for ex_idx, exercise in enumerate(day.get('exercises', [])):
            ex_card = self._build_exercise_editor(index, ex_idx, exercise)
            layout.add_widget(ex_card)
        
        # Add exercise button with library dropdown
        add_ex_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        # Dropdown for exercise library
        dropdown = DropDown()
        for key, ex_data in list(self.exercise_lib.exercises.items())[:10]:  # Show top 10
            btn = Button(text=ex_data['name'], size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda btn, k=key: self._add_exercise_from_lib(index, k))
            dropdown.add_widget(btn)
        
        lib_btn = Button(text="📚 From Library", size_hint_x=None, width=dp(150))
        lib_btn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(lib_btn, 'text', x))
        
        add_custom_btn = Button(text="+ Custom Exercise")
        add_custom_btn.bind(on_press=lambda _: self._add_custom_exercise(index))
        
        add_ex_row.add_widget(lib_btn)
        add_ex_row.add_widget(add_custom_btn)
        layout.add_widget(add_ex_row)
        
        content.add_widget(layout)
        popup = Popup(title=f"Edit: {day['name']}", content=content, size_hint=(0.95, 0.9))
        popup.open()
    
    def _update_day_name(self, day_idx, new_name):
        self.current_plan.days[day_idx]['name'] = new_name
        self.save_plan()
    
    def _update_day_rest(self, day_idx, is_rest):
        self.current_plan.days[day_idx]['rest'] = is_rest
        self.save_plan()
    
    def _build_exercise_editor(self, day_idx, ex_idx, exercise):
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(220), 
                        canvas.before=[
                            kivy.graphics.Color(rgba=(0.98, 0.98, 0.98, 1)),
                            kivy.graphics.Rectangle(pos=self.root.pos, size=self.root.size)
                        ])
        
        # Header with delete gesture
        header = BoxLayout(size_hint_y=None, height=dp(40))
        ex_name_label = LongPressButton(
            text=f"💪 {exercise.get('name', 'New Exercise')}",
            color=(0, 0, 0, 1),
            font_size='16sp'
        )
        # Long press to delete exercise
        def make_delete_ex(d_idx, e_idx):
            def _delete(*args):
                self.delete_exercise(d_idx, e_idx)
            return _delete
        ex_name_label._on_long_press = make_delete_ex(day_idx, ex_idx)
        
        delete_hint = Label(text="(hold to delete)", size_hint_x=None, width=dp(120), 
                          color=(0.6, 0.6, 0.6, 1), font_size='12sp')
        header.add_widget(ex_name_label)
        header.add_widget(delete_hint)
        card.add_widget(header)
        
        # Last used stats
        history = exercise.get('history', [])
        if history:
            last = history[-1]
            last_text = f"Last: {last['sets']}x{last['reps']} @ {format_weight(last['weight'], self.unit)}"
        else:
            last_text = "No history yet"
        card.add_widget(Label(text=last_text, size_hint_y=None, height=dp(25), color=(0.4, 0.4, 0.4, 1)))
        
        # Input fields
        inputs = BoxLayout(size_hint_y=None, height=dp(120), spacing=dp(5))
        
        # Name (read-only in planner, editable in workout mode)
        name_input = TextInput(text=exercise['name'], multiline=False, readonly=True,
                             size_hint_x=0.4, height=dp(40))
        
        # Numeric inputs with validation
        def make_numeric_binder(key, default, allow_decimal=True):
            def _save(inst):
                val = safe_numeric_input(inst.text, allow_negative=False, 
                                       allow_decimal=allow_decimal, default=default)
                exercise[key] = val
                self.save_plan()
            return _save
        
        sets_input = TextInput(text=str(exercise.get('sets', 3)), hint_text="Sets", 
                             input_filter='int', size_hint_x=0.15, height=dp(40))
        sets_input.bind(on_text_validate=make_numeric_binder('sets', 3, allow_decimal=False))
        
        reps_input = TextInput(text=str(exercise.get('reps', 10)), hint_text="Reps", 
                             input_filter='int', size_hint_x=0.15, height=dp(40))
        reps_input.bind(on_text_validate=make_numeric_binder('reps', 10, allow_decimal=False))
        
        weight_input = TextInput(text=str(exercise.get('weight', 0)), 
                               hint_text=f"Weight ({self.unit})", 
                               input_filter='float' if self.unit == 'kg' else 'float', 
                               size_hint_x=0.2, height=dp(40))
        weight_input.bind(on_text_validate=make_numeric_binder('weight', 0, allow_decimal=True))
        
        rest_input = TextInput(text=str(exercise.get('rest_time', 60)), hint_text="Rest (s)", 
                             input_filter='int', size_hint_x=0.1, height=dp(40))
        rest_input.bind(on_text_validate=make_numeric_binder('rest_time', 60, allow_decimal=False))
        
        inputs.add_widget(name_input)
        inputs.add_widget(sets_input)
        inputs.add_widget(reps_input)
        inputs.add_widget(weight_input)
        inputs.add_widget(rest_input)
        card.add_widget(inputs)
        
        # Action buttons
        actions = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        rest_btn = Button(text="⏱️ Rest", size_hint_x=0.5)
        rest_btn.bind(on_press=lambda _: self.start_rest_timer(exercise.get('rest_time', 60)))
        actions.add_widget(rest_btn)
        
        # Only show log button in workout mode
        if self.workout_mode:
            log_btn = Button(text="✓ Log Set", background_color=(0.2, 0.8, 0.2, 1), size_hint_x=0.5)
            log_btn.bind(on_press=lambda _: self.log_actual_set(day_idx, ex_idx))
            actions.add_widget(log_btn)
        
        card.add_widget(actions)
        return card
    
    def _add_exercise_from_lib(self, day_idx, exercise_key):
        ex_data = self.exercise_lib.exercises.get(exercise_key)
        if not ex_data:
            return
        new_ex = {
            "name": ex_data['name'],
            "sets": 3,
            "reps": 10,
            "weight": 0,
            "rest_time": 60,
            "history": [],
            "library_key": exercise_key  # Reference for later updates
        }
        self.current_plan.days[day_idx].setdefault('exercises', []).append(new_ex)
        self.save_plan()
        self.refresh_ui()  # Refresh to show updated list
    
    def _add_custom_exercise(self, day_idx):
        new_ex = {
            "name": "New Exercise",
            "sets": 3,
            "reps": 10,
            "weight": 0,
            "rest_time": 60,
            "history": []
        }
        self.current_plan.days[day_idx].setdefault('exercises', []).append(new_ex)
        self.save_plan()
        # Reopen editor to edit the new exercise
        self.edit_day(day_idx)
    
    def delete_exercise(self, day_idx, ex_idx):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        ex_name = self.current_plan.days[day_idx]['exercises'][ex_idx].get('name', 'This exercise')
        content.add_widget(Label(text=f"Delete '{ex_name}'?", size_hint_y=None, height=dp(40)))
        
        btn_row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        cancel_btn = Button(text="Cancel")
        delete_btn = Button(text="Delete", background_color=(1, 0.3, 0.3, 1))
        
        def confirm(*args):
            self.current_plan.days[day_idx]['exercises'].pop(ex_idx)
            self.save_plan()
            self.refresh_ui()
            popup.dismiss()
        
        cancel_btn.bind(on_press=lambda *a: popup.dismiss())
        delete_btn.bind(on_press=confirm)
        btn_row.add_widget(cancel_btn)
        btn_row.add_widget(delete_btn)
        content.add_widget(btn_row)
        
        popup = Popup(title="Confirm Delete", content=content, size_hint=(0.8, 0.4))
        popup.open()
    
    # =============================================================================
    # WORKOUT MODE
    # =============================================================================
    
    def build_workout_screen(self):
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(5), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for idx, day in enumerate(self.current_plan.days):
            if day.get('rest'):
                continue  # Skip rest days in workout mode
            
            # Workout day card
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(80),
                           canvas.before=[
                               kivy.graphics.Color(rgba=(0.9, 0.95, 1, 1)),
                               kivy.graphics.Rectangle(pos=self.root.pos, size=self.root.size)
                           ])
            
            day_label = Label(text=f"🏋️ {day['name']}", font_size='18sp', bold=True)
            start_btn = Button(text="▶️ Start Workout", size_hint_x=None, width=dp(150))
            start_btn.bind(on_press=lambda _, d=day: self.start_workout_session(d))
            
            card.add_widget(day_label)
            card.add_widget(start_btn)
            layout.add_widget(card)
        
        scroll.add_widget(layout)
        self.root.add_widget(scroll)
    
    def start_workout_session(self, day_data):
        # In a real app, this would launch a dedicated workout logging screen
        # For now, just toggle UI to show logging controls
        self.refresh_ui()
    
    def log_actual_set(self, day_idx, ex_idx):
        """Log what the user actually lifted (vs planned)"""
        exercise = self.current_plan.days[day_idx]['exercises'][ex_idx]
        
        # In a full implementation, this would open a quick modal to enter actual reps/weight
        # For demo, we'll just increment history with planned values
        actual_entry = {
            "sets": exercise.get('sets', 3),
            "reps": exercise.get('reps', 10),
            "weight": exercise.get('weight', 0),
            "date": datetime.now().isoformat(),
            "actual": True  # Flag to distinguish from planned values
        }
        exercise.setdefault('history', []).append(actual_entry)
        self.save_plan()
        
        # Visual feedback
        vibration.vibrate(0.1)  # Short haptic on log
        # Could show toast: "Set logged! 🎯"
    
    # =============================================================================
    # REST TIMER WITH VIBRATION FALLBACK
    # =============================================================================
    
    def start_rest_timer(self, seconds):
        """Start countdown with sound + vibration fallback"""
        self.rest_remaining = seconds
        self.rest_popup = Popup(
            title="⏱️ Rest Period",
            content=Label(text=f"{seconds}s", font_size='48sp', bold=True),
            size_hint=(0.7, 0.3),
            auto_dismiss=False
        )
        self.rest_popup.open()
        
        def update(dt):
            if self.rest_remaining > 0:
                self.rest_remaining -= 1
                self.rest_popup.content.text = f"{self.rest_remaining}s"
            else:
                Clock.unschedule(update)
                self.rest_popup.content.text = "✅ GO!"
                # Play sound if available
                if self.bell_sound:
                    try:
                        self.bell_sound.play()
                    except:
                        pass
                # Vibration fallback (always works)
                try:
                    vibration.vibrate(0.5)  # 500ms vibration
                except:
                    pass  # plyer not available on desktop
                # Auto-close after 2 seconds
                Clock.schedule_once(lambda dt: self.rest_popup.dismiss(), 2)
        
        Clock.schedule_interval(update, 1)
    
    # =============================================================================
    # EXERCISE LIBRARY MANAGER
    # =============================================================================
    
    def open_exercise_library(self, instance):
        content = ScrollView(size_hint=(1, None), size=(400, 400))
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Search bar
        search = TextInput(hint_text="Search exercises...", multiline=False, size_hint_y=None, height=dp(40))
        search.bind(text=self._filter_exercise_library)
        layout.add_widget(search)
        
        # Exercise list container
        self.lib_list_container = BoxLayout(orientation='vertical', spacing=dp(5))
        self._render_exercise_library()
        layout.add_widget(self.lib_list_container)
        
        # Add new exercise
        add_btn = Button(text="+ Add New Exercise", size_hint_y=None, height=dp(50),
                        background_color=(0.2, 0.8, 0.2, 1))
        add_btn.bind(on_press=self.add_new_exercise_to_library)
        layout.add_widget(add_btn)
        
        content.add_widget(layout)
        popup = Popup(title="📚 Exercise Library", content=content, size_hint=(0.95, 0.9))
        popup.open()
    
    def _render_exercise_library(self, query=""):
        self.lib_list_container.clear_widgets()
        results = self.exercise_lib.search(query) if query else self.exercise_lib.exercises.items()
        
        for key, ex_data in results:
            row = BoxLayout(size_hint_y=None, height=dp(50))
            row.add_widget(Label(text=ex_data['name'], size_hint_x=0.6))
            row.add_widget(Label(text=ex_data.get('muscle', ''), size_hint_x=0.2, color=(0.5, 0.5, 0.5, 1)))
            
            edit_btn = Button(text="✏️", size_hint_x=None, width=dp(40))
            edit_btn.bind(on_press=lambda _, k=key: self.edit_exercise_in_library(k))
            row.add_widget(edit_btn)
            
            self.lib_list_container.add_widget(row)
    
    def _filter_exercise_library(self, instance, query):
        self._render_exercise_library(query)
    
    def add_new_exercise_to_library(self, instance):
        # Simplified: in production, use a form popup
        key = f"custom_{len(self.exercise_lib.exercises)}"
        self.exercise_lib.add(key, "New Exercise", muscle="", equipment="")
        self._render_exercise_library()
    
    def edit_exercise_in_library(self, key):
        # Placeholder for edit form
        pass
    
    # =============================================================================
    # PROGRESS CHARTS (kivy-garden.graph)
    # =============================================================================
    
    def show_progress_charts(self, instance):
        try:
            from kivy.garden.graph import Graph, MeshLinePlot
        except ImportError:
            popup = Popup(
                title="Chart Error",
                content=Label(text="kivy-garden.graph not installed.\n\nInstall with:\npip install kivy-garden.graph"),
                size_hint=(0.8, 0.4)
            )
            popup.open()
            return
        
        # Collect data: best weight per exercise over time
        exercise_data = {}
        for day in self.current_plan.days:
            for ex in day.get('exercises', []):
                name = ex['name']
                for entry in ex.get('history', []):
                    if name not in exercise_data:
                        exercise_data[name] = []
                    # Convert date string to ordinal for x-axis
                    try:
                        date_obj = datetime.fromisoformat(entry['date'])
                        exercise_data[name].append((date_obj.toordinal(), entry['weight']))
                    except:
                        continue
        
        if not exercise_data:
            popup = Popup(
                title="No Data Yet",
                content=Label(text="Log some workouts to see progress charts! 💪"),
                size_hint=(0.8, 0.4)
            )
            popup.open()
            return
        
        # Build chart UI
        content = BoxLayout(orientation='vertical', padding=dp(10))
        
        # Dropdown to select exercise
        ex_dropdown = DropDown()
        for ex_name in exercise_data.keys():
            btn = Button(text=ex_name, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda btn, name=ex_name: self._update_chart(graph, exercise_data[name], name))
            ex_dropdown.add_widget(btn)
        
        select_ex_btn = Button(text="Select Exercise ▼", size_hint_y=None, height=dp(40))
        select_ex_btn.bind(on_release=ex_dropdown.open)
        content.add_widget(select_ex_btn)
        
        # Graph widget
        graph = Graph(
            xlabel='Date',
            ylabel=f'Weight ({self.unit})',
            x_ticks_minor=5,
            x_ticks_major=10,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            y_grid=True,
            x_grid=True,
            draw_border=True
        )
        
        # Plot first exercise by default
        first_ex = list(exercise_data.keys())[0]
        self._update_chart(graph, exercise_data[first_ex], first_ex)
        
        content.add_widget(graph)
        
        popup = Popup(title="📈 Strength Progress", content=content, size_hint=(0.95, 0.9))
        popup.open()
    
    def _update_chart(self, graph, data_points, exercise_name):
        graph.clear_plot()
        if not data_points:
            return
        
        # Sort by date
        data_points.sort(key=lambda x: x[0])
        
        plot = MeshLinePlot(color=[0.2, 0.6, 1, 1])
        plot.points = data_points
        graph.add_plot(plot)
        
        # Update axis labels
        graph.xlabel = 'Date'
        graph.ylabel = f'Weight ({self.unit})'
        graph.title = exercise_name
    
    # =============================================================================
    # EXPORT / BACKUP
    # =============================================================================
    
    def export_plan(self, instance):
        import json
        from kivy.utils import platform
        from kivy.core.clipboard import Clipboard
        
        export_data = {
            'plan': self.current_plan.to_dict(),
            'library': self.exercise_lib.exercises,
            'exported_at': datetime.now().isoformat()
        }
        
        json_str = json.dumps(export_data, indent=2)
        Clipboard.copy(json_str)
        
        popup = Popup(
            title="✅ Exported!",
            content=Label(text="Plan copied to clipboard!\n\nPaste into a note or email to backup."),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def on_pause(self):
        self.save_plan()
        return True
    
    def on_resume(self):
        pass

if __name__ == '__main__':
    SmartLiftApp().run()
