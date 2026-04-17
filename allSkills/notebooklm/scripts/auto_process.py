#!/usr/bin/env python3
"""
自动处理流程：上传内容到 NotebookLM 并生成 PPT 和播客
"""

import sys
import time
import subprocess
import json
from pathlib import Path

# 设置编码
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_command(cmd, check=True):
    """运行命令并返回输出"""
    print(f"[CMD] {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
        encoding='utf-8',
        errors='replace'
    )
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed: {result.stderr}")
    return result

def wait_for_artifact_completion(notebook_id, timeout=600):
    """等待所有 artifact 完成"""
    print(f"[WAIT] Waiting for artifacts to complete (timeout={timeout}s)...")

    start_time = time.time()
    check_interval = 10  # 每 10 秒检查一次

    while time.time() - start_time < timeout:
        try:
            # 列出 artifacts
            result = run_command([
                sys.executable, "-m", "notebooklm",
                "-vv", "artifact", "list",
                "-n", notebook_id[:4]
            ], check=False)

            output = result.stdout + result.stderr

            # 检查是否有 "completed" 状态
            if "completed" in output.lower() or "success" in output.lower():
                print("[OK] Artifacts completed!")
                return True

            # 检查是否有失败
            if "failed" in output.lower():
                print("[WARN] Some artifacts may have failed")
                return False

            print(f"[CHECK] Still processing... ({int(time.time() - start_time)}s elapsed)")
            time.sleep(check_interval)

        except Exception as e:
            print(f"[WARN] Check failed: {e}, retrying...")
            time.sleep(check_interval)

    print("[TIMEOUT] Artifacts not completed within timeout")
    return False

def download_artifacts(notebook_id, output_dir):
    """下载所有生成的 artifacts"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 尝试下载 PPT
    print("[DOWNLOAD] Attempting to download slide-deck...")
    ppt_path = output_dir / "slides.pdf"
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "-vv", "download", "slide-deck",
        str(ppt_path), "-n", notebook_id[:4]
    ], check=False)

    if result.returncode == 0 and "Saved to" in result.stdout:
        print(f"[OK] PPT downloaded: {ppt_path}")
    else:
        print("[WARN] PPT download failed or not ready")

    # 尝试下载播客
    print("[DOWNLOAD] Attempting to download audio...")
    audio_path = output_dir / "podcast.mp3"
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "-vv", "download", "audio",
        str(audio_path), "-n", notebook_id[:4]
    ], check=False)

    if result.returncode == 0 and "Saved to" in result.stdout:
        print(f"[OK] Audio downloaded: {audio_path}")
    else:
        print("[WARN] Audio download failed or not ready")

    return ppt_path, audio_path

def main():
    # 配置
    weixin_file = "C:/Users/RyanCh/AppData/Local/Temp/weixin_为什么人人都应Skill_20260327.txt"
    notebook_name = "为什么人人都应Skill"
    output_dir = "C:/Users/RyanCh/CC_record/skills/demos"

    print("="*60)
    print("NotebookLM 自动处理流程")
    print("="*60)

    # Step 1: 创建 notebook（如果需要）
    print("\n[STEP 1] Creating notebook...")
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "create", notebook_name
    ], check=False)

    if result.returncode == 0:
        # 提取 notebook ID
        for line in result.stdout.split('\n'):
            if 'Created notebook:' in line:
                notebook_id = line.split(':')[-1].strip().split()[0]
                print(f"[OK] Notebook created: {notebook_id}")
                break
        else:
            # 尝试从现有列表获取
            result = run_command([
                sys.executable, "-m", "notebooklm", "list"
            ], check=False)
            print("[INFO] Using existing notebook")
    else:
        print("[INFO] Notebook may already exist, listing...")
        result = run_command([
            sys.executable, "-m", "notebooklm", "list"
        ], check=False)

    # 使用 notebook（取前4位）
    notebook_id = "db94"  # 从之前创建的
    run_command([
        sys.executable, "-m", "notebooklm", "use", notebook_id
    ], check=False)

    # Step 2: 上传文件
    print(f"\n[STEP 2] Uploading file: {weixin_file}")
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "source", "add", weixin_file,
        "--title", notebook_name
    ], check=False)

    if result.returncode == 0:
        print("[OK] File uploaded successfully")
        print("[WAIT] Waiting for source processing...")
        time.sleep(10)  # 等待源处理
    else:
        print("[WARN] File upload may have failed, continuing...")

    # Step 3: 生成 PPT
    print(f"\n[STEP 3] Generating slide-deck...")
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "generate", "slide-deck",
        f"{notebook_name} Presentation"
    ], check=False)

    if result.returncode == 0:
        print("[OK] Slide-deck generation started")
    else:
        print("[WARN] Slide-deck generation failed")

    # Step 4: 生成播客
    print(f"\n[STEP 4] Generating audio...")
    result = run_command([
        sys.executable, "-m", "notebooklm",
        "generate", "audio",
        f"{notebook_name} Podcast"
    ], check=False)

    if result.returncode == 0:
        print("[OK] Audio generation started")
    else:
        print("[WARN] Audio generation failed")

    # Step 5: 等待生成完成
    print(f"\n[STEP 5] Waiting for artifacts to complete...")
    wait_for_artifact_completion(notebook_id, timeout=300)

    # Step 6: 下载文件
    print(f"\n[STEP 6] Downloading artifacts...")
    ppt_path, audio_path = download_artifacts(notebook_id, output_dir)

    # 总结
    print("\n" + "="*60)
    print("处理完成!")
    print("="*60)
    print(f"Notebook ID: {notebook_id}")
    print(f"Output Directory: {output_dir}")
    print("\n生成的文件:")
    print(f"  - PPT: {ppt_path}")
    print(f"  - Audio: {audio_path}")
    print("\n如果文件未下载成功，请稍后手动使用以下命令下载:")
    print(f"  notebooklm use {notebook_id}")
    print(f"  notebooklm download slide-deck <path>")
    print(f"  notebooklm download audio <path>")
    print("="*60)

if __name__ == "__main__":
    main()
