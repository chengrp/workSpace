"""
ModelScope AI图片生成器
使用通义千问Turbo模型免费生成AI图片
每天免费额度：2000张

支持功能:
- 文生图 (Text-to-Image)
- 图生图 (Image-to-Image) - 根据参考图生成同风格图片
"""

import sys
import io
import requests
import time
import json
import base64
from PIL import Image
from io import BytesIO
from typing import Optional, Dict, Any
import argparse

# 设置stdout为utf-8编码，解决Windows控制台编码问题
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass


class ModelScopeImageGenerator:
    """ModelScope图片生成器类"""

    def __init__(self, api_key: str = None):
        """
        初始化图片生成器

        Args:
            api_key: ModelScope API Key，默认使用内置key
        """
        # 默认API Key
        self.api_key = api_key or "ms-51dd7494-0706-45d9-a901-c395522c55f2"
        self.base_url = 'https://api-inference.modelscope.cn/'
        self.common_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = "Tongyi-MAI/Z-Image-Turbo",
        size: Optional[str] = None,
        reference_image: Optional[str] = None,
        loras: Optional[Dict[str, float] | str] = None,
        output_path: str = "image/result_image.jpg",
        check_interval: int = 5,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        生成AI图片

        Args:
            prompt: 图片描述提示词（建议使用英文）
            model: 使用的模型，默认为Turbo模型
            size: 图片尺寸，格式为"宽x高"，如"1024x1792"(9:16)、"1792x1024"(16:9)、"1536x1536"(1:1)
            reference_image: 参考图片路径（图生图功能，生成同风格图片）
            loras: 可选的LoRA配置
            output_path: 输出图片路径
            check_interval: 状态检查间隔（秒）
            verbose: 是否显示详细输出

        Returns:
            包含生成结果的字典
        """
        try:
            # 步骤1：提交异步任务
            if verbose:
                print(f"📤 正在提交图片生成任务...")
                print(f"   Prompt: {prompt}")
                print(f"   Model: {model}")
                if size:
                    print(f"   Size: {size}")
                if reference_image:
                    print(f"   参考图: {reference_image} (图生图模式)")

            task_id = self._submit_task(prompt, model, size, reference_image, loras)

            if verbose:
                print(f"✅ 任务已提交，Task ID: {task_id}")
                print(f"⏳ 正在等待生成完成...")

            # 步骤2：轮询任务状态
            result = self._poll_task_status(task_id, check_interval, verbose)

            # 步骤3：下载并保存图片
            if result["task_status"] == "SUCCEED":
                image_url = result["output_images"][0]
                self._download_and_save_image(image_url, output_path)

                if verbose:
                    print(f"✅ 图片已成功生成并保存到: {output_path}")

                return {
                    "success": True,
                    "output_path": output_path,
                    "image_url": image_url,
                    "task_id": task_id
                }
            else:
                if verbose:
                    print(f"❌ 图片生成失败: {result.get('error_message', '未知错误')}")

                return {
                    "success": False,
                    "error": result.get('error_message', '未知错误'),
                    "task_id": task_id
                }

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP错误: {e.response.status_code}"
            if e.response.status_code == 401:
                error_msg += " (API Key无效或已过期)"
            elif e.response.status_code == 429:
                error_msg += " (额度超限，请等待明日重置)"

            if verbose:
                print(f"❌ {error_msg}")

            return {"success": False, "error": error_msg}

        except Exception as e:
            if verbose:
                print(f"❌ 发生错误: {str(e)}")

            return {"success": False, "error": str(e)}

    def _submit_task(
        self,
        prompt: str,
        model: str,
        size: Optional[str],
        reference_image: Optional[str],
        loras: Optional[Dict[str, float] | str]
    ) -> str:
        """提交图片生成任务"""

        payload = {
            "model": model,
            "prompt": prompt
        }

        # 添加尺寸配置（如果提供）
        if size:
            payload["size"] = size

        # 添加参考图（图生图功能）
        if reference_image:
            # 读取参考图并转为base64
            with open(reference_image, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            payload["image"] = image_data

        # 添加LoRA配置（如果提供）
        if loras:
            payload["loras"] = loras

        response = requests.post(
            f"{self.base_url}v1/images/generations",
            headers={
                **self.common_headers,
                "X-ModelScope-Async-Mode": "true"
            },
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )

        response.raise_for_status()
        return response.json()["task_id"]

    def _poll_task_status(
        self,
        task_id: str,
        check_interval: int,
        verbose: bool
    ) -> Dict[str, Any]:
        """轮询任务状态直到完成"""

        while True:
            response = requests.get(
                f"{self.base_url}v1/tasks/{task_id}",
                headers={
                    **self.common_headers,
                    "X-ModelScope-Task-Type": "image_generation"
                }
            )

            response.raise_for_status()
            data = response.json()

            if verbose:
                status = data["task_status"]
                if status in ["PENDING", "RUNNING"]:
                    print(f"   状态: {status}... (等待{check_interval}秒)")

            if data["task_status"] == "SUCCEED":
                return data
            elif data["task_status"] == "FAILED":
                return data

            time.sleep(check_interval)

    def _download_and_save_image(self, url: str, output_path: str):
        """下载并保存图片"""
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        image.save(output_path)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='ModelScope AI图片生成器 - 每天免费生成2000张图片'
    )
    parser.add_argument(
        'prompt',
        help='图片描述提示词（建议使用英文）'
    )
    parser.add_argument(
        '-o', '--output',
        default='image/result_image.jpg',
        help='输出图片路径（默认：image/result_image.jpg）'
    )
    parser.add_argument(
        '-m', '--model',
        default='Tongyi-MAI/Z-Image-Turbo',
        help='使用的模型（默认：Tongyi-MAI/Z-Image-Turbo）'
    )
    parser.add_argument(
        '-s', '--size',
        help='图片尺寸，格式：宽x高，如1024x1792(9:16)、1792x1024(16:9)、1536x1536(1:1)'
    )
    parser.add_argument(
        '-r', '--reference',
        help='参考图片路径（图生图模式，生成同风格图片）'
    )
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=5,
        help='状态检查间隔秒数（默认：5）'
    )
    parser.add_argument(
        '-k', '--api-key',
        help='ModelScope API Key（可选，默认使用内置key）'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='静默模式，减少输出'
    )

    args = parser.parse_args()

    # 创建生成器实例
    generator = ModelScopeImageGenerator(api_key=args.api_key)

    # 生成图片
    result = generator.generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        reference_image=args.reference,
        output_path=args.output,
        check_interval=args.interval,
        verbose=not args.quiet
    )

    # 返回退出码
    exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
