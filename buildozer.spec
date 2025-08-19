[app]
# (str) Title of your application
title = SmartLift

# (str) Package name
package.name = smartlift

# (str) Package domain (unique identifier)
package.domain = com.yourdomain

# (str) Source code directory
source.dir = .

# (list) Source files to include (leave empty to include all)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application requirements
requirements = python3,kivy,buildozer,python-for-android

# (str) Entry point of the app
entrypoint = main.py

# (str) Supported orientation
orientation = portrait

# (int) Android API level
android.api = 33
android.ndk = 25b
android.minapi = 21
android.sdk = 33

# (str) Default architecture; workflow will override this per-ABI
android.arch = arm64-v8a

# (bool) Include universal APK
android.multiple_apks = True

# (str) Keystore (for release builds via GH Secrets)
# android.keystore = ${ANDROID_KEYSTORE}
# android.keyalias = ${ANDROID_KEY_ALIAS}
# android.keyalias_password = ${ANDROID_KEY_PASSWORD}

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Presplash image
presplash.filename = %(source.dir)s/images/presplash.png

# (str) Icon
icon.filename = %(source.dir)s/images/icon.png
