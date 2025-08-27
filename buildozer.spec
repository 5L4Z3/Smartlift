[app]
# Title of your application
title = SmartLift

# Package name
package.name = smartlift

# Package domain (unique identifier)
package.domain = com.yourdomain

# Source code directory
source.dir = .

# Source files to include (empty = include all)
source.include_exts = py,png,jpg,kv,atlas

# Application version
version = 1.0.0

# Application requirements
requirements = python3,kivy,python-for-android,cython

# Entry point of the app
entrypoint = main.py

# Supported orientation
orientation = portrait

# Android settings
android.api = 33
android.ndk = 25b
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a, x86, x86_64  # multiple ABI support
android.multiple_apks = True

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Presplash and icon
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png

# Keystore (release signing via GH secrets)
# android.keystore = ${ANDROID_KEYSTORE}
# android.keyalias = ${ANDROID_KEY_ALIAS}
# android.keyalias_password = ${ANDROID_KEY_PASSWORD}
