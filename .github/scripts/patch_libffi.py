import os
import fileinput

def patch_libffi():
    print("Patching libffi if needed...")

    for root, dirs, files in os.walk("~/.buildozer"):
        for filename in files:
            if filename.endswith("configure.ac") or filename.endswith("configure.in"):
                filepath = os.path.expanduser(os.path.join(root, filename))
                print(f"Patching {filepath}")
                with fileinput.FileInput(filepath, inplace=True) as file:
                    for line in file:
                        # Example fix for certain libffi issues
                        print(line.replace("AM_CONFIG_HEADER", "AC_CONFIG_HEADERS"), end=")

if __name__ == "__main__":
    patch_libffi()
