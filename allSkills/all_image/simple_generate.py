#!/usr/bin/env python3
"""
Simple CLI wrapper for all-image generation.
Support batch processing from JSON/JSONL files.
"""
import sys
import os
import json
import argparse
import logging
from typing import List, Dict

# === Setup: ensure skills dir is in path and .env is loaded BEFORE imports ===
current_dir = os.path.dirname(os.path.abspath(__file__))
skills_dir = os.path.dirname(current_dir)

# Add skills directory to sys.path so 'all_image' junction can be found
if skills_dir not in sys.path:
    sys.path.insert(0, skills_dir)

# Pre-load .env BEFORE importing all_image (so proxy/API keys are available during init)
env_path = os.path.join(current_dir, '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key, value = key.strip(), value.strip()
                if key not in os.environ:
                    os.environ[key] = value

# Now import - this works because 'all_image' junction points to 'all-image'
from all_image import ImageGenerator
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_prompts(file_path: str) -> List[Dict]:
    """Load prompts from JSON or JSONL file"""
    prompts = []
    try:
        if file_path.endswith('.jsonl'):
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        prompts.append(json.loads(line))
        else:
            # Assume JSON array
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read().strip()
                if content:
                    prompts = json.loads(content)
                    if not isinstance(prompts, list):
                        prompts = [prompts]
    except Exception as e:
        logger.error(f"Failed to load prompts from {file_path}: {e}")
        return []
    return prompts

def main():
    parser = argparse.ArgumentParser(description="Generate images using all-image")
    parser.add_argument("--prompt", type=str, help="Single prompt to generate")
    parser.add_argument("--batch", type=str, help="Path to JSON/JSONL file with prompts")
    parser.add_argument("--output", type=str, default=".", help="Output directory")
    args = parser.parse_args()

    # Initialize Generator (auto-loads environment from package init)
    generator = ImageGenerator(auto_fallback=True)

    requests = []

    # Handle Single Prompt
    if args.prompt:
        requests.append({"prompt": args.prompt})

    # Handle Batch File
    if args.batch:
        batch_prompts = load_prompts(args.batch)
        if batch_prompts:
            requests.extend(batch_prompts)
            logger.info(f"Loaded {len(batch_prompts)} prompts from {args.batch}")

    if not requests:
        logger.warning("No prompts provided. Use --prompt or --batch.")
        return

    # Process Requests
    logger.info(f"Starting generation for {len(requests)} items...")
    
    # Use batch generation for efficiency
    results = generator.generate_batch(requests, max_concurrent=2)
    
    success_count = 0
    for i, result in enumerate(results):
        prompt_preview = requests[i].get('prompt', '')[:50]
        if result.success:
            success_count += 1
            logger.info(f"✅ [{i+1}/{len(results)}] Success: {result.image_path}")
        else:
            logger.error(f"❌ [{i+1}/{len(results)}] Failed ({prompt_preview}...): {result.error}")

    logger.info(f"Completed. Success: {success_count}/{len(requests)}")

if __name__ == "__main__":
    main()