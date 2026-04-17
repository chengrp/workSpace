#!/usr/bin/env python3
"""
NotebookLM Artifact 下载脚本
稍后运行此脚本来下载已完成生成的文件

使用方法:
    python scripts/download_ready.py

Notebook ID: db948d6a-7df4-48fa-ba84-114c65bb84a1 (前4位: db94)
"""

import sys
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import subprocess
from pathlib import Path

NOTEBOOK_ID = "db94"
OUTPUT_DIR = "C:/Users/RyanCh/CC_record/skills/demos"

def download_artifact(type_name, filename):
    """下载 artifact"""
    output_path = Path(OUTPUT_DIR) / filename

    print(f"\n[DOWNLOAD] {type_name} -> {output_path}")

    cmd = [
        sys.executable, "-m", "notebooklm",
        "download", type_name,
        str(output_path), "-n", NOTEBOOK_ID
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and "Saved to" in result.stdout:
        print(f"[OK] 下载成功: {output_path}")
        return True
    else:
        print(f"[INFO] {result.stderr or result.stdout}")
        return False

def main():
    print("="*60)
    print("NotebookLM Artifact 下载器")
    print("="*60)
    print(f"Notebook ID: {NOTEBOOK_ID}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("\n正在下载...")

    success = []

    # 下载 PPT
    if download_artifact("slide-deck", "skill_evolution_slides.pdf"):
        success.append("PPT")

    # 下载播客
    if download_artifact("audio", "skill_evolution_podcast.mp3"):
        success.append("播客")

    print("\n" + "="*60)
    if success:
        print(f"下载完成: {', '.join(success)}")
    else:
        print("文件可能还在生成中，请稍后重试")
        print("\n手动下载命令:")
        print(f"  notebooklm use {NOTEBOOK_ID}")
        print(f"  notebooklm download slide-deck <path>")
        print(f"  notebooklm download audio <path>")
    print("="*60)

if __name__ == "__main__":
    main()
