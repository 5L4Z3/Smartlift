[app]
title = SmartLift
package.name = smartlift
package.domain = com.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,buildozer,python-for-android
entrypoint = main.py
orientation = portrait

# Android build
android.api = 33
android.ndk = 25b
android.minapi = 21
android.archs = arm64-v8a  # Default; overridden by workflow
android.multiple_apks = True

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Presplash and icon
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
