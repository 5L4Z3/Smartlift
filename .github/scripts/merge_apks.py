#!/usr/bin/env python3
"""
Simple placeholder APK merger: picks the first ABI APK and copies it as 'universal'.
For real universal multi-ABI bundles use: build a .aab and deploy via Google Play (recommended).
"""
import os
import sys
import shutil

def main():
    if len(sys.argv) != 3:
        print("Usage: merge_apks.py <apk_folder> <output_apk>")
        sys.exit(2)

    apk_folder, output = sys.argv[1], sys.argv[2]
    files = []
    for root, _, files_in in os.walk(apk_folder):
        for f in files_in:
            if f.endswith(".apk"):
                files.append(os.path.join(root, f))
    if not files:
        print("No APKs found in", apk_folder)
        sys.exit(1)

    print("Found APKs:", files)
    # Pick the first ABI APK as placeholder universal
    shutil.copy(files[0], output)
    print("Copied", files[0], "to", output)
    sys.exit(0)

if __name__ == "__main__":
    main()
