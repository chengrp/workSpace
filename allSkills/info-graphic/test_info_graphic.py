#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Density Infographic Generation Test Script
"""
import os
import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup: ensure skills dir is in path BEFORE imports
current_dir = Path(__file__).parent.absolute()
skills_dir = current_dir.parent

# Add skills directory to sys.path so 'all_image' junction can be found
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

# Pre-load .env BEFORE importing all_image
env_path = skills_dir / "all-image" / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                if key not in os.environ:
                    os.environ[key] = value

# Now import - this works because 'all_image' junction points to 'all-image'
from all_image import ImageGenerator

def test_imports():
    """Test imports"""
    print("[*] Test 1/3: Verifying all-image skill import...")
    try:
        from all_image import ImageGenerator
        print("   [OK] all-image imported successfully")
        return True
    except ImportError as e:
        print(f"   [FAIL] Import failed: {e}")
        return False

def test_api_key():
    """Test API Key configuration"""
    print("\n[*] Test 2/3: Verifying Google AI API Key...")

    api_key = os.getenv("ALL_IMAGE_GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if api_key:
        masked = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        print(f"   [OK] API Key configured: {masked}")
        return True
    else:
        print("   [FAIL] API Key not configured")
        print("   Please set ALL_IMAGE_GOOGLE_API_KEY in all-image/.env")
        return False

def test_generation():
    """Test image generation"""
    print("\n[*] Test 3/3: Generating test infographic...")

    # Test prompt (simplified)
    test_prompt = """Create a high-density, professional information design infographic about "AI Writing Tools Comparison".

=== CRITICAL STYLE REQUIREMENTS ===

COLOR PALETTE - BLUEPRINT & POP LOGIC:
- BACKGROUND: Professional grayish-white (#F2F2F2)
- SYSTEMIC BASE: Muted Teal/Sage Green (#B8D8BE)
- HIGH-ALERT ACCENT: Vibrant Fluorescent Pink (#E91E63) for "Winner"
- MARKER HIGHLIGHTS: Vivid Lemon Yellow (#FFF200)
- LINE ART: Ultra-fine Charcoal Brown (#2D2926)

LAYOUT & INFORMATION DENSITY:
- INFORMATION AS COORDINATES: Every module has coordinate labels (e.g., A-01, B-05)
- HIGH DENSITY: 6-7 distinct modules per image
- VISUAL CONTRAST: Massive bold headers vs tiny technical annotations

MODULES - 6 TOTAL:
- MOD 1: BRAND ARRAY - 3x3 matrix, "Claude" highlighted in Pink as Winner
- MOD 2: SPECS SCALE - Quality ruler with "Standard" to "Premium" markers
- MOD 3: DEEP DIVE - Technical sketch showing features
- MOD 4: SCENARIO GRID - Comparison cards with hair-lines
- MOD 5: WARNING ZONE - Pink/Black area for pitfalls
- MOD 6: QUICK CHECK - Dense summary table

AVOID:
- NO cute/cartoonish doodles
- NO soft pastels or empty white space

Aspect Ratio: 3:4 (Portrait)"""

    print("   Generating image (may take 30-60 seconds)...")
    print("   Prompt:", test_prompt[:100] + "...")

    gen = ImageGenerator()

    try:
        result = gen.generate(
            prompt=test_prompt,
            ratio="3:4",
            quality="4k",
            mode="quality",
            auto_fallback=True
        )

        if result.success:
            print(f"\n   [OK] Image generated successfully!")
            print(f"   Path: {result.image_path}")
            print(f"   Provider: {result.provider}")
            print(f"   Time: {result.metadata.get('generation_time', 0)} seconds")

            # Check if file exists
            image_path = Path(result.image_path)
            if image_path.exists():
                file_size = image_path.stat().st_size / 1024  # KB
                print(f"   File size: {file_size:.1f} KB")

                # Convert to absolute path for display
                abs_path = image_path.resolve()
                print(f"   Absolute path: {abs_path}")
            else:
                print("   [WARN] File path doesn't exist, might be relative path issue")

            return True
        else:
            print(f"\n   [FAIL] Generation failed: {result.error}")
            if result.suggestions:
                print(f"   Suggestions: {result.suggestions}")
            if result.attempted_providers:
                print(f"   Attempted providers: {result.attempted_providers}")
            return False

    except Exception as e:
        print(f"\n   [ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test flow"""
    print("=" * 60)
    print("High-Density Infographic Generation - Skill Test")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Import test", test_imports()))
    results.append(("API Key test", test_api_key()))

    # Only run generation test if previous tests pass
    if all(r[1] for r in results):
        results.append(("Generation test", test_generation()))
    else:
        print("\n[WARN] Previous tests failed, skipping generation test")

    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{name}: {status}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n[SUCCESS] All tests passed! Skill is ready.")
    else:
        print("\n[WARN] Some tests failed, please check configuration.")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
