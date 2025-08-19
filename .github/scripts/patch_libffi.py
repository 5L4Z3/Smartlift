import os

# Path to libffi configure file inside buildozer/.buildozer
libffi_dir = os.path.expanduser("~/.buildozer/android/platform/build-arm64-v8a/build/other_builds/libffi/armeabi-v7a/libffi")
configure_ac = os.path.join(libffi_dir, "configure.ac")

if os.path.exists(configure_ac):
    with open(configure_ac, "r") as f:
        lines = f.readlines()

    with open(configure_ac, "w") as f:
        for line in lines:
            if "AM_CONFIG_HEADER" in line:
                f.write(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"))
            else:
                f.write(line)

    print("✅ Successfully patched libffi configure.ac")
else:
    print("⚠️ configure.ac not found at:", configure_ac)
