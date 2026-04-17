#!/usr/bin/env python3
"""
Upload content to NotebookLM and generate outputs (PPT, Podcast, etc.)

Usage:
    python upload_and_generate.py --file <path> --name <notebook_name>
"""

import argparse
import sys
import time
import re
from pathlib import Path

from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory, StealthUtils
from config import PROXY_SERVER


def create_notebook_and_upload(file_path: str, notebook_name: str, headless: bool = False, proxy: str = None):
    """
    Create a new NotebookLM notebook, upload content, and generate outputs

    Args:
        file_path: Path to the file to upload
        notebook_name: Name for the new notebook
        headless: Run browser in headless mode (False for manual auth)
        proxy: Optional proxy server (e.g., "http://127.0.0.1:51561")
    """
    # Use proxy from env if not specified
    if not proxy and PROXY_SERVER:
        proxy = PROXY_SERVER

    auth = AuthManager()

    if not auth.is_authenticated():
        print("[!] Not authenticated. Please run setup first:")
        print("   python scripts/run.py auth_manager.py setup")
        return False

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
    page = None

    try:
        # Start playwright
        playwright = sync_playwright().start()

        # Launch persistent browser context
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=headless,
            proxy=proxy
        )

        page = context.new_page()
        stealth = StealthUtils()

        # Step 1: Navigate to NotebookLM home
        print("[INFO] Opening NotebookLM...")
        page.goto("https://notebooklm.google.com/", wait_until="networkidle", timeout=60000)

        # Wait for page load - longer delay for slow connections
        print(f"[INFO] Current URL after navigation: {page.url}")
        stealth.random_delay(5000, 8000)

        # Step 2: Create new notebook
        print("[INFO] Creating new notebook...")
        print(f"[DEBUG] Current URL: {page.url}")
        try:
            # Look for "New notebook" button - try multiple selectors
            create_selectors = [
                'button:has-text("New notebook")',
                'button:has-text("Create")',
                'button:has-text("New")',
                '[data-test-id="create-notebook-button"]',
                'div[role="button"]:has-text("New")',
                'span:has-text("New notebook")',
            ]

            create_button = None
            for selector in create_selectors:
                try:
                    print(f"[DEBUG] Trying selector: {selector}")
                    create_button = page.wait_for_selector(selector, timeout=10000, state="visible")
                    if create_button:
                        print(f"[OK] Found create button with selector: {selector}")
                        break
                except Exception as e:
                    print(f"[DEBUG] Selector {selector} failed: {e}")
                    continue

            if create_button:
                stealth.realistic_click(page, create_button)
                stealth.random_delay(2000, 3000)
                print(f"[DEBUG] URL after clicking create button: {page.url}")
            else:
                print("[WARN] Could not find create button, may already be on notebook creation page")

        except Exception as e:
            print(f"[WARN] Navigate to create: {e}")

        # Step 3: Set notebook name
        print(f"  ✏️  Setting notebook name: {notebook_name}")
        try:
            # Look for title input
            title_selectors = [
                'input[placeholder*="notebook" i]',
                'input[type="text"]',
                'textarea[placeholder*="notebook" i]',
            ]

            title_input = None
            for selector in title_selectors:
                try:
                    title_input = page.wait_for_selector(selector, timeout=3000, state="visible")
                    if title_input:
                        break
                except:
                    continue

            if title_input:
                title_input.click()
                title_input.fill("")  # Clear any existing text
                stealth.human_type(page, title_input, notebook_name)
                stealth.random_delay(500, 1000)
            else:
                print("  ⚠️ Could not find title input")

        except Exception as e:
            print(f"  ⚠️ Set title: {e}")

        # Step 4: Upload source file
        print(f"📤 Uploading source file...")
        try:
            # Look for source upload area
            upload_selectors = [
                'input[type="file"]',
                '[data-test-id="source-upload"]',
                'div[role="button"]:has-text("Add source")',
                'button:has-text("Add")',
            ]

            # Find file input
            file_input = None
            for selector in upload_selectors:
                try:
                    if selector == 'input[type="file"]':
                        file_input = page.wait_for_selector(selector, timeout=5000, state="attached")
                        if file_input:
                            break
                    else:
                        elem = page.wait_for_selector(selector, timeout=3000, state="visible")
                        if elem:
                            # Click to reveal file input
                            stealth.realistic_click(page, elem)
                            stealth.random_delay(500, 1000)
                            file_input = page.wait_for_selector('input[type="file"]', timeout=3000, state="attached")
                            if file_input:
                                break
                except:
                    continue

            if file_input:
                file_input.set_input_files(str(file_path))
                print("  ✅ File uploaded!")
                stealth.random_delay(2000, 4000)
            else:
                print("  ⚠️ Could not find file upload input")

        except Exception as e:
            print(f"  ⚠️ Upload failed: {e}")

        # Step 5: Wait for processing
        print("⏳ Waiting for source processing...")
        stealth.random_delay(5000, 8000)

        # Get current URL (notebook URL)
        notebook_url = page.url
        print(f"📚 Notebook URL: {notebook_url}")

        # Step 6: Generate PPT (Slide Deck)
        print("\n📊 Generating PPT (Slide Deck)...")
        try:
            # Look for generate button or area
            generate_selectors = [
                'button:has-text("Generate")',
                '[data-test-id="generate-button"]',
                'div[role="button"]:has-text("Generate")',
            ]

            # First, try to find a notebook overview/generation panel
            # The UI may have changed, so we'll try to navigate to it

            # Type in the query box to request slide deck generation
            query_selectors = [
                "textarea.query-box-input",
                'textarea[aria-label*="query" i]',
                'textarea[placeholder*="ask" i]',
                'div[contenteditable="true"]',
            ]

            query_input = None
            for selector in query_selectors:
                try:
                    query_input = page.wait_for_selector(selector, timeout=5000, state="visible")
                    if query_input:
                        print(f"  ✓ Found query input: {selector}")
                        break
                except:
                    continue

            if query_input:
                stealth.realistic_click(page, query_input)
                stealth.human_type(page, query_input, "Generate a slide deck presentation summarizing this content")
                stealth.random_delay(500, 1000)
                page.keyboard.press("Enter")
                print("  ✅ PPT generation requested!")
                stealth.random_delay(3000, 5000)
            else:
                print("  ⚠️ Could not find query input")

        except Exception as e:
            print(f"  ⚠️ PPT generation: {e}")

        # Step 7: Generate Podcast (Audio)
        print("\n🎙️  Generating Podcast (Audio)...")
        try:
            # Find query input again for second request
            query_selectors = [
                "textarea.query-box-input",
                'textarea[aria-label*="query" i]',
                'textarea[placeholder*="ask" i]',
                'div[contenteditable="true"]',
            ]

            query_input = None
            for selector in query_selectors:
                try:
                    query_input = page.wait_for_selector(selector, timeout=5000, state="visible")
                    if query_input:
                        break
                except:
                    continue

            if query_input:
                stealth.realistic_click(page, query_input)
                stealth.human_type(page, query_input, "Generate an audio overview podcast for this content")
                stealth.random_delay(500, 1000)
                page.keyboard.press("Enter")
                print("  ✅ Podcast generation requested!")
                stealth.random_delay(3000, 5000)
            else:
                print("  ⚠️ Could not find query input")

        except Exception as e:
            print(f"  ⚠️ Podcast generation: {e}")

        print("\n" + "="*50)
        print("✅ Tasks completed!")
        print("="*50)
        print(f"📚 Notebook: {notebook_url}")
        print("📊 Check the 'Notebook overview' section for PPT")
        print("🎙️  Check the 'Audio overview' section for Podcast")
        print("\n💡 Keep the browser open to let generation complete!")
        print("💡 You can close this script when done viewing.")
        print("="*50)

        # Keep browser open for user to see results
        if headless:
            print("\n[INFO] Keeping browser open for 30 seconds for review...")
            time.sleep(30)
        else:
            print("\n[INFO] Browser will stay open for manual interaction.")
            print("[INFO] Keeping browser open for 5 minutes...")
            print("[INFO] You can close the browser window manually when done.")
            time.sleep(300)  # Keep open for 5 minutes

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if playwright:
            # Only close playwright if headless, otherwise leave it open
            if headless:
                playwright.stop()


def main():
    parser = argparse.ArgumentParser(description="Upload content to NotebookLM and generate outputs")
    parser.add_argument("--file", required=True, help="Path to the file to upload")
    parser.add_argument("--name", required=True, help="Name for the notebook")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--proxy", help="Proxy server (e.g., http://127.0.0.1:51561)")

    args = parser.parse_args()

    create_notebook_and_upload(args.file, args.name, args.headless, args.proxy)


if __name__ == "__main__":
    main()
