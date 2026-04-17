"""
自适应重试 - 智能错误处理和自动修复
"""
import time
import re
from typing import Optional, Callable
from dataclasses import dataclass, field

from ..providers import (
    BaseProvider,
    ImageRequest,
    ImageResult,
    APIError,
    AuthenticationError,
    QuotaExceededError,
    RateLimitError,
    InvalidPromptError
)


@dataclass
class RetryAttempt:
    """重试记录"""
    provider_name: str
    success: bool
    error: Optional[str] = None
    error_type: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class RetryHistory:
    """重试历史"""
    attempts: list[RetryAttempt] = field(default_factory=list)
    total_attempts: int = 0
    success_provider: Optional[str] = None
    total_time: float = 0.0

    def add_attempt(self, attempt: RetryAttempt):
        self.attempts.append(attempt)
        self.total_attempts += 1

    def get_error_summary(self) -> list[str]:
        """获取错误摘要"""
        return [
            f"{attempt.provider_name}: {attempt.error_type or 'UnknownError'} - {attempt.error or '未知错误'}"
            for attempt in self.attempts
            if not attempt.success
        ]


class AdaptiveRetry:
    """自适应重试器 - 智能错误处理和自动修复"""

    # 自动修复规则
    FIX_RULES = {
        "missing_aspect_ratio": {
            "patterns": [r"aspect ratio", r"尺寸", r"resolution"],
            "fix": lambda p: f"{p} Aspect ratio: 16:9."
        },
        "prompt_too_short": {
            "patterns": [r"too short", r"太短", r"至少.*字符"],
            "fix": lambda p: f"{p}，详细描述，高质量"
        },
        "sensitive_content": {
            "patterns": [r"sensitive", r"敏感", r"policy"],
            "fix": lambda p: re.sub(r'[^\w\s\u4e00-\u9fff,。，！？、]', '', p)
        },
    }

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def execute_with_retry(
        self,
        request: ImageRequest,
        provider_selector: Callable[[ImageRequest, list[str]], ImageResult],
        original_mode: str = "auto"
    ) -> ImageResult:
        """
        执行带重试的生图请求

        Args:
            request: 图片生成请求
            provider_selector: Provider 选择器函数
            original_mode: 原始模式（用于日志）

        Returns:
            ImageResult: 生成结果
        """
        history = RetryHistory()
        excluded_providers = []
        modified_request = request
        start_time = time.time()

        for attempt in range(self.max_retries):
            try:
                # 尝试生成
                result = provider_selector(modified_request, excluded_providers)

                # 成功
                history.success_provider = result.provider
                history.total_time = time.time() - start_time
                result.metadata["retries"] = history.total_attempts - 1
                result.metadata["fallback_used"] = history.total_attempts > 1
                result.metadata["history"] = history

                return result

            except InvalidPromptError as e:
                # 尝试自动修复提示词
                attempt_record = RetryAttempt(
                    provider_name=getattr(e, 'provider_name', 'unknown'),
                    success=False,
                    error=str(e),
                    error_type="InvalidPromptError"
                )
                history.add_attempt(attempt_record)

                fixed_request = self._try_fix_prompt(modified_request, str(e))
                if fixed_request:
                    modified_request = fixed_request
                    continue  # 重试修复后的请求
                else:
                    # 无法修复，添加到排除列表
                    if hasattr(e, 'provider_name') and e.provider_name:
                        excluded_providers.append(e.provider_name)

            except (AuthenticationError, QuotaExceededError) as e:
                # 配置问题，切换 Provider
                attempt_record = RetryAttempt(
                    provider_name=getattr(e, 'provider_name', 'unknown'),
                    success=False,
                    error=str(e),
                    error_type=type(e).__name__
                )
                history.add_attempt(attempt_record)

                # 添加到排除列表
                if hasattr(e, 'provider_name') and e.provider_name:
                    excluded_providers.append(e.provider_name)

            except RateLimitError as e:
                # 速率限制，等待后重试
                attempt_record = RetryAttempt(
                    provider_name=getattr(e, 'provider_name', 'unknown'),
                    success=False,
                    error=str(e),
                    error_type="RateLimitError"
                )
                history.add_attempt(attempt_record)

                # 等待 2 秒后重试
                time.sleep(2)

            except APIError as e:
                # 其他 API 错误，切换 Provider
                attempt_record = RetryAttempt(
                    provider_name=getattr(e, 'provider_name', 'unknown'),
                    success=False,
                    error=str(e),
                    error_type="APIError"
                )
                history.add_attempt(attempt_record)

                # 添加到排除列表
                if hasattr(e, 'provider_name') and e.provider_name:
                    excluded_providers.append(e.provider_name)

        # 所有重试都失败
        history.total_time = time.time() - start_time
        return self._create_failure_result(history, request)

    def _try_fix_prompt(self, request: ImageRequest, error_message: str) -> Optional[ImageRequest]:
        """尝试自动修复提示词"""
        prompt = request.prompt

        # 检查是否匹配任何修复规则
        for rule_name, rule in self.FIX_RULES.items():
            for pattern in rule["patterns"]:
                if re.search(pattern, error_message, re.IGNORECASE):
                    # 应用修复
                    fixed_prompt = rule["fix"](prompt)
                    if fixed_prompt != prompt:
                        # 创建修复后的请求
                        return ImageRequest(
                            prompt=fixed_prompt,
                            ratio=request.ratio,
                            quality=request.quality,
                            style=request.style,
                            reference_image=request.reference_image,
                            output_path=request.output_path
                        )

        return None

    def _create_failure_result(self, history: RetryHistory, request: ImageRequest) -> ImageResult:
        """创建失败结果"""
        error_details = history.get_error_summary()
        attempted_providers = list(set([a.provider_name for a in history.attempts]))

        # 生成恢复建议
        suggestions = self._generate_suggestions(error_details, attempted_providers)

        return ImageResult(
            success=False,
            error=f"所有生图 API 均不可用（已尝试 {history.total_attempts} 次）",
            provider=None,
            image_path=None,
            base64=None,
            suggestions=suggestions,
            attempted_providers=attempted_providers,
            error_details=error_details,
            metadata={
                "total_attempts": history.total_attempts,
                "total_time": round(history.total_time, 2),
                "history": history
            }
        )

    def _generate_suggestions(self, error_details: list[str], attempted_providers: list[str]) -> list[str]:
        """生成恢复建议"""
        suggestions = []

        # 根据错误类型生成建议
        for error in error_details:
            if "AuthenticationError" in error:
                suggestions.append("检查 API Key 是否正确配置")
            elif "QuotaExceededError" in error:
                suggestions.append("配额已用完，请考虑使用其他 Provider")
            elif "RateLimitError" in error:
                suggestions.append("请求过于频繁，请稍后重试")
            elif "InvalidPromptError" in error:
                suggestions.append("提示词可能包含敏感内容，请修改后重试")

        # 去重
        suggestions = list(dict.fromkeys(suggestions))

        # 添加通用建议
        if not any("ModelScope" in p for p in attempted_providers):
            suggestions.append("尝试使用 ModelScope（免费额度）")

        if not any("google_ai" in p or "yunwu" in p for p in attempted_providers):
            suggestions.append("配置 Google AI 或云雾 API 以获得更高质量")

        return suggestions
