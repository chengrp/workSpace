"""
OpenAI Provider - 使用 DALL-E (gpt-image-1.5)
高质量生图，DALL-E 系列
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


class OpenAIProvider(BaseProvider):
    """OpenAI DALL-E Provider"""

    # 支持的比例（DALL-E 3 支持）
    SUPPORTED_RATIOS = ["1:1", "16:9", "9:16"]

    # 比例到 OpenAI 格式映射
    RATIO_TO_OPENAI = {
        "1:1": "1024x1024",
        "16:9": "1792x1024",
        "9:16": "1024x1792",
    }

    # 质量到 OpenAI 格式映射
    QUALITY_MAP = {
        "standard": "standard",
        "high": "hd",
        "4k": "hd",
    }

    def __init__(self):
        super().__init__()
        self.name = "openai"
        self.api_key = os.getenv("ALL_IMAGE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("ALL_IMAGE_OPENAI_MODEL", "dall-e-3")
        self.base_url = os.getenv("ALL_IMAGE_OPENAI_BASE_URL", "https://api.openai.com/v1")

        if not self.api_key:
            raise AuthenticationError(self.name, "OPENAI_API_KEY 环境变量未设置")

    def supports_image2image(self) -> bool:
        # DALL-E 2 支持，DALL-E 3 不直接支持（需要通过编辑 API）
        return self.model.startswith("dall-e-2")

    def get_supported_ratios(self) -> list[str]:
        return self.SUPPORTED_RATIOS

    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片"""
        start_time = time.time()

        try:
            # 验证请求
            self._validate_request(request)

            # 构建请求体
            request_body = self._build_request_body(request)

            # 发送请求
            url = f"{self.base_url}/images/generations"
            req = urllib.request.Request(
                url,
                data=json.dumps(request_body).encode("utf-8"),
                method="POST"
            )
            req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", f"Bearer {self.api_key}")

            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))

            # 解析结果
            return self._parse_result(result, time.time() - start_time, request)

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            if e.code == 401:
                raise AuthenticationError(self.name, "API Key 无效或已过期", e)
            elif e.code == 429:
                raise RateLimitError(self.name, "速率限制或配额用尽", e)
            else:
                try:
                    error_data = json.loads(error_body)
                    error_msg = error_data.get("error", {}).get("message", str(e))
                except:
                    error_msg = error_body or str(e)
                raise APIError(self.name, f"HTTP 错误: {e.code} - {error_msg}", e)
        except urllib.error.URLError as e:
            raise APIError(self.name, f"网络连接失败: {e}", e)
        except Exception as e:
            raise APIError(self.name, f"未知错误: {e}", e)

    def _build_request_body(self, request: ImageRequest) -> dict:
        """构建 DALL-E 请求体"""
        # DALL-E 3 会自动优化提示词，所以直接传入
        prompt = request.prompt.strip()

        # 添加风格信息
        if request.style:
            prompt = f"{prompt}，{request.style}风格"

        body = {
            "model": self.model,
            "prompt": prompt,
            "n": 1,
            "size": self._get_size_for_ratio(request.ratio),
        }

        # DALL-E 3 支持质量参数
        if self.model == "dall-e-3":
            body["quality"] = self._get_quality(request.quality)

        return body

    def _get_size_for_ratio(self, ratio: str) -> str:
        """获取 OpenAI 格式的尺寸"""
        return self.RATIO_TO_OPENAI.get(ratio, "1024x1024")

    def _get_quality(self, quality: str) -> str:
        """获取 OpenAI 格式的质量"""
        return self.QUALITY_MAP.get(quality, "standard")

    def _parse_result(self, result: dict, generation_time: float, request: ImageRequest) -> ImageResult:
        """解析 OpenAI API 结果"""
        try:
            # OpenAI 返回 URL，不是 base64
            image_url = result.get("data", [{}])[0].get("url")

            if not image_url:
                raise APIError(self.name, "OpenAI API 未返回图片 URL")

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
                    "resolution": self._get_size_for_ratio(request.ratio),
                    "quality": self._get_quality(request.quality),
                    "generation_time": round(generation_time, 2),
                    "provider": "OpenAI",
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
        return f"all-image_openai_{timestamp}_{ratio_safe}.png"
