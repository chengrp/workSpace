#!/usr/bin/env python3
"""Install browsers for patchright"""
import subprocess
import sys

print("Installing Chromium for patchright...")
result = subprocess.run([sys.executable, "-m", "patchright", "install", "chromium"])
if result.returncode == 0:
    print("[OK] Chromium installed successfully!")
else:
    print(f"[X] Installation failed with code {result.returncode}")
    sys.exit(1)
