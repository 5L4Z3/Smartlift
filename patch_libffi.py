#!/usr/bin/env python3
"""
Patch the libffi recipe in python-for-android to fix the LT_SYS_SYMBOL_USCORE error.
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
        print("❌ libffi recipe not found!")
        return

    print(f"✅ Found libffi recipe at {init_py}")
    with open(init_py, 'r') as f:
        lines = f.readlines()

    patched_lines = []
    for line in lines:
        patched_lines.append(line)
        if '"LDFLAGS="' in line:
            patched_lines.append('        env["HAVE_HIDDEN"] = "0"\n')
    
    for i, line in enumerate(patched_lines):
        if '"--enable-shared"' in line and '"--disable-raw-api"' not in line:
            patched_lines[i] = '        "--enable-shared", "--disable-raw-api",\n'

    with open(init_py, 'w') as f:
        f.writelines(patched_lines)
    
    print("✅ libffi recipe patched successfully!")

if __name__ == "__main__":
    wait_and_patch()
