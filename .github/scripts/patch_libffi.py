#!/usr/bin/env python3
"""
Patch libffi to fix AC_CONFIG_HEADERS issue in Python-for-Android builds.
"""

input_file = "recipes/libffi/libffi-3.4.2/configure.ac"
output_file = input_file + ".patched"

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        # Replace AM_CONFIG_HEADER with AC_CONFIG_HEADERS safely
        f_out.write(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))

# Replace original file
import shutil
shutil.move(output_file, input_file)

print("[patch_libffi.py] libffi patched successfully.")
