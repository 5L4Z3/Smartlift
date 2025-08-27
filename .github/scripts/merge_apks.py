#!/usr/bin/env python3
import sys
import zipfile
import shutil
from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description="Merge multiple APKs into one universal APK")
parser.add_argument('--output', required=True, help='Output APK path')
parser.add_argument('apks', nargs='+', help='List of APKs to merge')
args = parser.parse_args()

output_apk = args.output
temp_dir = Path("merged_apk")
shutil.rmtree(temp_dir, ignore_errors=True)
temp_dir.mkdir()

for apk_path in args.apks:
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

with zipfile.ZipFile(output_apk, 'w') as zip_out:
    for file in temp_dir.rglob('*'):
        zip_out.write(file, file.relative_to(temp_dir))

print(f"Universal APK created at {output_apk}")
