"""
云雾 API Provider - 使用 Gemini 2.5 Flash
🚀 快速兜底 - 响应速度快（5-10秒）
"""
import os
import base64
import time
from typing import Optional
import urllib.request
import json

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


class YunwuProvider(BaseProvider):
    """云雾 API Provider - 快速兜底方案"""

    # 分辨率映射（云雾主要依赖提示词控制）
    RESOLUTION_MAP = {
        "standard": "1024x1024",
        "high": "2048x2048",
        "16:9": "1792x1024",
        "9:16": "1024x1792",
        "1:1": "1536x1536",
        "4:3": "1536x1152",
        "3:4": "1152x1536",
    }

    # 比例到提示词格式映射
    RATIO_TO_PROMPT = {
        "16:9": "Aspect ratio: 16:9.",
        "9:16": "Aspect ratio: 9:16.",
        "1:1": "Aspect ratio: 1:1.",
        "4:3": "Aspect ratio: 4:3.",
        "3:4": "Aspect ratio: 3:4.",
        "21:9": "Aspect ratio: 21:9.",
        "3:2": "Aspect ratio: 3:2.",
    }

    def __init__(self):
        super().__init__()
        self.name = "yunwu"
        self.api_key = os.getenv("ALL_IMAGE_YUNWU_API_KEY") or os.getenv("YUNWU_API_KEY")
        self.model = os.getenv("ALL_IMAGE_YUNWU_MODEL", "gemini-2.5-flash-image-preview")
        self.base_url = os.getenv("ALL_IMAGE_YUNWU_BASE_URL", "https://yunwu.ai/v1beta/models")

        if not self.api_key:
            raise AuthenticationError(self.name, "YUNWU_API_KEY 环境变量未设置")

    def supports_image2image(self) -> bool:
        return True  # 云雾支持图生图

    def get_supported_ratios(self) -> list[str]:
        return list(self.RATIO_TO_PROMPT.keys())

    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片"""
        start_time = time.time()

        try:
            # 验证请求
            self._validate_request(request)

            # 构建提示词
            prompt = self._build_prompt(request)

            # 构建请求体
            request_body = self._build_request_body(prompt, request)

            # 发送请求
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            req = urllib.request.Request(url, data=json.dumps(request_body).encode("utf-8"), method="POST")
            req.add_header("Content-Type", "application/json")

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))

            # 解析结果
            return self._parse_result(result, time.time() - start_time, request)

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
        except Exception as e:
            raise APIError(self.name, f"未知错误: {e}", e)

    def _build_prompt(self, request: ImageRequest) -> str:
        """构建提示词"""
        prompt = request.prompt.strip()

        # 添加比例
        ratio_directive = self.RATIO_TO_PROMPT.get(request.ratio, "")
        if ratio_directive:
            prompt = f"{prompt} {ratio_directive}"

        # 添加风格
        if request.style:
            prompt = f"{prompt}，{request.style}风格"

        return prompt

    def _build_request_body(self, prompt: str, request: ImageRequest) -> dict:
        """构建请求体（Gemini 格式）"""
        return {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE", "TEXT"]
            }
        }

    def _parse_result(self, result: dict, generation_time: float, request: ImageRequest) -> ImageResult:
        """解析 API 结果"""
        try:
            # 提取 base64 数据
            base64_data = (
                result.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("inlineData", {})
                .get("data")
            )

            if not base64_data:
                raise APIError(self.name, "API 未返回图片数据")

            # 解码并保存
            image_bytes = base64.b64decode(base64_data)
            output_path = request.output_path or self._generate_output_path(request)

            import pathlib
            pathlib.Path(output_path).write_bytes(image_bytes)

            # 获取实际分辨率
            resolution = self._get_resolution_for_ratio(request.ratio)

            return ImageResult(
                success=True,
                provider=self.name,
                image_path=output_path,
                base64=base64_data,
                metadata={
                    "model": self.model,
                    "resolution": resolution,
                    "generation_time": round(generation_time, 2),
                    "provider": "云雾 API",
                    "fallback_used": False,
                }
            )

        except (KeyError, IndexError, TypeError) as e:
            raise APIError(self.name, f"解析响应失败: {e}", e)

    def _get_resolution_for_ratio(self, ratio: str) -> str:
        """根据比例获取分辨率"""
        return self.RESOLUTION_MAP.get(ratio, self.RESOLUTION_MAP["16:9"])

    def _generate_output_path(self, request: ImageRequest) -> str:
        """生成输出文件名"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ratio_safe = request.ratio.replace(":", "x")
        return f"all-image_yunwu_{timestamp}_{ratio_safe}.png"
