#!/usr/bin/env python3
"""
Patch libffi recipe inside pythonforandroid installation to avoid
autoreconf errors (LT_SYS_SYMBOL_USCORE) on hosted runners.

This script modifies the installed pythonforandroid package files
immediately after pip installing python-for-android (develop).
"""
import sys
from pathlib import Path
import shutil

def find_p4a_recipe():
    try:
        import pythonforandroid
    except Exception as e:
        print("pythonforandroid not importable yet:", e)
        return None
    p4a_dir = Path(pythonforandroid.__file__).resolve().parent
    recipe = p4a_dir / "recipes" / "libffi" / "__init__.py"
    return recipe if recipe.exists() else None

def patch_recipe(path: Path):
    backup = path.with_suffix(".py.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"Backup created: {backup}")

    text = path.read_text(encoding="utf-8")

    # Defensive: if we've patched already, don't do it again
    if 'HAVE_HIDDEN' in text or '--disable-raw-api' in text:
        print("Recipe appears already patched; skipping.")
        return

    # Insert HAVE_HIDDEN env assignment after any LDFLAGS string usage
    new_text = text.replace(
        '"LDFLAGS="',
        '"LDFLAGS="'
    )

    # Strategy: try to add env["HAVE_HIDDEN"]="0" into build args if present
    # This is conservative: we search for a common marker and insert nearby.
    marker = 'env["LDFLAGS"]'
    if marker in new_text:
        new_text = new_text.replace(marker, marker + '\n        env["HAVE_HIDDEN"] = "0"')
        print("Inserted HAVE_HIDDEN near LDFLAGS token.")
    else:
        # fallback: append an env assignment near top (safe minimal change)
        lines = new_text.splitlines()
        for i, ln in enumerate(lines):
            if ln.strip().startswith("def build_arch("):
                insert_at = i + 1
                break
        else:
            insert_at = 1
        lines.insert(insert_at, '        env["HAVE_HIDDEN"] = "0"')
        new_text = "\n".join(lines)
        print("Inserted HAVE_HIDDEN at top of build_arch fallback location.")

    # Replace --enable-shared with a safer variant if present
    new_text = new_text.replace('"--enable-shared"', '"--enable-shared", "--disable-raw-api"')

    path.write_text(new_text, encoding="utf-8")
    print(f"Patched libffi recipe at: {path}")

def main():
    recipe = find_p4a_recipe()
    if not recipe:
        print("libffi recipe not found in python-for-android installation; skipping patch.")
        sys.exit(0)
    try:
        patch_recipe(recipe)
    except Exception as e:
        print("Failed to patch recipe:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
