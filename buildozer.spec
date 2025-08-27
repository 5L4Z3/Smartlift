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
android.archs = arm64-v8a  # Default; workflow will override
android.multiple_apks = True

# Keystore (uncomment workflow will handle these automatically)
# android.keystore = release.keystore
# android.keyalias = my_key_alias
# android.keyalias_password = my_password

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Presplash and icon
presplash.filename = %(source.dir)s/images/presplash.png
icon.filename = %(source.dir)s/images/icon.png
