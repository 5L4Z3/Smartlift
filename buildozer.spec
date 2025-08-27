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

# Android settings
android.api = 33
android.ndk = 25b
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a, x86, x86_64
android.multiple_apks = True

# Keystore (signed via GitHub secrets)
android.keystore = release.keystore
android.keyalias = ${ANDROID_KEY_ALIAS}
android.keyalias_password = ${ANDROID_KEY_PASSWORD}

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
