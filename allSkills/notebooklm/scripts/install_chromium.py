#!/usr/bin/env python3
"""Install Chromium for NotebookLM skill"""
from patchright.sync_api import sync_playwright

print('Checking Patchright and Chromium...')
playwright = sync_playwright().start()

try:
    browser_type = playwright.chromium
    print(f'Chromium executable: {browser_type.executable_path}')

    print('Ensuring Chromium is installed...')
    browser_type.install()
    print('[OK] Chromium ready!')

except Exception as e:
    print(f'[X] Error: {e}')
finally:
    playwright.stop()
