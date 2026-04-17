"""
Google AI Provider - 使用 Gemini 3 Pro (Nano Banana Pro) / Imagen 3
⭐ 首选 API - 最高质量，支持 4K 和图生图

使用 tenacity 实现指数退避重试，应对 503 Service Unavailable 错误
"""
import os
import base64
import time
from typing import Optional
import urllib.request
import json
import logging

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type,
    before_sleep_log
)

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

logger = logging.getLogger(__name__)


# 可重试的异常类型
class RetryableError(Exception):
    """可重试的临时错误（503、502、连接中断等）"""
    pass


class RateLimitOrServerError(Exception):
    """速率限制或服务器错误"""
    pass

class GoogleAIProvider(BaseProvider):
    """Google AI Provider (Gemini 3 Pro / Imagen via Google AI Studio)"""

    # 分辨率映射
    RESOLUTION_MAP = {
        "standard": "1024x1024",
        "high": "2048x2048",
        "4k": "4096x4096",
        "16:9": "1792x1024",
        "9:16": "1024x1792",
        "1:1": "1536x1536",
        "4:3": "1536x1152",
        "3:4": "1152x1536",
        "21:9": "2048x896",
        "3:2": "1536x1024",
    }

    # 比例到提示词格式映射
    RATIO_TO_PROMPT = {
        "16:9": "Aspect ratio: 16:9",
        "9:16": "Aspect ratio: 9:16",
        "1:1": "Aspect ratio: 1:1",
        "4:3": "Aspect ratio: 4:3",
        "3:4": "Aspect ratio: 3:4",
        "21:9": "Aspect ratio: 21:9",
        "3:2": "Aspect ratio: 3:2",
    }

    def __init__(self):
        super().__init__()
        self.name = "google_ai"
        self.api_key = os.getenv("ALL_IMAGE_GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
        # 默认使用用户指定的 Gemini 3 Pro (Banana Pro)
        self.model = os.getenv("ALL_IMAGE_GOOGLE_MODEL", "gemini-3-pro-image-preview")
        self.base_url = os.getenv("ALL_IMAGE_GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
        # 最大重试次数（与 tenacity stop_after_attempt 保持一致）
        self.max_retries = 5

        # 智能代理切换：保存原始代理配置
        self._original_proxy = os.getenv("ALL_IMAGE_PROXY", "")
        self._proxy_enabled = False  # 代理是否已启用
        self._direct_tried = False  # 是否已尝试过直连

        if not self.api_key:
            raise AuthenticationError(self.name, "GOOGLE_API_KEY 环境变量未设置")

    def supports_image2image(self) -> bool:
        return True

    def get_supported_ratios(self) -> list[str]:
        return list(self.RATIO_TO_PROMPT.keys())

    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片（带指数退避重试）"""
        start_time = time.time()

        try:
            # 验证请求
            self._validate_request(request)

            # 构建提示词
            prompt = self._build_prompt(request)

            # 构建请求体
            request_body = self._build_request_body(prompt, request)

            # 使用带重试的 API 调用
            result = self._call_api_with_retry(request_body, prompt)

            # 解析结果
            return self._parse_result(result, time.time() - start_time, request)

        except RetryableError as e:
            # 重试次数用尽，仍然失败
            raise APIError(self.name, f"重试 {self.max_retries} 次后仍然失败: {e}", e)
        except AuthenticationError as e:
            raise e
        except RateLimitError as e:
            raise e
        except APIError as e:
            raise e
        except Exception as e:
            raise APIError(self.name, f"未知错误: {e}", e)

    def _call_api_with_retry(self, request_body: dict, prompt: str) -> dict:
        """
        智能代理切换：优先直连，失败后自动启用代理

        策略：
        1. 首次调用：尝试直连（禁用代理）
        2. 直连失败：自动启用代理重试
        3. 记住成功的连接方式供后续使用
        """
        # 如果已经知道哪种方式有效，直接使用
        if self._proxy_enabled:
            logger.info("🔄 使用代理模式（已验证有效）")
            return self._do_api_call(request_body, prompt, use_proxy=True)
        elif self._direct_tried and self._original_proxy:
            # 直连失败过，有代理配置，跳过直连直接用代理
            logger.info("🔄 跳过直连，直接使用代理")
            return self._do_api_call(request_body, prompt, use_proxy=True)
        else:
            # 首次调用，优先尝试直连
            try:
                logger.info("🚀 尝试直连（无代理）...")
                self._direct_tried = True
                result = self._do_api_call(request_body, prompt, use_proxy=False)
                logger.info("✅ 直连成功！")
                return result
            except (RetryableError, urllib.error.URLError) as e:
                # 直连失败，如果有代理配置则尝试代理
                if self._original_proxy:
                    logger.warning(f"⚠️ 直连失败: {e}")
                    logger.info(f"🔄 切换到代理模式: {self._original_proxy}")
                    self._proxy_enabled = True
                    return self._do_api_call(request_body, prompt, use_proxy=True)
                else:
                    # 无代理配置，直接抛出异常
                    raise

    def _do_api_call(self, request_body: dict, prompt: str, use_proxy: bool) -> dict:
        """
        实际执行 API 调用（带 @retry 装饰器处理临时错误）
        """
        return self._api_call_with_retry(request_body, prompt, use_proxy)

    @retry(
        # 重试 RetryableError 和连接相关的异常
        retry=retry_if_exception_type(RetryableError),
        # 指数退避：1秒到60秒之间随机
        wait=wait_random_exponential(min=1, max=60),
        # 最多重试 5 次
        stop=stop_after_attempt(5),
        # 每次重试前记录日志
        before_sleep=before_sleep_log(logger, logging.WARNING),
        # 重试时重新抛出异常以便记录
        reraise=True
    )
    def _api_call_with_retry(self, request_body: dict, prompt: str, use_proxy: bool) -> dict:
        """
        实际调用 Google AI API 的方法（带重试装饰器）
        遇到 503、502、连接中断等临时错误会自动重试
        """
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

        logger.debug(f"Requesting Google AI: {url}")
        logger.debug(f"Prompt: {prompt[:100]}...")

        req = urllib.request.Request(
            url,
            data=json.dumps(request_body).encode("utf-8"),
            method="POST"
        )
        req.add_header("Content-Type", "application/json")

        # 设置代理
        proxy_handler = None
        if use_proxy and self._original_proxy:
            proxy_handler = urllib.request.ProxyHandler({
                "http": self._original_proxy,
                "https": self._original_proxy
            })
            logger.debug(f"使用代理: {self._original_proxy}")
        else:
            # 不使用代理
            proxy_handler = urllib.request.ProxyHandler({})

        # 创建 opener
        if proxy_handler:
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener()

        try:
            with opener.open(req, timeout=90) as response:
                response_data = response.read().decode("utf-8")
                result = json.loads(response_data)
                return result

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            logger.warning(f"Google API HTTP Error {e.code}: {error_body[:200]}")

            # 认证错误 - 不重试
            if e.code == 401:
                raise AuthenticationError(self.name, "API Key 无效或已过期", e)

            # 速率限制 - 不重试（需要等待更长时间）
            if e.code == 429:
                raise RateLimitError(self.name, "速率限制，请稍后再试", e)

            # 服务器错误 (500, 502, 503, 504) - 可重试
            if e.code in (500, 502, 503, 504):
                error_msg = error_body if error_body else str(e)
                logger.warning(f"服务器返回 {e.code}，触发重试...")
                raise RetryableError(f"HTTP {e.code}: {error_msg}")

            # 其他 HTTP 错误 - 不重试
            raise APIError(self.name, f"HTTP 错误: {e.code} - {error_body}", e)

        except urllib.error.URLError as e:
            # 连接中断、超时等 - 可重试
            error_msg = str(e)
            if any(keyword in error_msg.lower() for keyword in ["connection", "timeout", "reset", "refused"]):
                logger.warning(f"网络连接错误，触发重试: {error_msg}")
                raise RetryableError(f"网络连接错误: {error_msg}")
            raise APIError(self.name, f"网络连接失败: {e}", e)

        except Exception as e:
            # 捕获其他可能的网络错误（如 RemoteDisconnected）
            error_msg = str(e)
            error_type = type(e).__name__

            # 连接相关的错误都重试
            retry_keywords = ["connection", "timeout", "reset", "refused", "remote", "disconnected", "closed"]
            if any(keyword in error_msg.lower() for keyword in retry_keywords):
                logger.warning(f"连接错误 ({error_type})，触发重试: {error_msg}")
                raise RetryableError(f"{error_type}: {error_msg}")

            # 其他未知错误
            raise APIError(self.name, f"未知错误 ({error_type}): {error_msg}", e)

    def _build_prompt(self, request: ImageRequest) -> str:
        """构建提示词"""
        prompt = request.prompt.strip()

        # 添加比例指令 (这对 Gemini 生图模型很重要)
        ratio_directive = self.RATIO_TO_PROMPT.get(request.ratio, "")
        if ratio_directive:
            prompt = f"{prompt} --aspect_ratio {request.ratio.strip()}"

        # 添加风格
        if request.style:
            prompt = f"{prompt}, style: {request.style}"

        # 确保包含 generate image 指令
        if "generate" not in prompt.lower() and "image" not in prompt.lower() and "draw" not in prompt.lower():
            prompt = f"Generate an image of {prompt}"

        return prompt

    def _build_request_body(self, prompt: str, request: ImageRequest) -> dict:
        """构建请求体"""
        # Gemini 2.0 Flash 多模态 API 需要指定响应模态
        generation_config = {
            "responseModalities": ["TEXT", "IMAGE"],  # 关键：告诉 API 我们要图片
            "temperature": 0.4,
        }

        # 标准 Gemini GenerateContent 结构
        return {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": generation_config
        }

    def _parse_result(self, result: dict, generation_time: float, request: ImageRequest) -> ImageResult:
        """解析 API 结果"""
        try:
            # 尝试多种可能的返回路径
            base64_data = None
            
            candidates = result.get("candidates", [])
            if not candidates:
                 raise APIError(self.name, f"API 返回无候选项: {json.dumps(result)}")

            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            
            # 1. 检查 inlineData (标准 Gemini 多模态输出)
            for part in parts:
                if "inlineData" in part:
                    base64_data = part["inlineData"]["data"]
                    break
            
            # 2. 检查 executableCode 后的输出 (如果是通过工具调用)
            # (此处暂略，假设直接返回图片)

            if not base64_data:
                # 3. 检查是否返回了文本错误而非图片
                text_content = "".join([p.get("text", "") for p in parts])
                if text_content:
                    raise APIError(self.name, f"API 返回了文本而非图片: {text_content[:200]}...")
                raise APIError(self.name, "API 未返回图片数据 (无 inlineData)")

            # 解码并保存
            image_bytes = base64.b64decode(base64_data)
            output_path = request.output_path or self._generate_output_path(request)

            import pathlib
            pathlib.Path(output_path).write_bytes(image_bytes)

            return ImageResult(
                success=True,
                provider=self.name,
                image_path=output_path,
                base64=base64_data,
                metadata={
                    "model": self.model,
                    "resolution": self._get_resolution_for_quality(request.quality),
                    "generation_time": round(generation_time, 2),
                    "provider": "Google AI (Gemini 2.0 Flash)",
                    "fallback_used": False,
                }
            )

        except (KeyError, IndexError, TypeError) as e:
            if isinstance(e, APIError):
                raise e
            raise APIError(self.name, f"解析响应失败: {e} - Raw: {str(result)[:200]}", e)

    def _get_resolution_for_quality(self, quality: str) -> str:
        """根据质量级别获取分辨率"""
        return self.RESOLUTION_MAP.get(quality, self.RESOLUTION_MAP["high"])

    def _generate_output_path(self, request: ImageRequest) -> str:
        """生成输出文件名"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ratio_safe = request.ratio.replace(":", "x")
        return f"all-image_gemini_{timestamp}_{ratio_safe}.png"


class GoogleAIProviderFlash(GoogleAIProvider):
    """Google AI Flash Provider - 备用模型，响应更快更稳定

    当 gemini-3-pro-image-preview (Nano Banana Pro) 过载时，
    自动降级到 gemini-2.0-flash-exp-image-generation
    """

    def __init__(self):
        super().__init__()
        self.name = "google_flash"  # 区别于 google_ai
        self.model = "gemini-2.0-flash-exp-image-generation"


class GoogleAIProviderImagen(GoogleAIProvider):
    """Google Imagen 3 Provider (Legacy/Alternative)"""

    def __init__(self):
        super().__init__()
        self.name = "google_imagen"  # Distinct name to avoid overwriting google_ai
        self.model = "imagen-3.0-generate-001"
        # 即使是 Imagen，也尽可能尝试使用标准的 googleapis
        # 如果需要 OpenAI 兼容层，需用户显式配置 Base URL
