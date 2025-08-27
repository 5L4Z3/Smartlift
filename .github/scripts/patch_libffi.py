#!/usr/bin/env python3
import os

p4a_dir = os.path.expanduser("~/.buildozer/android/platform/python-for-android")
libffi_dir = os.path.join(p4a_dir, "pythonforandroid/recipes/libffi")

if not os.path.isdir(libffi_dir):
    print("libffi directory not found, skipping patch.")
else:
    patched_file = os.path.join(libffi_dir, "build.py")
    with open(patched_file, "r") as f:
        lines = f.readlines()
    with open(patched_file, "w") as f:
        for line in lines:
            f.write(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))
    print("libffi patch applied successfully.")
