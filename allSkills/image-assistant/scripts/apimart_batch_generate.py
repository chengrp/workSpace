#!/usr/bin/env python3
"""
APIMart 批量图片生成脚本
支持异步任务提交和轮询
"""

import argparse
import json
import time
from pathlib import Path
from typing import Any
import urllib.request
import urllib.error


def load_config(path: Path) -> dict[str, str]:
    """加载配置文件"""
    config: dict[str, str] = {}
    if not path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            config[key.strip()] = value.strip()

    return config


def load_requests(input_path: Path) -> list[dict[str, Any]]:
    """加载批量请求文件（JSONL格式）"""
    if not input_path.exists():
        raise FileNotFoundError(f"请求文件不存在: {input_path}")

    requests_list = []
    for line_no, raw_line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"第 {line_no} 行 JSON 格式错误: {exc}")
        if not isinstance(obj, dict):
            raise ValueError(f"第 {line_no} 行应该是 JSON 对象")
        requests_list.append(obj)

    return requests_list


def submit_task(api_url: str, token: str, request: dict[str, Any]) -> dict[str, Any]:
    """提交生图任务"""
    payload = {
        "model": request.get("model", "gemini-3-pro-image-preview"),
        "prompt": request.get("prompt", ""),
        "size": request.get("size", "16:9"),
        "n": request.get("n", 1),
        "resolution": request.get("resolution", "2K"),
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url=api_url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=30.0) as resp:
        body = resp.read()

    return json.loads(body.decode("utf-8", errors="replace"))


def poll_task(task_url: str, token: str, max_wait: int = 300) -> dict[str, Any]:
    """轮询任务状态"""
    start_time = time.time()

    while True:
        if time.time() - start_time > max_wait:
            raise TimeoutError(f"任务轮询超时（{max_wait}秒）")

        req = urllib.request.Request(url=task_url, method="GET")
        req.add_header("Authorization", f"Bearer {token}")

        try:
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                body = resp.read()
            result = json.loads(body.decode("utf-8", errors="replace"))

            status = result.get("status", "unknown")
            if status == "completed":
                return result
            elif status == "failed":
                raise RuntimeError(f"任务失败: {result.get('error', '未知错误')}")

            # 等待后重试
            time.sleep(5)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                # 任务可能还在处理中
                time.sleep(5)
                continue
            raise


def download_image(url: str, output_path: Path) -> None:
    """下载图片"""
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=30.0) as resp:
        data = resp.read()
    output_path.write_bytes(data)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="APIMart 批量图片生成")
    parser.add_argument("--config", type=Path, default=Path("scripts/apimart.env"), help="配置文件路径")
    parser.add_argument("--input", type=Path, required=True, help="批量请求文件（JSONL格式）")
    parser.add_argument("--out", type=Path, default=None, help="输出目录")
    parser.add_argument("--max-wait", type=int, default=300, help="最大等待时间（秒）")

    args = parser.parse_args(argv)

    # 加载配置
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"错误：配置文件不存在: {args.config}")
        return 1

    api_url = config.get("API_URL", "https://api.apimart.ai/v1/images/generations")
    token = config.get("TOKEN", "").strip()

    if not token:
        print("错误：配置文件中缺少 TOKEN")
        return 1

    # 加载请求
    try:
        requests_list = load_requests(args.input)
    except Exception as e:
        print(f"错误：加载请求文件失败: {e}")
        return 1

    if not requests_list:
        print("错误：请求文件为空")
        return 1

    # 创建输出目录
    if args.out is None:
        out_dir = Path("outputs/apimart")
    else:
        out_dir = args.out

    out_dir.mkdir(parents=True, exist_ok=True)
    run_json_path = out_dir / "run.json"

    # 初始化运行记录
    run: dict[str, Any] = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "input": str(args.input),
        "output_dir": str(out_dir),
        "total_requests": len(requests_list),
        "items": [],
    }

    print(f"开始处理 {len(requests_list)} 个请求...")
    print(f"输出目录: {out_dir}\n")

    # 处理每个请求
    for idx, req in enumerate(requests_list, start=1):
        request_id = req.get("id", f"{idx:02d}")

        print(f"[{idx}/{len(requests_list)}] 处理请求: {request_id}")

        record: dict[str, Any] = {
            "id": request_id,
            "request": req,
        }

        try:
            # 提交任务
            print(f"  提交任务...")
            submit_response = submit_task(api_url, token, req)
            record["submit_response"] = submit_response

            # 获取任务 URL
            task_url = submit_response.get("task_url")
            if not task_url:
                print(f"  [X] 未返回 task_url")
                record["error"] = "未返回 task_url"
                run["items"].append(record)
                continue

            print(f"  任务已提交，开始轮询...")

            # 轮询任务状态
            result = poll_task(task_url, token, args.max_wait)
            record["result"] = result

            # 下载图片
            images = result.get("images", [])
            saved_images = []
            for img_idx, img_info in enumerate(images, start=1):
                img_url = img_info.get("url")
                if img_url:
                    filename = f"{request_id}-{img_idx}.png"
                    img_path = out_dir / filename
                    try:
                        download_image(img_url, img_path)
                        saved_images.append(filename)
                        print(f"  [OK] 已保存: {filename}")
                    except Exception as e:
                        print(f"  [X] 下载图片失败: {e}")

            if saved_images:
                record["saved_images"] = saved_images

            print()

        except Exception as e:
            record["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            print(f"  [X] 错误: {e}\n")

        run["items"].append(record)

        # 保存运行记录
        run_json_path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 完成
    run["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    run_json_path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("=" * 50)
    print(f"完成！输出目录: {out_dir}")
    print(f"运行记录: {run_json_path}")

    # 统计
    success_count = sum(1 for item in run["items"] if "saved_images" in item)
    error_count = sum(1 for item in run["items"] if "error" in item)
    print(f"\n统计: 成功 {success_count} 个, 失败 {error_count} 个")

    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
