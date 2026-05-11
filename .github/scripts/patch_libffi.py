#!/usr/bin/env python3
"""Idempotent patch for python-for-android libffi recipe to fix CI build failures."""
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("libffi-patcher")

def find_recipe():
    try:
        import pythonforandroid
        base = Path(pythonforandroid.__file__).parent
        return base / "recipes" / "libffi" / "__init__.py"
    except Exception as e:
        logger.debug(f"p4a not installed yet: {e}")
        return None

def patch(recipe: Path):
    if not recipe.exists():
        logger.error("Recipe not found.")
        return False

    text = recipe.read_text(encoding="utf-8")
    if "env['HAVE_HIDDEN'] = '0'" in text:
        logger.info("Already patched. Skipping.")
        return True

    # Safe insertion point
    marker = 'env["LDFLAGS"]'
    if marker in text:
        text = text.replace(marker, f'{marker}\n        env["HAVE_HIDDEN"] = "0"')
    else:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if "def build_arch(" in line:
                lines.insert(i + 1, '        env["HAVE_HIDDEN"] = "0"')
                break
        text = "\n".join(lines)

    recipe.write_text(text, encoding="utf-8")
    logger.info("Patched successfully.")
    return True

if __name__ == "__main__":
    r = find_recipe()
    if r:
        patch(r)
    else:
        logger.info("Skipping patch (p4a not available yet).")
