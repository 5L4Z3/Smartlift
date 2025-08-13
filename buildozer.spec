[app]

# App metadata
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3

# Requirements
requirements = python3,kivy==2.2.1,pillow,sdl2

# Android settings
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk_build_tools = 35.0.0
android.build_tools = 35.0.0
android.ndk = 27.2.12479018
android.archs = arm64-v8a

# Assets
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

# Build settings
p4a.bootstrap = sdl2
p4a.whitelist = whitelist.txt

# Buildozer settings
buildozer.build_log = 1
buildozer.warn_on_root = 1
buildozer.target = android

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = .buildozer

[buildozer:platform:android]
accept_android_sdk_license = True
