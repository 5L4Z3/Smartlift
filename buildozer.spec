[app]
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3

requirements = python3,kivy==2.2.1,pillow,sdl2

orientation = portrait
android.permissions = INTERNET

# prefer archs token (multi-apk support)
# default value will be overridden by the workflow per-ABI step
android.archs = armeabi-v7a, arm64-v8a, x86, x86_64

# NDK / SDK
android.api = 33
android.minapi = 21
android.ndk = 27.2.12479018
android.sdk_build_tools = 35.0.0

# Assets
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

# Use p4a bootstrap
p4a.bootstrap = sdl2

# Use p4a develop branch to get AAB support
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
