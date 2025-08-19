#!/usr/bin/env python3
import os

# Path to the libffi recipe in python-for-android
recipe_path = os.path.join(os.environ.get("P4A_RECIPES_DIR", ""), "libffi", "build", "libffi-3.4.2", "configure.ac")

if not os.path.exists(recipe_path):
    print("libffi configure.ac not found, skipping patch")
    exit(0)

patched_lines = []
with open(recipe_path, "r") as f:
    for line in f:
        # Correct AM_CONFIG_HEADER to AC_CONFIG_HEADERS
        patched_lines.append(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))

with open(recipe_path, "w") as f:
    f.writelines(patched_lines)

print("libffi patch applied successfully.")
