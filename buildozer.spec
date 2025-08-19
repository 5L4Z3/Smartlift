#!/usr/bin/env python3
"""
patch_libffi.py

Waits for the python-for-android libffi recipe to exist and applies
a small, safe patch to avoid autoreconf/autogen errors such as:
  "error: possibly undefined macro: LT_SYS_SYMBOL_USCORE"

This script tries multiple likely locations for python-for-android recipes:
 - the installed python-for-android package location (preferred)
 - fallback: ~/.local/share/python-for-android/recipes/libffi/__init__.py
 - fallback: ~/.local/share/python-for-android/build/... (less common)

Intended usage:
  python .github/scripts/patch_libffi.py

Return codes:
  0 - patched or patch not needed
  1 - recipe not found after timeout or an unrecoverable failure
"""

from pathlib import Path
import time
import sys
import os

def find_init_py():
    """
    Attempt to locate the libffi recipe __init__.py file in several probable locations.
    Prefer the location under the installed python-for-android package if available.
    """
    # 1) Try to import pythonforandroid and construct the recipe path
    try:
        import pythonforandroid as p4a
        p4a_root = Path(p4a.__file__).resolve().parent
        candidate = p4a_root / "recipes" / "libffi" / "__init__.py"
        if candidate.exists():
            return candidate
    except Exception:
        # ignore; we'll try other locations
        pass

    # 2) Default user-local python-for-android recipes path
    home = Path.home()
    candidate = home / ".local" / "share" / "python-for-android" / "recipes" / "libffi" / "__init__.py"
    if candidate.exists():
        return candidate

    # 3) Another possible location used by some build systems
    candidate = home / ".local" / "share" / "python-for-android" / "build" / "recipes" / "libffi" / "__init__.py"
    if candidate.exists():
        return candidate

    # 4) Last resort: try scanning ~/.local/share/python-for-android for a libffi recipe directory
    base = home / ".local" / "share" / "python-for-android"
    if base.exists():
        for p in base.rglob("__init__.py"):
            if "recipes" in str(p) and "libffi" in str(p):
                return p

    return None

def apply_patch(init_py_path: Path):
    """
    Read file, make idempotent modifications, and write back.
    The modifications:
    - Insert env['HAVE_HIDDEN'] = '0' after a line containing '"LDFLAGS="'
    - Ensure the configure flags include "--disable-raw-api" alongside "--enable-shared"
    This is applied conservatively and only if not already present.
    """
    text = init_py_path.read_text(encoding="utf-8")
    original = text

    # 1) Add HAVE_HIDDEN after a "LDFLAGS=" occurrence (if not already present)
    if 'env["HAVE_HIDDEN"]' not in text and '"LDFLAGS="' in text:
        # insert after the first LDFLAGS line
        parts = text.splitlines()
        out_lines = []
        inserted = False
        for line in parts:
            out_lines.append(line)
            if not inserted and '"LDFLAGS="' in line:
                # Add a guarded insertion with indentation matching the file
                indent = ""
                # preserve leading whitespace from the line if any
                for ch in line:
                    if ch.isspace():
                        indent += ch
                    else:
                        break
                out_lines.append(f'{indent}env["HAVE_HIDDEN"] = "0"')
                inserted = True
        text = "\n".join(out_lines)

    # 2) Ensure "--disable-raw-api" appears next to "--enable-shared"
    if '"--enable-shared"' in text and '--disable-raw-api' not in text:
        text = text.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')

    if text != original:
        # Write a backup and write the new file
        bak = init_py_path.with_suffix(init_py_path.suffix + ".bak")
        try:
            init_py_path.rename(bak)
            bak.write_text(original, encoding="utf-8")  # ensure backup contains original
        except Exception:
            # if rename fails (e.g. permissions), still try to write backup as .bak
            try:
                init_py_path.with_suffix(init_py_path.suffix + ".bak").write_text(original, encoding="utf-8")
            except Exception:
                pass

        init_py_path.write_text(text, encoding="utf-8")
        print(f"✅ Patched libffi recipe at: {init_py_path}")
    else:
        print(f"ℹ️ No patch needed for: {init_py_path}")

def main(timeout_seconds=600, poll_interval=5):
    """
    Wait up to timeout_seconds for the recipe file to appear. Poll every poll_interval seconds.
    """
    t_start = time.time()
    print("⏳ Waiting for libffi recipe to appear (up to {:.0f}s)...".format(timeout_seconds))
    while True:
        p = find_init_py()
        if p:
            print(f"✅ Found candidate recipe file: {p}")
            try:
                apply_patch(p)
                return 0
            except Exception as exc:
                print(f"❌ Failed to apply patch: {exc}", file=sys.stderr)
                return 1

        if (time.time() - t_start) > timeout_seconds:
            print("❌ Timeout reached: libffi recipe not found.", file=sys.stderr)
            return 1

        time.sleep(poll_interval)

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
