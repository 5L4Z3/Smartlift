[app]

# (str) Title of your application
title = SmartLift

# (str) Package name
package.name = smartlift

# (str) Package domain (needed for Android packaging)
package.domain = com.example

# (str) Source code where the main.py lives
source.dir = .

# (str) Main entry point
source.main = main.py

# (str) Version number
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,python-for-android,sh

# (str) Icon of the app
icon.filename = %(source.dir)s/assets/icon.png

# (str) Presplash of the app
presplash.filename = %(source.dir)s/assets/presplash.png

# (bool) Include all source files
include.source = True

# (str) Orientation: portrait, landscape or all
orientation = portrait

# (list) Supported platforms
# android only for now
android.arch = all

# (bool) Allow backup
android.allowBackup = True

# (str) Minimum API level
android.minapi = 21

# (str) Target API level
android.api = 33

# (str) NDK API level
android.ndk = 25b

# (str) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Keystore info will be injected via GitHub Actions secrets
android.release_keystore = android.keystore
android.release_keyalias = %(ANDROID_KEY_ALIAS)s
android.release_keypass = %(ANDROID_KEY_PASSWORD)s
android.release_storepass = %(ANDROID_KEYSTORE_PASSWORD)s

# (str) Version code
android.version_code = 1

# (bool) Android fullscreen
fullscreen = 1

# (bool) Android presplash fade
presplash.fade = 1

# (bool) Copy all Python modules automatically
android.copy_libs = True

# (bool) Enable SDL2
android.use_sdl2 = True

# (bool) Enable patching of libffi (Python-for-Android)
android.patch_libffi = True

# (str) Additional build flags
android.extra_flags = --disable-raw-api

# (list) Exclude unnecessary files
exclude_patterns = *.pyc, *.pyo, __pycache__, .git, .github

# (bool) Use virtual environment
use_venv = True
