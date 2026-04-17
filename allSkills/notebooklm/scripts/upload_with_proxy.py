#!/usr/bin/env python3
"""
Upload content to NotebookLM with proxy support

Usage:
    python upload_with_proxy.py --file <path> --name <notebook_name> [--proxy <proxy_url>]

Example:
    python upload_with_proxy.py --file article.txt --name "My Notebook" --proxy "http://127.0.0.1:7890"
"""

import argparse
import sys
import time
import os
from pathlib import Path

from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory, StealthUtils


def create_notebook_and_upload(file_path: str, notebook_name: str, proxy: str = None):
    """
    Create a new NotebookLM notebook, upload content, and generate outputs

    Args:
        file_path: Path to the file to upload
        notebook_name: Name for the new notebook
        proxy: Optional proxy URL (e.g., "http://127.0.0.1:7890")
    """
    auth = AuthManager()

    file_path = Path(file_path).resolve()
    if not file_path.exists():
        print(f"[X] File not found: {file_path}")
        return False

    print(f"[INFO] File: {file_path}")
    print(f"[INFO] Notebook: {notebook_name}")
    if proxy:
        print(f"[INFO] Proxy: {proxy}")

    playwright = None
    context = None

    try:
        # Start playwright
        playwright = sync_playwright().start()

        # Prepare browser context arguments
        context_args = {
            "headless": False,  # Show browser for manual login
            "args": [
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        }

        # Add proxy if specified
        if proxy:
            context_args["proxy"] = {"server": proxy}

        # Get browser state directory
        from config import BROWSER_STATE_DIR
        context_args["user_data_dir"] = str(BROWSER_STATE_DIR)

        # Launch browser
        print("[INFO] Launching browser...")
        context = playwright.chromium.launch_persistent_context(**context_args)

        # Set default timeout
        context.set_default_timeout(60000)

        page = context.new_page()
        stealth = StealthUtils()

        # Navigate to NotebookLM
        print("[INFO] Opening NotebookLM...")
        page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded", timeout=60000)

        # Check if we need to login
        current_url = page.url
        if "accounts.google.com" in current_url:
            print("\n" + "="*60)
            print("[AUTH REQUIRED] Please login to Google in the browser window")
            print("="*60)
            print("Waiting for login to complete...")

            # Wait for navigation away from login page
            try:
                page.wait_for_url(
                    lambda url: "accounts.google.com" not in url,
                    timeout=300000  # 5 minutes
                )
                print("[OK] Login successful!")
            except Exception as e:
                print(f"[X] Login timeout or failed: {e}")
                return False

        # Wait for page load
        stealth.random_delay(2000, 3000)

        # Get the current page URL
        notebook_url = page.url
        print(f"[INFO] Current URL: {notebook_url}")

        # Look for source upload button
        print("\n[INFO] Looking for source upload option...")

        # Try multiple selectors for adding sources
        upload_selectors = [
            'button:has-text("Add sources")',
            'button:has-text("Add source")',
            'button:has-text("添加来源")',
            'div[role="button"]:has-text("Add")',
            '[data-test-id="add-source-button"]',
        ]

        upload_button = None
        for selector in upload_selectors:
            try:
                upload_button = page.wait_for_selector(selector, timeout=5000, state="visible")
                if upload_button:
                    print(f"[OK] Found upload button: {selector}")
                    break
            except:
                continue

        if upload_button:
            stealth.realistic_click(page, upload_button)
            stealth.random_delay(1000, 2000)
        else:
            print("[WARN] Could not find upload button, may be on correct page already")

        # Look for file input or Google Drive option
        print("[INFO] Looking for file upload option...")

        # Try to find the file upload area
        file_input_selectors = [
            'input[type="file"]',
            'button:has-text("Upload from computer")',
            'button:has-text("从计算机上传")',
        ]

        file_input = None
        for selector in file_input_selectors:
            try:
                if 'input[type="file"]' in selector:
                    file_input = page.wait_for_selector(selector, timeout=5000, state="attached")
                    if file_input:
                        print(f"[OK] Found file input")
                        break
                else:
                    elem = page.wait_for_selector(selector, timeout=3000, state="visible")
                    if elem:
                        stealth.realistic_click(page, elem)
                        stealth.random_delay(500, 1000)
                        file_input = page.wait_for_selector('input[type="file"]', timeout=3000, state="attached")
                        if file_input:
                            print(f"[OK] Found file input after clicking: {selector}")
                            break
            except:
                continue

        if file_input:
            print(f"[INFO] Uploading file: {file_path.name}")
            file_input.set_input_files(str(file_path))
            print("[OK] File uploaded!")
            stealth.random_delay(3000, 5000)
        else:
            print("[WARN] Could not find file upload option")
            print("[HINT] You may need to manually upload the file in the browser")

        # Get final notebook URL
        notebook_url = page.url

        print("\n" + "="*60)
        print("[OK] Upload process completed!")
        print("="*60)
        print(f"Notebook URL: {notebook_url}")
        print("\nNext steps in NotebookLM:")
        print("1. Wait for the source to be processed")
        print("2. In 'Notebook overview' section, click to generate PPT/Slide deck")
        print("3. In 'Audio overview' section, click to generate Podcast")
        print("="*60)
        print("\n[Browser will stay open for you to complete the steps]")
        print("[Press Ctrl+C to close]")

        # Keep browser open
        try:
            input()  # Wait for user
        except KeyboardInterrupt:
            pass

        return True

    except Exception as e:
        print(f"[X] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if playwright:
            playwright.stop()


def main():
    parser = argparse.ArgumentParser(description="Upload content to NotebookLM")
    parser.add_argument("--file", required=True, help="Path to the file to upload")
    parser.add_argument("--name", required=True, help="Name for the notebook")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://127.0.0.1:7890)")

    args = parser.parse_args()

    # Check for common proxy ports if no proxy specified
    proxy = args.proxy
    if not proxy:
        print("[INFO] No proxy specified. Trying without proxy...")
        print("[HINT] If connection fails, use --proxy parameter")
        print("[HINT] Common proxy ports: 7890, 10809, 8080")
        print()

    create_notebook_and_upload(args.file, args.name, proxy)


if __name__ == "__main__":
    main()
