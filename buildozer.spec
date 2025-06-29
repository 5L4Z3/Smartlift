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

android.api = 33
android.minapi = 21
android.sdk_build_tools = 33.0.2
android.ndk = 25b
android.ndk_api = 21

android.ignore_sdk_update = 1

# Optional, pin Gradle plugin version to avoid incompatibility:
android.gradle_dependencies = com.android.tools.build:gradle:7.4.2

[buildozer]
log_level = 2
warn_on_root = 1
