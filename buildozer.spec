[app]

# --- App Metadata ---
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
name = SmartLift

# --- Source Configuration ---
source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3
source.exclude_dirs = tests, bin

# --- Requirements ---
# These are the same as your p4a --requirements
requirements = python3==3.11.5,kivy==2.2.1,setuptools,sdl2,pillow,pyjnius

# --- Android Settings ---
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk_build_tools = 35.0.0
android.build_tools = 35.0.0
android.ndk = 27.2.12479018
android.archs = arm64-v8a

# --- Assets ---
# Make sure these files exist in your repo root
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

# --- Bootstrap ---
# Use sdl2 for full Kivy support
p4a.bootstrap = sdl2

# --- App Behavior ---
# Keep the screen on during workouts
android.wakelock = 1
# Use a dark theme if desired (optional)
# android.bootstrap = sdl2
# android.fullscreen = 1

# --- Buildozer Settings ---
# Set to 1 to see more logs
buildozer.build_log = 1
# Warn if running as root
buildozer.warn_on_root = 1
# Use a clean build directory
buildozer.build_dir = .buildozer

# --- Android SDK/NDK Paths (for local builds) ---
# These are ignored in CI but useful locally
[buildozer:platform:android]
# Automatically accept Android SDK licenses
accept_android_sdk_license = True

# --- p4a Flags (passed directly to p4a) ---
# Use this section to pass extra flags
[p4a]
# Whitelist your app files
whitelist = whitelist.txt
# Copy native libraries
# p4a.copy_libs = 1
# Use color in output
color = always
# Release build
release = 1
