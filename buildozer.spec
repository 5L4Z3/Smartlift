[app]
title = SmartLift
package.name = smartlift
package.domain = org.example
source.dir = .
source.include_exts = py
source.exclude_dirs = tests, bin
version = 1.0
requirements = python3,kivy,setuptools,sdl2,pillow
orientation = portrait
android.permissions = INTERNET

# Match CI environment
android.api = 33
android.minapi = 21
android.sdk_build_tools = 33.0.2
android.ndk = r24

# Optional: avoid Gradle version conflicts
# android.gradle_dependencies =  # ← Remove or comment out
# android.gradle_version =       # ← Let Buildozer decide

# Icon and presplash (add these files to your repo root!)
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.jpg

[buildozer]
log_level = 2
warn_on_root = 1

# Optional (usually not needed)
# p4a.bootstrap = sdl2
