[app]
title = SmartLift
package.name = smartlift
package.domain = org.smartlift.app
version = 2.0.0
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3,ttf,otf,md,txt

requirements = python3,kivy==2.2.1,pillow,plyer,kivy-garden.graph,sdl2

orientation = portrait
android.permissions = VIBRATE,INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = true
android.backup_rules = auto

# Multi-ABI support (overridden by CI matrix)
android.archs = armeabi-v7a,arm64-v8a,x86,x86_64

# Android SDK/NDK
android.api = 34
android.minapi = 21
android.ndk = 27.2.12479018
android.sdk_build_tools = 35.0.0

# Assets
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Presplash.png

# P4A config
p4a.bootstrap = sdl2
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
