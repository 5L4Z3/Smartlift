"""
SmartLift Pro v2.0.0
Production-grade workout planner & logger
"""
import logging
import os
import json
import math
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path

import plyer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
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
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SmartLift")

kivy.require("2.2.1")

# ==============================================================================
# CONSTANTS & SCHEMA
# ==============================================================================
SCHEMA_VERSION = 2
APP_DIR = Path(__file__).parent

# ==============================================================================
# DATA LAYER
# ==============================================================================
class DataStore:
    """Handles JSON persistence with schema migration & versioning"""
    def __init__(self, filepath: str, default_data: Dict):
        self.path = Path(filepath)
        self.default_data = default_data
        self.data = self._load()

    def _load(self) -> Dict:
        if not self.path.exists():
            logger.info(f"Initializing new store at {self.path}")
            self.default_data["_schema_version"] = SCHEMA_VERSION
            self.save()
            return self.default_data.copy()

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Migration hook
        version = data.get("_schema_version", 0)
        if version < SCHEMA_VERSION:
            logger.info(f"Migrating store from v{version} to v{SCHEMA_VERSION}")
            data = self._migrate(data, version)
            data["_schema_version"] = SCHEMA_VERSION
            self.save()
        return data

    def _migrate(self, data: Dict, from_version: int) -> Dict:
        """Add migration logic here for future schema changes"""
        if from_version < 2:
            data.setdefault("unit", "kg")
        return data

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
        self.save()

# ==============================================================================
# UTILS & VALIDATION
# ==============================================================================
def parse_numeric(value: str, allow_negative: bool = False, allow_decimal: bool = True, default: float = 0.0) -> float:
    if not value or not value.strip():
        return default
    try:
        cleaned = value.strip().replace(",", ".")
        num = float(cleaned) if allow_decimal else int(float(cleaned))
        if not allow_negative and num < 0:
            raise ValueError("Negative values not allowed")
        return num
    except (ValueError, TypeError) as e:
        logger.warning(f"Numeric parse failed for '{value}': {e}")
        return default

def format_weight(value: float, unit: str = "kg") -> str:
    return f"{value:.1f} {unit}" if value else f"0 {unit}"

def safe_vibrate(duration: float = 0.5):
    try:
        plyer.vibration.vibrate(duration)
    except Exception as e:
        logger.debug(f"Vibration unavailable: {e}")

# ==============================================================================
# CUSTOM WIDGETS
# ==============================================================================
class LongPressBehavior(ButtonBehavior):
    """Mixin for long-press detection with proper Clock cleanup"""
    long_press_time = NumericProperty(0.5)
    on_long_press = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._trigger = Clock.create_trigger(self._dispatch_long_press, self.long_press_time)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.on_long_press:
            touch.grab(self)
            self._trigger()
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self._trigger.cancel()
            touch.ungrab(self)
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self and not self.collide_point(*touch.pos):
            self._trigger.cancel()
            touch.ungrab(self)
        return super().on_touch_move(touch)

    def _dispatch_long_press(self, dt):
        if self.on_long_press:
            self.on_long_press(self)

    def on_long_press_time(self, instance, value):
        self._trigger.cancel()
        self._trigger = Clock.create_trigger(self._dispatch_long_press, value)

class LongPressButton(LongPressBehavior, Label):
    pass

# ==============================================================================
# SCREENS
# ==============================================================================
class PlanningScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, padding=dp(5))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        self.layout.add_widget(self.scroll)

        btn_add = Button(text="➕ Add Day", size_hint_y=None, height=dp(50), background_color=(0.2, 0.8, 0.2, 1))
        btn_add.bind(on_press=lambda _: self.app_ref.add_day())
        self.layout.add_widget(btn_add)
        self.add_widget(self.layout)
        self._render_days()

    def _render_days(self):
        self.content.clear_widgets()
        for i, day in enumerate(self.app_ref.plan_data.get("days", [])):
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(100))
            with card.canvas.before:
                Color(rgba=(0.95, 0.95, 0.95, 1))
                self.rect = Rectangle(pos=card.pos, size=card.size)
                card.bind(pos=self._update_rect, size=self._update_rect)

            header = BoxLayout(size_hint_y=None, height=dp(40))
            title = LongPressButton(
                text=f"🗓️ {day.get('name', f'Day {i+1}')}",
                font_size=dp(16),
                color=(0, 0, 0, 1),
                on_long_press=lambda btn, idx=i: self.app_ref.confirm_delete_day(idx)
            )
            header.add_widget(title)
            header.add_widget(Label(text=f"({len(day.get('exercises', []))} exercises)", size_hint_x=None, width=dp(100), color=(0.5, 0.5, 0.5, 1)))
            edit_btn = Button(text="✏️ Edit", size_hint_x=None, width=dp(70))
            edit_btn.bind(on_press=lambda _, idx=i: self.app_ref.open_day_editor(idx))
            header.add_widget(edit_btn)
            card.add_widget(header)
            self.content.add_widget(card)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class WorkoutScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        self.scroll = ScrollView(size_hint=(1, 1))
        self.content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, padding=dp(10))
        self.content.bind(minimum_height=self.content.setter("height"))
        self.scroll.add_widget(self.content)
        self.add_widget(self.scroll)
        self._render_days()

    def _render_days(self):
        self.content.clear_widgets()
        for day in self.app_ref.plan_data.get("days", []):
            if day.get("rest", False):
                continue
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(60))
            with card.canvas.before:
                Color(rgba=(0.9, 0.95, 1, 1))
                self.rect = Rectangle(pos=card.pos, size=card.size)
                card.bind(pos=self._update_rect, size=self._update_rect)

            label = Label(text=f"🏋️ {day['name']}", font_size=dp(18), bold=True)
            btn = Button(text="▶️ Start", size_hint_x=None, width=dp(100))
            btn.bind(on_press=lambda _, d=day: self.app_ref.open_workout_logger(d))
            card.add_widget(label)
            card.add_widget(btn)
            self.content.add_widget(card)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class SettingsScreen(Screen):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref
        layout = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))

        layout.add_widget(Label(text="⚙️ Settings", font_size=dp(24), size_hint_y=None, height=dp(40)))

        unit_row = BoxLayout(size_hint_y=None, height=dp(40))
        unit_row.add_widget(Label(text="Weight Unit:", size_hint_x=None, width=dp(150)))
        self.switch_unit = Switch(active=self.app_ref.unit == "lb")
        self.switch_unit.bind(active=self.app_ref.toggle_unit)
        unit_row.add_widget(self.switch_unit)
        layout.add_widget(unit_row)

        btn_export = Button(text="💾 Export Data", size_hint_y=None, height=dp(50))
        btn_export.bind(on_press=lambda _: self.app_ref.export_data())
        layout.add_widget(btn_export)

        btn_charts = Button(text="📈 View Progress", size_hint_y=None, height=dp(50))
        btn_charts.bind(on_press=lambda _: self.app_ref.open_charts())
        layout.add_widget(btn_charts)

        btn_lib = Button(text="📚 Exercise Library", size_hint_y=None, height=dp(50))
        btn_lib.bind(on_press=lambda _: self.app_ref.open_library())
        layout.add_widget(btn_lib)

        self.add_widget(ScrollView(size_hint=(1, 1), content=layout))

# ==============================================================================
# MAIN APP
# ==============================================================================
class SmartLiftApp(App):
    title = APP_TITLE
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store: Optional[DataStore] = None
        self.plan_data: Dict = {}
        self.unit: str = "kg"
        self.workout_mode: bool = False
        self.sm: Optional[ScreenManager] = None
        self.bell_sound = None

    def build(self):
        self.sm = ScreenManager()
        self.sm.transition = SlideTransition()
        return self.sm

    def on_start(self):
        self._init_storage()
        self._init_audio()
        self._setup_navigation()

    def _init_storage(self):
        data_dir = self.user_data_dir
        os.makedirs(data_dir, exist_ok=True)
        default_plan = {
            "name": "Starter Plan",
            "days": [
                {"name": "Push Day", "rest": False, "exercises": []},
                {"name": "Pull Day", "rest": False, "exercises": []},
                {"name": "Rest Day", "rest": True, "exercises": []}
            ],
            "unit": "kg"
        }
        self.store = DataStore(os.path.join(data_dir, "smartlift_v2.json"), default_plan)
        self.plan_data = self.store.data
        self.unit = self.plan_data.get("unit", "kg")
        logger.info("Storage initialized")

    def _init_audio(self):
        try:
            self.bell_sound = SoundLoader.load("bell_sound.mp3")
        except Exception as e:
            logger.warning(f"Audio init failed: {e}")

    def _setup_navigation(self):
        self.planning_screen = PlanningScreen(self)
        self.workout_screen = WorkoutScreen(self)
        self.settings_screen = SettingsScreen(self)

        self.sm.add_widget(self.planning_screen)
        self.sm.add_widget(self.workout_screen)
        self.sm.add_widget(self.settings_screen)

        # Header bar
        self.header = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5), spacing=dp(10))
        self.btn_mode = Button(text="📝 Plan", size_hint_x=0.5)
        self.btn_mode.bind(on_press=self._toggle_mode)
        self.btn_settings = Button(text="⚙️", size_hint_x=0.2)
        self.btn_settings.bind(on_press=lambda _: self.sm.current = "settings")
        self.header.add_widget(self.btn_mode)
        self.header.add_widget(self.btn_settings)

        # Wrap screens in container
        container = BoxLayout(orientation="vertical")
        container.add_widget(self.header)
        container.add_widget(self.sm)
        Window.add_widget(container)
        self._container = container

    def _toggle_mode(self, *_):
        self.workout_mode = not self.workout_mode
        self.btn_mode.text = "🏋️ Workout" if self.workout_mode else "📝 Plan"
        self.sm.current = "workout" if self.workout_mode else "planning"
        # Refresh screens on entry
        if self.workout_mode:
            self.workout_screen._render_days()
        else:
            self.planning_screen._render_days()

    def toggle_unit(self, instance, value):
        self.unit = "lb" if value else "kg"
        self.store.set("unit", self.unit)
        logger.info(f"Unit changed to {self.unit}")

    def save_plan(self):
        self.store.set("days", self.plan_data.get("days", []))
        self.store.set("unit", self.unit)

    def add_day(self):
        idx = len(self.plan_data.get("days", [])) + 1
        self.plan_data.setdefault("days", []).append({
            "name": f"Day {idx}", "rest": False, "exercises": []
        })
        self.save_plan()
        self.planning_screen._render_days()

    def confirm_delete_day(self, idx: int):
        day_name = self.plan_data["days"][idx].get("name", "this day")
        popup = Popup(title="Delete Day?", size_hint=(0.8, 0.4))
        content = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(15))
        content.add_widget(Label(text=f"Delete '{day_name}'? This cannot be undone."))
        btns = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        cancel = Button(text="Cancel")
        delete = Button(text="Delete", background_color=(1, 0.3, 0.3, 1))

        cancel.bind(on_press=popup.dismiss)
        delete.bind(on_press=lambda _: self._delete_day(idx, popup))
        btns.add_widget(cancel)
        btns.add_widget(delete)
        content.add_widget(btns)
        popup.content = content
        popup.open()

    def _delete_day(self, idx: int, popup):
        self.plan_data["days"].pop(idx)
        self.save_plan()
        self.planning_screen._render_days()
        popup.dismiss()
        logger.info(f"Deleted day at index {idx}")

    def open_day_editor(self, idx: int):
        day = self.plan_data["days"][idx]
        popup = Popup(title=f"Edit: {day['name']}", size_hint=(0.95, 0.9))
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        name_input = TextInput(text=day["name"], multiline=False, size_hint_y=None, height=dp(40))
        name_input.bind(text=lambda i, v: self._update_day_name(idx, v))
        content.add_widget(name_input)

        rest_switch = Switch(active=day.get("rest", False))
        rest_switch.bind(active=lambda i, v: self._update_day_rest(idx, v))
        content.add_widget(rest_switch)

        for ex_idx, ex in enumerate(day.get("exercises", [])):
            content.add_widget(self._build_exercise_card(idx, ex_idx, ex))

        add_btn = Button(text="➕ Add Exercise", size_hint_y=None, height=dp(50))
        add_btn.bind(on_press=lambda _: self._add_exercise(idx))
        content.add_widget(add_btn)

        scroll.add_widget(content)
        popup.content = scroll
        popup.open()

    def _update_day_name(self, idx, name):
        self.plan_data["days"][idx]["name"] = name
        self.save_plan()

    def _update_day_rest(self, idx, is_rest):
        self.plan_data["days"][idx]["rest"] = is_rest
        self.save_plan()

    def _build_exercise_card(self, day_idx: int, ex_idx: int, exercise: Dict) -> BoxLayout:
        card = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(180), spacing=dp(5))
        with card.canvas.before:
            Color(rgba=(0.98, 0.98, 0.98, 1))
            self.rect = Rectangle(pos=card.pos, size=card.size)
            card.bind(pos=self._update_rect, size=self._update_rect)

        header = BoxLayout(size_hint_y=None, height=dp(35))
        header.add_widget(LongPressButton(
            text=f"💪 {exercise.get('name', 'Exercise')}",
            on_long_press=lambda _: self._delete_exercise(day_idx, ex_idx, card)
        ))
        header.add_widget(Label(text="(hold to del)", size_hint_x=None, width=dp(100), color=(0.6,0.6,0.6,1)))
        card.add_widget(header)

        # History
        hist = exercise.get("history", [])
        last = hist[-1] if hist else None
        card.add_widget(Label(text=f"Last: {last['sets']}x{last['reps']}@{last['weight']}{self.unit}" if last else "No history", size_hint_y=None, height=dp(25), color=(0.4,0.4,0.4,1)))

        # Inputs
        inputs = BoxLayout(size_hint_y=None, height=dp(80), spacing=dp(5))
        fields = [
            ("Sets", exercise.get("sets", 3), False, "sets"),
            ("Reps", exercise.get("reps", 10), False, "reps"),
            ("Weight", exercise.get("weight", 0), True, "weight"),
            ("Rest(s)", exercise.get("rest_time", 60), False, "rest_time")
        ]
        for hint, default, dec, key in fields:
            ti = TextInput(text=str(default), hint_text=hint, input_filter="int" if not dec else "float", size_hint_x=0.25, height=dp(40))
            ti.bind(on_text_validate=lambda i, k=key, d=default, dc=dec: self._save_exercise_field(day_idx, ex_idx, k, i.text, d, dc))
            inputs.add_widget(ti)
        card.add_widget(inputs)

        # Actions
        acts = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        rest_btn = Button(text="⏱️ Rest")
        rest_btn.bind(on_press=lambda _: self.start_rest_timer(exercise.get("rest_time", 60)))
        acts.add_widget(rest_btn)
        log_btn = Button(text="✓ Log", background_color=(0.2, 0.8, 0.2, 1))
        log_btn.bind(on_press=lambda _: self.log_set(day_idx, ex_idx))
        acts.add_widget(log_btn)
        card.add_widget(acts)
        return card

    def _save_exercise_field(self, d_idx, e_idx, key, val, default, allow_dec):
        self.plan_data["days"][d_idx]["exercises"][e_idx][key] = parse_numeric(val, allow_decimal=allow_dec, default=default)
        self.save_plan()

    def _add_exercise(self, idx):
        self.plan_data["days"][idx].setdefault("exercises", []).append({
            "name": "New Exercise", "sets": 3, "reps": 10, "weight": 0, "rest_time": 60, "history": []
        })
        self.save_plan()
        self.open_day_editor(idx)

    def _delete_exercise(self, d_idx, e_idx, widget):
        self.plan_data["days"][d_idx]["exercises"].pop(e_idx)
        self.save_plan()
        widget.parent.remove_widget(widget)

    def log_set(self, d_idx, e_idx):
        ex = self.plan_data["days"][d_idx]["exercises"][e_idx]
        ex.setdefault("history", []).append({
            "sets": ex["sets"], "reps": ex["reps"], "weight": ex["weight"],
            "date": datetime.now().isoformat()
        })
        self.save_plan()
        safe_vibrate(0.1)
        logger.info(f"Set logged: {ex['name']}")

    def start_rest_timer(self, seconds: int):
        if hasattr(self, "_timer_popup") and self._timer_popup:
            self._timer_popup.dismiss()
        self._timer_remaining = seconds
        self._timer_popup = Popup(title="⏱️ Resting", size_hint=(0.7, 0.3), auto_dismiss=False)
        self._timer_label = Label(text=f"{seconds}s", font_size=dp(48), bold=True)
        self._timer_popup.content = self._timer_label
        self._timer_popup.open()

        def tick(dt):
            if self._timer_remaining > 0:
                self._timer_remaining -= 1
                self._timer_label.text = f"{self._timer_remaining}s"
            else:
                Clock.unschedule(tick)
                self._timer_label.text = "✅ GO!"
                try: self.bell_sound.play() if self.bell_sound else None
                except: pass
                safe_vibrate(0.5)
                Clock.schedule_once(lambda _: self._timer_popup.dismiss(), 1.5)

        Clock.schedule_interval(tick, 1.0)

    def open_workout_logger(self, day):
        self.workout_mode = True
        self.btn_mode.text = "🏋️ Workout"
        self.sm.current = "workout"

    def export_data(self):
        try:
            import json
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(json.dumps(self.plan_data, indent=2))
            Popup(title="✅ Exported", content=Label(text="Copied to clipboard!"), size_hint=(0.6, 0.3)).open()
        except Exception as e:
            logger.error(f"Export failed: {e}")

    def open_charts(self):
        try:
            from kivy.garden.graph import Graph, MeshLinePlot
        except ImportError:
            Popup(title="Missing Dependency", content=Label(text="Install kivy-garden.graph"), size_hint=(0.7, 0.3)).open()
            return

        data = {}
        for day in self.plan_data.get("days", []):
            for ex in day.get("exercises", []):
                name = ex["name"]
                for entry in ex.get("history", []):
                    data.setdefault(name, []).append((datetime.fromisoformat(entry["date"]).toordinal(), entry["weight"]))

        if not data:
            Popup(title="No Data", content=Label(text="Log workouts first."), size_hint=(0.6, 0.3)).open()
            return

        popup = Popup(title="📈 Progress", size_hint=(0.95, 0.9))
        content = BoxLayout(orientation="vertical", padding=dp(10))
        dropdown = DropDown()
        for name in data:
            btn = Button(text=name, size_hint_y=None, height=dp(40))
            btn.bind(on_release=lambda btn, n=name: self._plot_data(graph, data[n], n))
            dropdown.add_widget(btn)
        sel = Button(text="Select Exercise ▼", size_hint_y=None, height=dp(40))
        sel.bind(on_release=dropdown.open)
        content.add_widget(sel)

        graph = Graph(xlabel="Date", ylabel=f"Weight ({self.unit})", x_ticks_minor=5, x_ticks_major=10, y_grid_label=True, x_grid_label=True, y_grid=True, x_grid=True, draw_border=True)
        content.add_widget(graph)

        first = list(data.keys())[0]
        self._plot_data(graph, data[first], first)
        popup.content = content
        popup.open()

    def _plot_data(self, graph, points, title):
        graph.clear_plots()
        points.sort(key=lambda x: x[0])
        plot = MeshLinePlot(color=[0.2, 0.6, 1, 1])
        plot.points = points
        graph.add_plot(plot)
        graph.title = title

    def open_library(self):
        Popup(title="📚 Library", content=Label(text="Library management coming in v2.1"), size_hint=(0.7, 0.4)).open()

    def _update_rect(self, instance, value):
        pass  # Handled in screen builds

    def on_pause(self):
        self.save_plan()
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    SmartLiftApp().run()
