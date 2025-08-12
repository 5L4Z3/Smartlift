[app]

# App metadata
title = SmartLift
package.name = smartlift
package.domain = org.example
version = 1.0
source.dir = .
source.include_exts = py
source.exclude_dirs = tests, bin

# Kivy requirements
requirements = python3,kivy,setuptools,sdl2,pillow

# Android settings
orientation = portrait
android.permissions = INTERNET

# SDK/NDK Versions (must match CI)
android.api = 33
android.minapi = 21
android.sdk_build_tools = 33.0.2
android.ndk = r24

# Icon and splash screen (required to avoid warnings)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.jpg

# Gradle: Let Buildozer handle it
# android.gradle_dependencies =
# android.gradle_version =

[buildozer]

# Build settings
log_level = 2
warn_on_root = 1

# p4a.bootstrap = sdl2  # optional, default
