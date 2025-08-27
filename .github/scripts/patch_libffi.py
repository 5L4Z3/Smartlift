import os

libffi_path = "./.buildozer/android/platform/build/other_builds/libffi"
if os.path.exists(libffi_path):
    for root, dirs, files in os.walk(libffi_path):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                lines = f.readlines()
            with open(filepath, "w") as f:
                for line in lines:
                    f.write(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))
else:
    print("libffi directory not found, skipping patch.")
