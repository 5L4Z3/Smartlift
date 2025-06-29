[app]
title = SmartLift
package.name = smartlift
package.domain = org.example
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET

# Android config (matches GitHub workflow)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.sdk_build_tools = 33.0.2

# Prevent Buildozer from auto-updating SDK
android.ignore_sdk_update = 1

# Prevent use of newer incompatible Gradle plugins
android.gradle_dependencies = com.android.tools.build:gradle:7.4.2

[buildozer]
log_level = 2
warn_on_root = 1
