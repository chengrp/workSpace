"""
Provider 基类 - 所有 API Provider 的抽象接口
"""
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from pathlib import Path

# --- Global Environment Setup (Proxy & API Keys) ---
# Ensure .env is loaded regardless of how this module is imported
try:
    # Attempt to locate .env relative to this file (providers/base.py -> all-image/.env)
    current_file = Path(__file__).resolve()
    # Go up two levels: providers/ -> all-image/
    project_root = current_file.parent.parent
    env_path = project_root / ".env"

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Load if not present
                    if key not in os.environ:
                        os.environ[key] = value
                        # Enforce Proxy for urllib if present
                        if key.upper() in ("HTTP_PROXY", "HTTPS_PROXY"):
                            if key.upper() != key:
                                os.environ[key.upper()] = value
except Exception as e:
    # Silent fail or log strictly to stderr to avoid polluting stdout
    pass
# ---------------------------------------------------



class GenerationMode(Enum):
    """生成模式"""
    AUTO = "auto"           # 自动选择
    QUALITY = "quality"   # 质量优先
    SPEED = "speed"       # 速度优先
    FREE = "free"         # 成本优先


class QualityLevel(Enum):
    """质量级别"""
    STANDARD = "standard"
    HIGH = "high"
    ULTRA = "4k"


@dataclass
class ImageRequest:
    """图片生成请求"""
    prompt: str
    ratio: str = "16:9"
    quality: str = "high"
    mode: str = "auto"
    style: Optional[str] = None
    reference_image: Optional[str] = None  # base64 或文件路径
    output_path: Optional[str] = None


@dataclass
class ImageResult:
    """图片生成结果"""
    success: bool
    provider: Optional[str] = None
    image_path: Optional[str] = None
    base64: Optional[str] = None
    error: Optional[str] = None
    suggestions: list = None
    metadata: dict = None
    attempted_providers: list = None
    error_details: list = None

    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []
        if self.metadata is None:
            self.metadata = {}
        if self.attempted_providers is None:
            self.attempted_providers = []
        if self.error_details is None:
            self.error_details = []


class ImageProviderError(Exception):
    """Provider 基础异常"""
    def __init__(self, provider: str, message: str, original_error: Optional[Exception] = None):
        self.provider = provider
        self.message = message
        self.original_error = original_error
        super().__init__(f"[{provider}] {message}")


class AuthenticationError(ImageProviderError):
    """认证错误"""
    pass


class QuotaExceededError(ImageProviderError):
    """配额用尽"""
    pass


class RateLimitError(ImageProviderError):
    """速率限制"""
    pass


class InvalidPromptError(ImageProviderError):
    """提示词无效"""
    pass


class APIError(ImageProviderError):
    """API 错误"""
    pass


class BaseProvider(ABC):
    """Provider 基类"""

    def __init__(self):
        self.name = self.__class__.__name__
        self.health_status = {"healthy": True, "last_check": None, "error": None}

    @abstractmethod
    def generate(self, request: ImageRequest) -> ImageResult:
        """生成图片"""
        pass

    @abstractmethod
    def supports_image2image(self) -> bool:
        """是否支持图生图"""
        pass

    @abstractmethod
    def get_supported_ratios(self) -> list[str]:
        """支持的比例列表"""
        pass

    def check_health(self) -> dict:
        """健康检查"""
        return self.health_status

    def _validate_request(self, request: ImageRequest) -> bool:
        """验证请求参数"""
        if not request.prompt:
            raise InvalidPromptError(self.name, "提示词不能为空")

        if request.ratio not in self.get_supported_ratios():
            raise InvalidPromptError(
                self.name,
                f"不支持的比例: {request.ratio}，支持: {self.get_supported_ratios()}"
            )

        if request.reference_image and not self.supports_image2image():
            raise InvalidPromptError(
                self.name,
                f"不支持图生图"
            )

        return True
