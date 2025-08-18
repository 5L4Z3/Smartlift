#!/usr/bin/env python3
"""
Deterministically patch the libffi recipe in the installed python-for-android package.
Safe and idempotent. Not used by CI (the CI inlines this logic before build),
but handy for local builds if needed.
"""

import os
import sys
from pathlib import Path

try:
    import pythonforandroid as p4a
except Exception as e:
    print(f"❌ Could not import pythonforandroid: {e}")
    sys.exit(1)

p4a_dir = Path(p4a.__file__).parent
recipe = p4a_dir / "recipes" / "libffi" / "__init__.py"

if not recipe.exists():
    print(f"❌ libffi recipe not found at {recipe}")
    sys.exit(1)

text = recipe.read_text()

changed = False
if 'env["HAVE_HIDDEN"] = "0"' not in text:
    text = text.replace('"LDFLAGS="', '"LDFLAGS="\n        env["HAVE_HIDDEN"] = "0"')
    changed = True

if '"--disable-raw-api"' not in text and '"--enable-shared"' in text:
    text = text.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')
    changed = True

if changed:
    recipe.write_text(text)
    print(f"✅ Patched {recipe}")
else:
    print("ℹ️ Already patched; no changes made.")
