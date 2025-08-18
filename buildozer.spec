[app]
title = SmartLift
package.name = smartlift
package.domain = com.example
source.include_exts = py,png,jpg,kv,atlas
version = 2.0.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a,arm64-v8a,x86,x86_64
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Signing (via environment variables / GH Secrets)
android.keystore = %(ANDROID_KEYSTORE_PATH)s
android.keyalias = %(ANDROID_KEY_ALIAS)s
android.keyalias_password = %(ANDROID_KEY_PASSWORD)s

[buildozer]
log_level = 2
warn_on_root = 1
