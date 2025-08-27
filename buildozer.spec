[app]
title = SmartLift
package.name = smartlift
package.domain = com.yourdomain
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,python-for-android
entrypoint = main.py
orientation = portrait

# Android settings
android.api = 33
android.ndk = 25b
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a, x86, x86_64
android.multiple_apks = True

# Keystore (release signing)
android.keystore = release.keystore
android.keyalias = smartlift
android.keyalias_password = 123456
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Assets
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
