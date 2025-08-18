[app]
title = SmartLift
package.name = smartlift
package.domain = com.smartlift
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Icon and Presplash
icon.filename = assets/Icon.png
presplash.filename = assets/Preplash.png

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,VIBRATE

# Supported architectures
android.arch = arm64-v8a

# Entry point
entrypoint = main.py

# Packaging
package.format = apk

[buildozer]
log_level = 2
warn_on_root = 1

[app:source.include_patterns]
*.py
assets/*
