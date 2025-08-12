[app]

# App metadata
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
name = SmartLift

# Source configuration
source.dir = .
source.main.py = main.py
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3
source.exclude_dirs = tests, bin

# Requirements (pin versions for reproducibility)
requirements = python3==3.10.12,kivy==2.2.1,setuptools,sdl2,pillow

# Android settings
orientation = portrait
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk_build_tools = 33.0.2
android.build_tools = 33.0.2    # Critical: prevent p4a from using 36+
android.ndk = 24                # Must be '24', not 'r24' to use local NDK
android.archs = arm64-v8a       # Faster build, smaller APK (remove to build for all)

# Assets
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

# Bootstrap
p4a.bootstrap = sdl2

# App behavior
android.allow_backup = true
android.fullscreen = 1
android.gradle_dependencies = 

# Buildozer settings
buildozer.build_log = 1
buildozer.target = android


[buildozer]

# General
log_level = 2
warn_on_root = 1
build_dir = .buildozer

# Auto-accept Android SDK license in CI
[buildozer:platform:android]
accept_android_sdk_license = True
