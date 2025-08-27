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

# Android
android.api = 33
android.ndk = 25b
android.minapi = 21
android.sdk = 33
android.arch = arm64-v8a
android.multiple_apks = True
# Uncomment to sign via GH secrets
# android.keystore = ${ANDROID_KEYSTORE}
# android.keyalias = ${ANDROID_KEY_ALIAS}
# android.keyalias_password = ${ANDROID_KEY_PASSWORD}

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
