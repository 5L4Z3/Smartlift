import os

def patch_libffi():
    libffi_dir = os.path.expanduser("~/.buildozer/android/platform/build-arm64-v8a/build/other_builds/libffi")
    if not os.path.exists(libffi_dir):
        print("libffi directory not found, skipping patch.")
        return

    for root, dirs, files in os.walk(libffi_dir):
        for file in files:
            if file.endswith("Makefile"):
                makefile_path = os.path.join(root, file)
                with open(makefile_path, "r") as f:
                    content = f.read()
                patched = content.replace("-Werror", "")
                if patched != content:
                    with open(makefile_path, "w") as f:
                        f.write(patched)
                    print(f"Patched {makefile_path}")

if __name__ == "__main__":
    patch_libffi()
