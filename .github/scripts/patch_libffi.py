#!/usr/bin/env python3
"""
Non-fatal libffi recipe patcher for python-for-android.

- Searches common recipe locations.
- If the file is found, applies two tweaks:
    1) env["HAVE_HIDDEN"] = "0"   (right after the LDFLAGS line)
    2) add "--disable-raw-api" to the configure args (with --enable-shared)
- If not found, exits 0 (skips).
"""

from __future__ import annotations
import os
import sys
import re
from pathlib import Path

def find_recipe_paths() -> list[Path]:
    candidates = []

    # 1) Site-packages install of python-for-android
    try:
        import pythonforandroid as p4a  # type: ignore
        p4a_dir = Path(p4a.__file__).resolve().parent
        candidates.append(p4a_dir / "recipes" / "libffi" / "__init__.py")
    except Exception:
        pass

    # 2) User cache that p4a sometimes uses during build
    candidates.append(Path.home() / ".local" / "share" / "python-for-android" / "recipes" / "libffi" / "__init__.py")

    # 3) Buildozer local workspace (if any)
    candidates.append(Path(".buildozer") / "android" / "platform" / "python-for-android" / "recipes" / "libffi" / "__init__.py")

    # Filter to existing files (unique)
    seen = set()
    out = []
    for p in candidates:
        if p.exists() and p not in seen:
            out.append(p)
            seen.add(p)
    return out

def patch_libffi_init(pyfile: Path) -> bool:
    original = pyfile.read_text(encoding="utf-8")
    patched = original

    # Add env["HAVE_HIDDEN"] = "0" after a line that sets LDFLAGS=
    if 'env["HAVE_HIDDEN"]' not in patched:
        patched = re.sub(
            r'(^\s*env\["LDFLAGS"\].*$)',
            r'\1\n        env["HAVE_HIDDEN"] = "0"',
            patched,
            flags=re.MULTILINE
        )

    # Ensure --disable-raw-api accompanies --enable-shared
    if "--disable-raw-api" not in patched:
        patched = patched.replace(
            '"--enable-shared"',
            '"--enable-shared", "--disable-raw-api"'
        )

    if patched != original:
        pyfile.write_text(patched, encoding="utf-8")
        print(f"[libffi] Patched: {pyfile}")
        return True

    print(f"[libffi] Already patched: {pyfile}")
    return False

def main() -> int:
    paths = find_recipe_paths()
    if not paths:
        print("libffi recipe not found yet; skipping patch (this is OK).")
        return 0

    changed_any = False
    for p in paths:
        try:
            changed_any |= patch_libffi_init(p)
        except Exception as e:
            print(f"[libffi] Patch error at {p}: {e}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
