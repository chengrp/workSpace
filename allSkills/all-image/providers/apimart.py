"""
APIMart Provider - 第三方聚合 API
支持批量生成，异步+轮询
"""
import os
import base64
import time
import urllib.request
import json
from typing import Optional

from .base import (
    BaseProvider,
    ImageRequest,
    ImageResult,
    AuthenticationError,
    QuotaExceededError,
    RateLimitError,
    InvalidPromptError,
    APIError
)


class APIMartProvider(BaseProvider):
    """APIMart 第三方聚合 Provider"""

    # 支持的比例
    SUPPORTED_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "3:2"]

    # 分辨率映射
    RESOLUTION_MAP = {
        "standard": "1K",
        "high": "2K",
        "4k": "4K",
    }

    # 比例到 APIMart 格式映射
    RATIO_MAP = {
        "16:9": "16:9",
        "9:16": "9:16",
        "1:1": "1:1",
        "4:3": "4:3",
        "3:4": "3:4",
        "21:9": "21:9",
        "3:2": "3:2",
    }

    def __init__(self):
        super().__init__()
        self.name = "apimart"
        self.token = os.getenv("ALL_IMAGE_APIMART_TOKEN") or os.getenv("APIMART_TOKEN")
        self.model = os.getenv("ALL_IMAGE_APIMART_MODEL", "gemini-3-pro-image-preview")
        self.api_url = os.getenv("ALL_IMAGE_APIMART_URL", "https://api.apimart.ai/v1/images/generations")
        self.poll_timeout = int(os.getenv("ALL_IMAGE_APIMART_POLL_TIMEOUT", "300"))
        self.poll_interval = int(os.getenv("ALL_IMAGE_APIMART_POLL_INTERVAL", "5"))

        if not self.token:
            raise AuthenticationError(self.name, "APIMART_TOKEN 环境变量未设置")

    def supports_image2image(self) -> bool:
        # APIMart 支持图生图，但需要特殊参数
        return True

    def get_supported_ratios(self) -> list[str]:
        return self.SUPPORTED_RATIOS

    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片（异步+轮询）"""
        start_time = time.time()

        try:
            # 验证请求
            self._validate_request(request)

            # 构建请求体
            request_body = self._build_request_body(request)

            # 提交任务
            task_url = self._submit_task(request_body)

            # 轮询任务状态
            result = self._poll_task(task_url)

            # 解析结果
            return self._parse_result(result, time.time() - start_time, request)

        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise AuthenticationError(self.name, "TOKEN 无效或已过期", e)
            elif e.code == 429:
                raise RateLimitError(self.name, "速率限制", e)
            else:
                raise APIError(self.name, f"HTTP 错误: {e.code}", e)
        except urllib.error.URLError as e:
            raise APIError(self.name, f"网络连接失败: {e}", e)
        except TimeoutError as e:
            raise APIError(self.name, f"任务轮询超时（{self.poll_timeout}秒）", e)
        except Exception as e:
            raise APIError(self.name, f"未知错误: {e}", e)

    def _build_request_body(self, request: ImageRequest) -> dict:
        """构建 APIMart 请求体"""
        prompt = request.prompt.strip()

        # 添加风格
        if request.style:
            prompt = f"{prompt}，{request.style}风格"

        body = {
            "model": self.model,
            "prompt": prompt,
            "size": self.RATIO_MAP.get(request.ratio, "16:9"),
            "n": 1,
            "resolution": self._get_resolution(request.quality),
        }

        # 如果有参考图，添加参数
        if request.reference_image:
            # APIMart 可能需要 base64 或 URL
            body["reference_image"] = request.reference_image

        return body

    def _get_resolution(self, quality: str) -> str:
        """获取 APIMart 格式的分辨率"""
        return self.RESOLUTION_MAP.get(quality, "2K")

    def _submit_task(self, request_body: dict) -> str:
        """提交生图任务，返回 task_url"""
        data = json.dumps(request_body, ensure_ascii=False).encode("utf-8")

        req = urllib.request.Request(url=self.api_url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {self.token}")
        req.add_header("Content-Type", "application/json")

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
        response = json.loads(body.decode("utf-8", errors="replace"))

        task_url = response.get("task_url")
        if not task_url:
            raise APIError(self.name, "API 未返回 task_url")

        return task_url

    def _poll_task(self, task_url: str) -> dict:
        """轮询任务状态直到完成"""
        start_time = time.time()

        while True:
            if time.time() - start_time > self.poll_timeout:
                raise TimeoutError(f"任务轮询超时（{self.poll_timeout}秒）")

            req = urllib.request.Request(url=task_url, method="GET")
            req.add_header("Authorization", f"Bearer {self.token}")

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    body = resp.read()
                result = json.loads(body.decode("utf-8", errors="replace"))

                status = result.get("status", "unknown")
                if status == "completed":
                    return result
                elif status == "failed":
                    error_msg = result.get("error", "未知错误")
                    raise APIError(self.name, f"任务失败: {error_msg}")

                # 等待后重试
                time.sleep(self.poll_interval)

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # 任务可能还在处理中
                    time.sleep(self.poll_interval)
                    continue
                raise

    def _parse_result(self, result: dict, generation_time: float, request: ImageRequest) -> ImageResult:
        """解析 APIMart API 结果"""
        try:
            images = result.get("images", [])
            if not images:
                raise APIError(self.name, "API 未返回图片数据")

            # 获取第一张图片
            image_url = images[0].get("url")
            if not image_url:
                raise APIError(self.name, "图片数据中缺少 URL")

            # 下载图片
            output_path = request.output_path or self._generate_output_path(request)

            with urllib.request.urlopen(image_url, timeout=30) as response:
                image_bytes = response.read()

            import pathlib
            pathlib.Path(output_path).write_bytes(image_bytes)

            # 转换为 base64
            base64_data = base64.b64encode(image_bytes).decode("utf-8")

            return ImageResult(
                success=True,
                provider=self.name,
                image_path=output_path,
                base64=base64_data,
                metadata={
                    "model": self.model,
                    "resolution": self._get_resolution(request.quality),
                    "generation_time": round(generation_time, 2),
                    "provider": "APIMart",
                    "url": image_url,
                }
            )

        except (KeyError, IndexError, TypeError) as e:
            raise APIError(self.name, f"解析响应失败: {e}", e)

    def _generate_output_path(self, request: ImageRequest) -> str:
        """生成输出文件名"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ratio_safe = request.ratio.replace(":", "x")
        return f"all-image_apimart_{timestamp}_{ratio_safe}.png"
