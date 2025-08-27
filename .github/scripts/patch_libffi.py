#!/usr/bin/env python3
"""
Patch libffi headers for compatibility with older p4a recipes.
Safe to keep in repo; modern python-for-android no longer requires this,
but it will not break builds.
"""

import os
import sys

def main():
    # Attempt to locate libffi source directory
    p4a_build_dir = os.path.join(os.getcwd(), ".buildozer", "android", "platform", "libffi")
    if not os.path.isdir(p4a_build_dir):
        print("libffi directory not found, skipping patch.")
        sys.exit(0)

    patched_files = 0
    for root, _, files in os.walk(p4a_build_dir):
        for file in files:
            if file.endswith(".h"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                new_lines = [line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS") for line in lines]
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                patched_files += 1

    print(f"Patched {patched_files} libffi header files.")

if __name__ == "__main__":
    main()
