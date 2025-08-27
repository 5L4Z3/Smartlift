[app]
title = SmartLift
package.name = smartlift
package.domain = org.smartlift
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Multi-ABI builds (will be handled in workflow)
archs = armeabi-v7a, arm64-v8a, x86, x86_64

# Keystore (handled via GitHub Actions secrets)
android.release_keystore = release.keystore
android.release_keyalias = release-key-alias
