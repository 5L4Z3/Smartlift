[app]
title = SmartLift
package.name = smartlift
package.domain = org.smartlift
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Entry point
source.main = main.py

# Icon and presplash
icon.filename = assets/Icon.png
presplash.filename = assets/Preplash.png

[buildozer]
log_level = 2

# Comment out here, gets replaced in workflow
# android.arch = armeabi-v7a

# Universal APK will be forced in workflow
# android.arch = all

# (str) Android entry point, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions
android.permissions = INTERNET

# (bool) Indicate if the .apk should be signed
android.release = 1
