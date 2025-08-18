[app]
title = SmartLift
package.name = smartlift
package.domain = org.smartlift
version = 1.0.0
source.dir = .
source.main_py = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3

requirements = python3,kivy==2.2.1,pillow

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 35
android.ndk = 27c
android.archs = arm64-v8a
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1, androidx.constraintlayout:constraintlayout:2.1.4

icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

p4a.bootstrap = sdl2
p4a.local_recipes = recipes

log_level = 2
warn_on_root = 1
build_dir = .buildozer
