"""
ModelScope Provider - 使用 Z-Image-Turbo
🆓 免费额度 - 2000张/天，支持图生图
"""
import os
import base64
import time
import urllib.request
import urllib.error
import json
from typing import Optional
from pathlib import Path

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


class ModelScopeProvider(BaseProvider):
    """ModelScope Provider - 免费额度兜底方案"""

    # 分辨率映射（ModelScope 使用 "宽x高" 格式）
    RESOLUTION_MAP = {
        "standard": "1024x1024",
        "high": "2048x2048",
        "16:9": "1792x1024",
        "9:16": "1024x1792",
        "1:1": "1536x1536",
        "4:3": "1536x1152",
        "3:4": "1152x1536",
    }

    def __init__(self):
        super().__init__()
        self.name = "modelscope"
        self.api_key = os.getenv("ALL_IMAGE_MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_API_KEY")
        self.model = os.getenv("ALL_IMAGE_MODELSCOPE_MODEL", "Tongyi-MAI/Z-Image-Turbo")
        self.base_url = os.getenv("ALL_IMAGE_MODELSCOPE_BASE_URL", "https://api-inference.modelscope.cn/v1")
        self.poll_timeout = int(os.getenv("ALL_IMAGE_MODELSCOPE_POLL_TIMEOUT", "300"))
        self.poll_interval = int(os.getenv("ALL_IMAGE_MODELSCOPE_POLL_INTERVAL", "5"))

        if not self.api_key:
            raise AuthenticationError(self.name, "MODELSCOPE_API_KEY 环境变量未设置")

    def supports_image2image(self) -> bool:
        return True  # ModelScope 支持图生图

    def get_supported_ratios(self) -> list[str]:
        return list(self.RESOLUTION_MAP.keys())

    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片（异步 + 轮询）"""
        start_time = time.time()

        try:
            # 验证请求
            self._validate_request(request)

            # 提交任务
            task_id = self._submit_task(request)

            # 轮询结果
            result = self._poll_result(task_id, start_time)

            # 下载图片
            return self._download_and_save(result, time.time() - start_time, request)

        except urllib.error.HTTPError as e:
            if e.code == 401:
                raise AuthenticationError(self.name, "API Key 无效或已过期", e)
            elif e.code == 429:
                raise RateLimitError(self.name, "速率限制", e)
            elif e.code == 400:
                raise InvalidPromptError(self.name, "提示词格式错误或包含敏感内容", e)
            else:
                raise APIError(self.name, f"HTTP 错误: {e.code}", e)
        except urllib.error.URLError as e:
            raise APIError(self.name, f"网络连接失败: {e}", e)
        except TimeoutError as e:
            raise APIError(self.name, f"任务轮询超时（{self.poll_timeout}秒）", e)
        except Exception as e:
            raise APIError(self.name, f"未知错误: {e}", e)

    def _submit_task(self, request: ImageRequest) -> str:
        """提交生图任务"""
        url = f"{self.base_url}/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-ModelScope-Async-Mode": "true"
        }

        # 构建请求体
        size = self._get_resolution_for_ratio(request.ratio)
        request_body = {
            "model": self.model,
            "prompt": self._build_prompt(request),
            "size": size
        }

        # 如果是图生图
        if request.reference_image:
            request_body["image"] = request.reference_image

        req = urllib.request.Request(url, data=json.dumps(request_body).encode("utf-8"), method="POST")
        for key, value in headers.items():
            req.add_header(key, value)

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

        # 提取 task_id
        task_id = result.get("task_id") or result.get("id")
        if not task_id:
            raise APIError(self.name, "API 未返回 task_id")

        return task_id

    def _poll_result(self, task_id: str, start_time: float) -> dict:
        """轮询任务结果"""
        url = f"{self.base_url}/images/generations/{task_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        while time.time() - start_time < self.poll_timeout:
            try:
                req = urllib.request.Request(url, headers=headers, method="GET")
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode("utf-8"))

                status = result.get("task_status") or result.get("status")

                if status == "SUCCEED" or status == "SUCCESS":
                    return result
                elif status == "FAILED":
                    error_msg = result.get("error", "未知错误")
                    raise APIError(self.name, f"任务失败: {error_msg}")

                # 继续等待
                time.sleep(self.poll_interval)

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # 任务可能还未就绪，继续轮询
                    time.sleep(self.poll_interval)
                    continue
                else:
                    raise

        raise TimeoutError(f"任务轮询超时（{self.poll_timeout}秒）")

    def _download_and_save(self, result: dict, generation_time: float, request: ImageRequest) -> ImageResult:
        """下载图片并保存"""
        try:
            # 提取图片 URL
            output_images = result.get("output_images") or result.get("data", [])
            if not output_images:
                raise APIError(self.name, "API 未返回图片 URL")

            image_url = output_images[0]

            # 下载图片
            with urllib.request.urlopen(image_url, timeout=30) as response:
                image_bytes = response.read()

            # 保存图片
            output_path = request.output_path or self._generate_output_path(request)
            Path(output_path).write_bytes(image_bytes)

            # 转换为 base64
            base64_data = base64.b64encode(image_bytes).decode("utf-8")

            return ImageResult(
                success=True,
                provider=self.name,
                image_path=output_path,
                base64=base64_data,
                metadata={
                    "model": self.model,
                    "resolution": self._get_resolution_for_ratio(request.ratio),
                    "generation_time": round(generation_time, 2),
                    "provider": "ModelScope",
                    "fallback_used": False,
                }
            )

        except (KeyError, IndexError, TypeError) as e:
            raise APIError(self.name, f"处理结果失败: {e}", e)

    def _build_prompt(self, request: ImageRequest) -> str:
        """构建提示词"""
        prompt = request.prompt.strip()

        # 添加风格
        if request.style:
            prompt = f"{prompt}，{request.style}风格"

        return prompt

    def _get_resolution_for_ratio(self, ratio: str) -> str:
        """根据比例获取分辨率"""
        return self.RESOLUTION_MAP.get(ratio, self.RESOLUTION_MAP["16:9"])

    def _generate_output_path(self, request: ImageRequest) -> str:
        """生成输出文件名"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ratio_safe = request.ratio.replace(":", "x")
        return f"all-image_modelscope_{timestamp}_{ratio_safe}.png"
