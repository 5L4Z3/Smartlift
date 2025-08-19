# buildozer.spec - polished production-ready configuration for SmartLift
#
# Notes:
# - Default android.arch is set to armeabi-v7a. The GitHub Actions workflow
#   replaces this line per-matrix job and for the universal build.
# - Signing values (keystore path / alias / passwords) can be injected at
#   runtime via environment variables and the workflow decodes the keystore
#   from a GitHub Secret into a file and sets ANDROID_KEYSTORE_PATH.
#
[app]

# (str) Title of your application
title = SmartLift

# (str) Package name (should be unique)
package.name = smartlift
package.domain = com.example

# (str) Application versioning
version = 2.0.0

# (str) Source dir / main
source.dir = .
source.main = main.py

# (list) Whitelist of file extensions to include in the apk
source.include_exts = py,png,jpg,jpeg,kv,atlas,mp3

# (list) Application requirements
# Pin kivy to a known working version to reduce variability in CI
requirements = python3,kivy==2.2.1,pillow

# (str) Orientation
orientation = portrait

# (str) Android permissions
android.permissions = INTERNET

# (int) Android API target
android.api = 33
android.minapi = 21

# (str) Build tools / NDK
# Note: p4a may accept a NDK version string. Use the NDK installed by workflow.
android.sdk_build_tools = 35.0.0
android.ndk = 27.2.12479018

# (str) Target architectures. This is the default, CI replaces it per job.
# Valid values: armeabi-v7a, arm64-v8a, x86, x86_64, or comma-separated set.
android.arch = armeabi-v7a

# (str) Assets - ensure these filenames match your repo exactly
# In your repo you currently have Preplash.png (typo preserved to match)
icon.filename = %(source.dir)s/Icon.png
presplash.filename = %(source.dir)s/Preplash.png

# p4a bootstrap and whitelist
p4a.bootstrap = sdl2
p4a.whitelist = whitelist.txt

# Local buildozer/debug settings
log_level = 2
warn_on_root = 1

[buildozer]
# use a predictable build directory
build_dir = ./.buildozer
