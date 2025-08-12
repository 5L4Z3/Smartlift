[app]

title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
name = SmartLift

source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3
source.exclude_dirs = tests, bin

requirements = python3==3.10.12,kivy==2.2.1,setuptools,sdl2,pillow

orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk_build_tools = 33.0.2
android.ndk = 24
android.archs = arm64-v8a

icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

p4a.bootstrap = sdl2
android.allow_backup = true
android.fullscreen = 1

buildozer.build_log = 1
buildozer.target = android

[buildozer]

log_level = 2
warn_on_root = 1
build_dir = .buildozer

[buildozer:platform:android]
accept_android_sdk_license = True
