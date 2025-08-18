#!/usr/bin/env python3
"""
Patch the libffi recipe in python-for-android to fix the LT_SYS_SYMBOL_USCORE error.
This script waits for the recipe to be created and patches it.
"""

import os
import time
from pathlib import Path

def wait_and_patch():
    home = Path.home()
    recipe_dir = home / ".local" / "share" / "python-for-android" / "recipes" / "libffi"
    init_py = recipe_dir / "__init__.py"

    print("⏳ Waiting for libffi recipe to be created...")
    for _ in range(600):  # Wait up to 10 minutes
        if init_py.exists():
            break
        time.sleep(10)
    else:
        print("❌ libffi recipe not found after 10 minutes!")
        return

    print(f"✅ Found libffi recipe at {init_py}")

    # Read original file
    with open(init_py, 'r') as f:
        lines = f.readlines()

    # Patch
    patched_lines = []
    inserted_have_hidden = False
    for line in lines:
        patched_lines.append(line)
        if '"LDFLAGS="' in line and not inserted_have_hidden:
            patched_lines.append('        env["HAVE_HIDDEN"] = "0"\n')
            inserted_have_hidden = True

    # Replace shared flag
    patched_lines = [
        line.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')
        if '"--enable-shared"' in line and '"--disable-raw-api"' not in line
        else line
        for line in patched_lines
    ]

    # Write patched file
    with open(init_py, 'w') as f:
        f.writelines(patched_lines)

    print("✅ libffi recipe patched successfully! Ready for build.")

if __name__ == "__main__":
    wait_and_patch()
