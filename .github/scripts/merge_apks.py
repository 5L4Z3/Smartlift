#!/usr/bin/env python3
"""Universal APK generator using bundletool (Android standard)."""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: merge_apks.py <aab_path> <output_apks_path>")
        sys.exit(1)

    aab, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    if not aab.exists():
        logger.error(f"AAB not found: {aab}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    bundletool = os.environ.get("BUNDLETOOL", "bundletool")

    try:
        subprocess.run([
            bundletool, "build-apks",
            "--bundle", str(aab),
            "--output", str(out_dir / "universal.apks"),
            "--mode=universal"
        ], check=True)
        print("✅ Universal APKs generated via bundletool")
    except FileNotFoundError:
        print("⚠️ bundletool not found. Copying arm64-v8a APK as fallback.")
        src = list(Path(".").rglob("*arm64-v8a*.apk"))
        if src:
            shutil.copy(src[0], out_dir / "fallback.apk")
        else:
            print("❌ No APKs found to fallback.")
            sys.exit(1)

if __name__ == "__main__":
    main()
