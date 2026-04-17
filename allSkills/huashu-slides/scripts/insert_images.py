#!/usr/bin/env python3
"""
Insert AI illustration images into HTML slides.
Replaces image placeholder divs with actual img tags.
"""

import re
from pathlib import Path


def insert_images_to_html(slides_dir: Path):
    """
    Replace image placeholder divs with img tags in HTML files.
    """
    slides_dir = Path(slides_dir)
    html_files = sorted(slides_dir.glob("slide-*.html"))

    updated_count = 0

    for html_file in html_files:
        # Extract slide number to find matching illustration
        match = re.search(r'slide-(\d+)\.html', html_file.name)
        if not match:
            continue

        slide_num = match.group(1)
        illustration_file = slides_dir / f"slide-{slide_num}-illustration.png"

        if not illustration_file.exists():
            print(f"[!] No illustration found for {html_file.name}")
            continue

        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has img tag
        if f'<img src="slide-{slide_num}-illustration.png"' in content:
            print(f"[+] {html_file.name} already has image")
            continue

        # Replace image placeholder div with img tag
        # Match the image-placeholder div pattern
        placeholder_pattern = r'<div class="image-placeholder">.*?</div>'

        # Create replacement img tag with same container styling
        img_tag = f'''<div class="image-container">
                  <img src="slide-{slide_num}-illustration.png" alt="AI Illustration" style="width:100%;height:auto;object-fit:contain;">
                </div>'''

        new_content = re.sub(placeholder_pattern, img_tag, content, flags=re.DOTALL)

        if new_content != content:
            # Write updated content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] Updated {html_file.name}")
            updated_count += 1
        else:
            print(f"[!] No placeholder found in {html_file.name}")

    return updated_count


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        slides_dir = Path(sys.argv[1])
    else:
        slides_dir = Path(__file__).parent.parent / "output" / "slides"

    print(f"Processing slides in: {slides_dir}")
    print("-" * 40)

    count = insert_images_to_html(slides_dir)

    print("-" * 40)
    print(f"[OK] Updated {count} HTML files with images")
    print(f"\nNext: Run 'node scripts/build_ppt.js' to rebuild PPTX")
