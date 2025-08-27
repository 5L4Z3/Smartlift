#!/usr/bin/env python3
import os

libffi_path = os.path.join(os.getcwd(), ".buildozer", "android", "platform", "build-arm64-v8a", "libffi")
if not os.path.exists(libffi_path):
    print("libffi directory not found, skipping patch.")
else:
    print("Patching libffi...")
    file_path = os.path.join(libffi_path, "configure.ac")
    with open(file_path, "r") as f:
        content = f.read()
    content = content.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS")
    with open(file_path, "w") as f:
        f.write(content)
    print("libffi patched successfully.")
