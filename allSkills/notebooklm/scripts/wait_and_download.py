#!/usr/bin/env python3
"""
等待并下载 NotebookLM Artifacts
使用轮询和重试逻辑处理网络不稳定情况
"""

import sys
import time
import subprocess
import json
from pathlib import Path

os = __import__('os')
os.environ['PYTHONIOENCODING'] = 'utf-8'

def run_cmd(cmd, retries=3, timeout=60):
    """运行命令，带重试"""
    for attempt in range(retries):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            return result
        except subprocess.TimeoutExpired:
            if attempt < retries - 1:
                print(f"[RETRY] Timeout, retrying... ({attempt+1}/{retries})")
                time.sleep(5)
            else:
                raise
        except Exception as e:
            if attempt < retries - 1:
                print(f"[RETRY] Error: {e}, retrying... ({attempt+1}/{retries})")
                time.sleep(5)
            else:
                raise

def get_artifacts_json(notebook_id="db94"):
    """获取 artifacts JSON"""
    for _ in range(10):
        try:
            result = run_cmd([
                sys.executable, "-m", "notebooklm",
                "artifact", "list", "-n", notebook_id, "--json"
            ], timeout=30)

            if result.stdout:
                data = json.loads(result.stdout)
                if not data.get("error"):
                    return data

            print(f"[WAIT] No valid data yet, retrying in 10s...")
            time.sleep(10)
        except Exception as e:
            print(f"[WARN] Failed to get artifacts: {e}")
            time.sleep(10)
    return None

def wait_for_completion(notebook_id="db94", max_wait=600):
    """等待所有 artifacts 完成"""
    start = time.time()
    completed = {}

    while time.time() - start < max_wait:
        data = get_artifacts_json(notebook_id)
        if not data:
            continue

        artifacts = data.get("artifacts", [])
        print(f"[CHECK] Found {len(artifacts)} artifacts")

        all_done = True
        for art in artifacts:
            art_id = art.get("id", "")[:8]
            status = art.get("status", "")
            type_name = art.get("type_id", "unknown")

            if status == "completed":
                if art_id not in completed:
                    completed[art_id] = art
                    print(f"[OK] {type_name} {art_id} completed!")
            elif status in ["failed", "error"]:
                print(f"[FAIL] {type_name} {art_id} failed: {status}")
            else:
                all_done = False
                print(f"[PENDING] {type_name} {art_id}: {status}")

        if all_done and completed:
            print(f"[DONE] All {len(completed)} artifacts completed!")
            return list(completed.values())

        elapsed = int(time.time() - start)
        print(f"[WAIT] Still processing... ({elapsed}s elapsed)")
        time.sleep(15)

    print("[TIMEOUT] Not all artifacts completed")
    return list(completed.values()) if completed else None

def download_artifact(art_id, type_name, output_dir):
    """下载单个 artifact"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if type_name == "slide_deck":
        ext = "pdf"
    elif type_name == "audio":
        ext = "mp3"
    else:
        ext = "bin"

    output_path = output_dir / f"{art_id[:8]}_{type_name}.{ext}"

    for attempt in range(5):
        try:
            print(f"[DOWNLOAD] Attempting {type_name} ({attempt+1}/5)...")

            result = run_cmd([
                sys.executable, "-m", "notebooklm",
                "download", type_name,
                str(output_path), "-n", "db94"
            ], timeout=60)

            if result.returncode == 0 and output_path.exists():
                size = output_path.stat().st_size
                print(f"[OK] Downloaded: {output_path} ({size} bytes)")
                return output_path
            else:
                print(f"[WARN] Download failed: {result.stderr}")

        except Exception as e:
            print(f"[WARN] Download error: {e}")

        print(f"[WAIT] Retrying in 10s...")
        time.sleep(10)

    return None

def main():
    notebook_id = "db94"
    output_dir = "C:/Users/RyanCh/CC_record/skills/demos"

    print("="*60)
    print("NotebookLM Artifact 下载器")
    print("="*60)

    # 等待完成
    print(f"\n[STEP 1] Waiting for artifacts to complete...")
    completed = wait_for_completion(notebook_id, max_wait=600)

    if not completed:
        print("[ERROR] No artifacts completed successfully")
        return

    # 下载
    print(f"\n[STEP 2] Downloading completed artifacts...")
    downloaded = []

    for art in completed:
        art_id = art.get("id")
        type_name = art.get("type_id")

        path = download_artifact(art_id, type_name, output_dir)
        if path:
            downloaded.append(path)

    # 总结
    print("\n" + "="*60)
    print("下载完成!")
    print("="*60)
    print(f"成功下载: {len(downloaded)} 个文件")
    for path in downloaded:
        print(f"  - {path}")
    print("="*60)

if __name__ == "__main__":
    main()
