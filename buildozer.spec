[app]
# (str) Title of your application
title = SmartLift

# (str) Package name
package.name = smartlift

# (str) Package domain (unique identifier)
package.domain = com.yourdomain

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application requirements
requirements = python3,kivy

# (str) Entry point of the app
entrypoint = main.py

# (str) Supported orientation
orientation = portrait

# Android configs
android.api = 33
android.ndk = 25b
android.minapi = 21
android.sdk = 33

# (str) Architecture - will be replaced by GitHub Actions per matrix
android.arch = arm64-v8a

# (bool) Include universal APK (built in separate job)
android.multiple_apks = True

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Presplash image
presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon
icon.filename = %(source.dir)s/images/icon.png

# Uncomment when setting up release signing
# android.keystore = ${ANDROID_KEYSTORE}
# android.keyalias = ${ANDROID_KEY_ALIAS}
# android.keyalias_password = ${ANDROID_KEY_PASSWORD}
