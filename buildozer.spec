[app]
title = SmartLift
package.name = smartlift
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,mp3,txt,atlas
version = 1.0.0
# Your app's main module:
entrypoint = main.py
requirements = python3,kivy==2.2.1,pillow,sdl2
orientation = portrait
fullscreen = 0
log_level = 2

# Images (make sure files exist in repo root or adjust paths)
presplash.filename = Preplash.png
icon.filename = Icon.png

# Runtime permissions you actually use
android.permissions = INTERNET, WAKE_LOCK

# API levels
android.api = 33
android.minapi = 21

# NDK left unspecified: p4a picks a working one automatically
# android.ndk = 27c

# Build architectures (overridden by GitHub Actions)
android.archs = arm64-v8a
# Legacy single-arch token kept for compatibility; set by workflow too
android.arch = arm64-v8a

# Keep the default bootstrap
android.bootstrap = sdl2

# Reduce noise in logs
warn_on_root = 0

# Optional: include only if you have a whitelist file
# android.whitelist = whitelist.txt

[buildozer]
log_level = 2
warn_on_root = 0
