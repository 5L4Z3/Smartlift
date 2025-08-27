#!/bin/bash
set -e

echo "Patching libffi for Buildozer..."

# Ensure correct libffi symlink for python-for-android
if [ -d "/usr/lib/x86_64-linux-gnu" ]; then
    sudo ln -sf /usr/lib/x86_64-linux-gnu/libffi.so.8 /usr/lib/x86_64-linux-gnu/libffi.so || true
fi
