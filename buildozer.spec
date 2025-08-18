[app]
# App metadata
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3

# Requirements - keep in sync with the workflow
requirements = python3,kivy==2.2.1,pillow,sdl2

# Android
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.build_tools = 35.0.0
android.ndk = 27.2.12479018
android.archs = arm64-v8a, armeabi-v7a, x86_64

# Assets
icon.filename = Icon.png
presplash.filename = Preplash.png

# P4A / Buildozer
p4a.bootstrap = sdl2
p4a.whitelist = whitelist.txt

# Buildozer behavior
log_level = 2
warn_on_root = 1
build_dir = .buildozer

[buildozer:platform:android]
accept_android_sdk_license = True
