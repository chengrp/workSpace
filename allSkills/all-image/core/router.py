"""
智能路由器 - 根据请求参数自动选择最优 Provider
"""
import os
from typing import Optional
from dataclasses import dataclass

from ..providers import BaseProvider, ImageRequest
from ..providers.google_ai import GoogleAIProvider, GoogleAIProviderFlash, GoogleAIProviderImagen
from ..providers.yunwu import YunwuProvider
from ..providers.modelscope import ModelScopeProvider
from ..providers.openai import OpenAIProvider
from ..providers.apimart import APIMartProvider


@dataclass
class RouteDecision:
    """路由决策"""
    provider: BaseProvider
    reason: str
    priority: int  # 1=首选, 2=备选, 3=兜底
    requires_confirmation: bool = False  # 是否需要用户确认


class SmartRouter:
    """智能路由器 - 自动选择最优 Provider"""

    def __init__(self):
        self.providers = self._initialize_providers()

    def _initialize_providers(self) -> dict[str, BaseProvider]:
        """Initialize available providers"""
        providers = {}
        provider_classes = [
            GoogleAIProvider,
            GoogleAIProviderFlash,
            GoogleAIProviderImagen,
            YunwuProvider,
            ModelScopeProvider,
            OpenAIProvider,
            APIMartProvider,
        ]

        for provider_class in provider_classes:
            try:
                # Provider __init__ checks for API keys
                provider = provider_class()
                providers[provider.name] = provider
            except Exception:
                # Skip if not configured/available
                pass

        return providers

    def select_provider(
        self,
        request: ImageRequest,
        mode: str = "auto",
        excluded_providers: Optional[list[str]] = None
    ) -> RouteDecision:
        """
        Smartly select the best provider
        """
        excluded = excluded_providers or []
        
        # Ensure we don't try exclude providers that don't exist
        available_providers = [p for p in self.providers.keys() if p not in excluded]
        
        if not available_providers:
             raise ValueError("所有生图 API 均不可用或已被排除，请检查 API Key 配置")

        if mode == "quality":
            return self._select_for_quality(request, excluded)
        elif mode == "speed":
            return self._select_for_speed(request, excluded)
        elif mode == "free":
            return self._select_for_free(request, excluded)
        else:  # auto
            return self._select_auto(request, excluded)

    def _select_auto(self, request: ImageRequest, excluded: list[str]) -> RouteDecision:
        """
        Automatic Mode Strategy:
        1. Google AI (Gemini 3 Pro - SOTA，可能过载)
        2. Google Flash (Gemini 2.0 Flash - 稳定备选)
        3. Google Imagen (Alternative High Quality)
        4. Yunwu/OpenAI/ModelScope/APIMart (Fallback - 需要确认)
        """

        # === Priority 1: Google AI (Gemini 3 Pro) ===
        if "google_ai" not in excluded and "google_ai" in self.providers:
            return RouteDecision(
                provider=self.providers["google_ai"],
                reason="首选 Google AI (最高质量/Gemini 3 Pro)",
                priority=1,
                requires_confirmation=False
            )

        # === Priority 1.5: Google Flash (稳定备选，不需要确认) ===
        if "google_flash" not in excluded and "google_flash" in self.providers:
            return RouteDecision(
                provider=self.providers["google_flash"],
                reason="备选 Google Flash (Gemini 2.0 - 响应快更稳定)",
                priority=1,
                requires_confirmation=False  # 仍是 Google，不需要确认
            )

        # === Priority 2: Google Imagen (Alternative) ===
        if "google_imagen" not in excluded and "google_imagen" in self.providers:
             return RouteDecision(
                provider=self.providers["google_imagen"],
                reason="备选 Google Imagen 3",
                priority=1,
                requires_confirmation=False # Still Google, safe
            )

        # === Priority 3: Fallbacks (Require Confirmation by default in Auto mode) ===

        # Yunwu (Fast)
        if "yunwu" not in excluded and "yunwu" in self.providers:
            return RouteDecision(
                provider=self.providers["yunwu"],
                reason="降级到云雾 API (快速)",
                priority=2,
                requires_confirmation=True
            )
            
        # OpenAI (DALL-E)
        if "openai" not in excluded and "openai" in self.providers:
             return RouteDecision(
                provider=self.providers["openai"],
                reason="降级到 OpenAI (DALL-E 3)",
                priority=2,
                requires_confirmation=True
            )

        # ModelScope (Free/Cheap)
        if "modelscope" not in excluded and "modelscope" in self.providers:
            return RouteDecision(
                provider=self.providers["modelscope"],
                reason="兜底到 ModelScope (免费额度)",
                priority=3,
                requires_confirmation=True
            )
            
        # APIMart
        if "apimart" not in excluded and "apimart" in self.providers:
             return RouteDecision(
                provider=self.providers["apimart"],
                reason="兜底到 APIMart",
                priority=3,
                requires_confirmation=True
            )

        raise ValueError("没有可用的生图服务")

    def _select_for_quality(self, request: ImageRequest, excluded: list[str]) -> RouteDecision:
        """质量优先模式"""
        # 1. Google AI (最高质量 - Gemini 3 Pro)
        if "google_ai" not in excluded and "google_ai" in self.providers:
            return RouteDecision(
                provider=self.providers["google_ai"],
                reason="质量优先：Google AI (Gemini 3 Pro)",
                priority=1,
                requires_confirmation=False
            )

        # 1.5. Google Flash (稳定备选 - Gemini 2.0)
        if "google_flash" not in excluded and "google_flash" in self.providers:
            return RouteDecision(
                provider=self.providers["google_flash"],
                reason="质量备选：Google Flash (Gemini 2.0)",
                priority=1,
                requires_confirmation=False
            )

        # 2. Google Imagen
        if "google_ai_imagen" not in excluded and "google_ai_imagen" in self.providers:
            return RouteDecision(
                provider=self.providers["google_ai_imagen"],
                reason="质量优先：Google Imagen 3",
                priority=1,
                requires_confirmation=False
            )

        # 3. 云雾 API - 需要确认
        if "yunwu" not in excluded and "yunwu" in self.providers:
            return RouteDecision(
                provider=self.providers["yunwu"],
                reason="质量备选：云雾 API",
                priority=2,
                requires_confirmation=True
            )

        raise ValueError("没有可用的 Provider")

    def _select_for_speed(self, request: ImageRequest, excluded: list[str]) -> RouteDecision:
        """速度优先模式"""
        # 1. 云雾 API (最快) - 如果是 speed 模式，云雾是首选，不需要确认
        if "yunwu" not in excluded and "yunwu" in self.providers:
            return RouteDecision(
                provider=self.providers["yunwu"],
                reason="速度优先：云雾 API (Gemini 2.5 Flash)",
                priority=1,
                requires_confirmation=False
            )

        # 2. ModelScope - 需要确认
        if "modelscope" not in excluded and "modelscope" in self.providers:
            return RouteDecision(
                provider=self.providers["modelscope"],
                reason="速度备选：ModelScope",
                priority=2,
                requires_confirmation=True
            )

        raise ValueError("没有可用的 Provider")

    def _select_for_free(self, request: ImageRequest, excluded: list[str]) -> RouteDecision:
        """免费优先模式"""
        # 1. ModelScope (免费额度) - 如果是 free 模式，ModelScope 是首选，不需要确认
        if "modelscope" not in excluded and "modelscope" in self.providers:
            return RouteDecision(
                provider=self.providers["modelscope"],
                reason="免费优先：ModelScope (2000张/天)",
                priority=1,
                requires_confirmation=False
            )

        raise ValueError("没有可用的免费 Provider")

    def get_available_providers(self) -> list[str]:
        """获取可用的 Provider 列表"""
        return list(self.providers.keys())

    def is_provider_available(self, provider_name: str) -> bool:
        """检查 Provider 是否可用"""
        return provider_name in self.providers
