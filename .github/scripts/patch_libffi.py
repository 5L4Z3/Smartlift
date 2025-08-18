#!/usr/bin/env python3
"""
Patch the libffi recipe in python-for-android to fix LT_SYS_SYMBOL_USCORE errors.

This script:
- Waits for the libffi recipe directory
- Checks if patch is already applied
- Applies patch only if necessary
"""

import os
import time
from pathlib import Path

def patch_libffi():
    home = Path.home()
    recipe_dir = home / ".local" / "share" / "python-for-android" / "recipes" / "libffi"
    init_py = recipe_dir / "__init__.py"

    print("⏳ Waiting for libffi recipe to appear (max 5 min)...")
    for _ in range(30):  # Wait up to 5 minutes
        if init_py.exists():
            break
        time.sleep(10)
    else:
        print("❌ libffi recipe not found after 5 minutes! Exiting.")
        return False

    print(f"✅ Found libffi recipe: {init_py}")

    with open(init_py, "r") as f:
        content = f.read()

    if 'env["HAVE_HIDDEN"] = "0"' in content:
        print("⚡ Patch already applied. Skipping.")
        return True

    print("🔧 Applying libffi patch...")
    lines = content.splitlines(keepends=True)
    patched_lines = []
    inserted = False

    for line in lines:
        patched_lines.append(line)
        if '"LDFLAGS="' in line and not inserted:
            patched_lines.append('        env["HAVE_HIDDEN"] = "0"\n')
            inserted = True

    patched_lines = [
        line.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')
        if '"--enable-shared"' in line and '"--disable-raw-api"' not in line else line
        for line in patched_lines
    ]

    with open(init_py, "w") as f:
        f.writelines(patched_lines)

    print("✅ libffi patch applied successfully.")
    return True


if __name__ == "__main__":
    success = patch_libffi()
    if not success:
        exit(1)
