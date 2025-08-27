#!/usr/bin/env python3
"""
Optional patch script for libffi.
Used to fix build issues on some architectures.
"""
import os
import sys

libffi_dir = os.path.join(os.getcwd(), '.buildozer', 'android', 'platform', 'build', 'other_builds', 'libffi')
if not os.path.exists(libffi_dir):
    print("Libffi directory not found, skipping patch.")
    sys.exit(0)

# Example patch: replace AM_CONFIG_HEADER with AC_CONFIG_HEADERS in configure.ac
configure_path = os.path.join(libffi_dir, 'configure.ac')
if os.path.exists(configure_path):
    with open(configure_path, 'r') as f:
        lines = f.readlines()

    with open(configure_path, 'w') as f:
        for line in lines:
            f.write(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))

    print("Libffi patched successfully.")
else:
    print("configure.ac not found, nothing patched.")
