#!/usr/bin/env python3
"""
Deterministic patch of the installed python-for-android libffi recipe.
Idempotent and safe for CI/local use.
"""

import sys
from pathlib import Path
try:
    import pythonforandroid as p4a
except Exception as e:
    print("❌ pythonforandroid import failed:", e)
    sys.exit(1)

p4a_dir = Path(p4a.__file__).parent
recipe = p4a_dir / "recipes" / "libffi" / "__init__.py"

if not recipe.exists():
    print(f"❌ libffi recipe not found at {recipe}")
    sys.exit(1)

text = recipe.read_text(encoding="utf-8")
changed = False

if 'env["HAVE_HIDDEN"] = "0"' not in text:
    text = text.replace('"LDFLAGS="', '"LDFLAGS="\n        env["HAVE_HIDDEN"] = "0"')
    changed = True

if '"--disable-raw-api"' not in text and '"--enable-shared"' in text:
    text = text.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')
    changed = True

if changed:
    recipe.write_text(text, encoding="utf-8")
    print("✅ libffi recipe patched")
else:
    print("ℹ️ libffi recipe already patched (no-op)")
