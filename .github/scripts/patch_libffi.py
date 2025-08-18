#!/usr/bin/env python3
import os, time, sys
from pathlib import Path

def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False

    # Insert env["HAVE_HIDDEN"] = "0" after line containing "LDFLAGS="
    if 'env["HAVE_HIDDEN"] = "0"' not in text and 'LDFLAGS=' in text:
        new_text = []
        for line in text.splitlines(True):
            new_text.append(line)
            if 'LDFLAGS=' in line and 'HAVE_HIDDEN' not in line:
                new_text.append('        env["HAVE_HIDDEN"] = "0"\n')
                changed = True
        text = "".join(new_text)

    # Ensure --disable-raw-api alongside --enable-shared
    if '"--enable-shared"' in text and '"--disable-raw-api"' not in text:
        text = text.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
    return changed

def find_candidates():
    candidates = []
    try:
        import pythonforandroid as p4a
        p = Path(p4a.__file__).parent / "recipes" / "libffi" / "__init__.py"
        candidates.append(p)
    except Exception:
        pass
    home = Path.home()
    p2 = home / ".local" / "share" / "python-for-android" / "recipes" / "libffi" / "__init__.py"
    candidates.append(p2)
    return candidates

def main():
    deadline = time.time() + 600
    candidates = find_candidates()
    while time.time() < deadline:
        for cand in candidates:
            if cand.exists():
                changed = patch_file(cand)
                print(("✅ Patched" if changed else "ℹ️ Already patched"), cand)
                return 0
        time.sleep(5)
    print("❌ libffi recipe not found to patch within timeout.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
