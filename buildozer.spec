# -*- coding: utf-8 -*-
# Buildozer configuration file for SmartLift Android app

[app]
# (Replace with your app details)
title = SmartLift
package.name = smartlift
package.domain = com.yourcompany
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.target = 33
# ABI will be replaced per matrix job
android.arch = __ABI__

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# Requirements (example, adapt to your project)
requirements = python3,kivy,cython,requests,openssl,libffi

# Additional Android configs
android.sdk_path = /opt/android-sdk
android.ndk_path = /opt/android-ndk
android.gradle_dependencies =
    androidx.appcompat:appcompat:1.6.1

# Signing config placeholders (to use GitHub Secrets)
# These will be set via buildozer command
# android.release_keystore = my-release-key.keystore
# android.keystore_password = <keystore-password>
# android.keyalias_name = <key-alias>
# android.keyalias_password = <key-password>

[buildozer]
log_level = 2
warn_on_root = 1
