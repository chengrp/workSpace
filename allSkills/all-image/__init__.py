"""
all-image - 统一生图工具
========================

智能路由 + 自动降级 + 自适应修复

示例:
    from all_image import ImageGenerator

    gen = ImageGenerator()
    result = gen.generate("一只可爱的猫咪")

    if result.success:
        print(f"✅ {result.image_path}")
    else:
        print(f"❌ {result.error}")
"""
import os
import sys
import time
from pathlib import Path

# Load .env file explicitly to ensure proxy and API keys are available
current_dir = Path(__file__).parent
env_file = current_dir / ".env"

if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Only load if not already set in environment
                    if key not in os.environ:
                        os.environ[key] = value
                        # Handle proxy variables explicitly for urllib
                        if key.upper() in ("HTTP_PROXY", "HTTPS_PROXY"):
                             # Ensure standard casing for library compatibility
                             if key.upper() != key:
                                 os.environ[key.upper()] = value
    except Exception as e:
        # Avoid crashing if .env is malformed, just log/print warning
        print(f"Warning: Failed to load .env from {env_file}: {e}", file=sys.stderr)

import logging
from typing import Optional, Union, Callable, TYPE_CHECKING
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .providers import ImageRequest, ImageResult
from .core import SmartRouter, AdaptiveRetry, RouteDecision

if TYPE_CHECKING:
    pass

# 配置日志
logger = logging.getLogger("all-image")


class ProviderConfirmationRequired(Exception):
    """需要用户确认才能切换 Provider"""
    def __init__(self, decision: RouteDecision, excluded: list[str]):
        self.decision = decision
        self.excluded = excluded
        super().__init__(
            f"⚠️ 需要确认：{decision.reason}\n"
            f"Provider: {decision.provider.name}\n"
            f"优先级: {decision.priority}\n"
            f"已排除: {excluded}\n"
            f"使用 auto_fallback=True 自动继续，或调用 confirm() 确认后重试"
        )


@dataclass
class ConfirmationRequest:
    """确认请求"""
    provider_name: str
    reason: str
    priority: int
    excluded_providers: list[str]
    message: str


class ImageGenerator:
    """
    统一生图工具 - 智能路由 + 自动降级 + 自适应修复

    特性:
        - 🚀 极简调用 - 一行代码生成图片
        - 🧠 智能路由 - 自动选择最优 API
        - 🔄 自动降级 - API 失败自动切换
        - 🛡️ 自适应修复 - 自动修复常见错误
        - 📊 详细报错 - 友好的错误信息和恢复建议
    """

    _instance = None  # 单例模式

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        enable_cache: bool = False,
        debug: bool = False,
        max_retries: int = 3,
        auto_fallback: bool = False,
        interactive: bool = False
    ):
        """
        初始化 ImageGenerator

        Args:
            enable_cache: 是否启用缓存
            debug: 是否启用调试日志
            max_retries: 最大重试次数
            auto_fallback: 是否自动降级（False=需要用户确认切换 Provider）
            interactive: 是否开启交互模式（生成前强制确认）
        """
        if self._initialized:
            return

        self._initialized = True
        self.enable_cache = enable_cache
        self.debug = debug
        self.max_retries = max_retries
        self.auto_fallback = auto_fallback
        self.interactive = interactive

        # 配置日志
        if debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format='[all-image] [%(levelname)s] %(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        # 初始化核心组件
        self.router = SmartRouter()
        self.retry = AdaptiveRetry(max_retries=max_retries)

        logger.info(f"ImageGenerator 初始化完成 (Interactive: {interactive})")

    def generate(
        self,
        prompt: str,
        ratio: str = "16:9",
        quality: str = "high",
        mode: str = "auto",
        style: Optional[str] = None,
        reference_image: Optional[str] = None,
        output_path: Optional[str] = None,
        auto_fallback: Optional[bool] = None,
        interactive: Optional[bool] = None
    ) -> ImageResult:
        """
        生成图片（极简调用）

        Args:
            prompt: 图片描述
            ratio: 宽高比 (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 3:2)
            quality: 质量 (standard, high, 4k)
            mode: 模式 (auto, quality, speed, free)
            style: 可选风格
            reference_image: 图生图参考图路径或 base64
            output_path: 输出路径（可选）
            auto_fallback: 是否自动降级（None=使用实例设置，False=需要用户确认）
            interactive: 是否交互确认（None=使用实例设置）

        Returns:
            ImageResult: 生成结果
        """
        # 使用实例设置作为默认值
        if auto_fallback is None:
            auto_fallback = self.auto_fallback
        if interactive is None:
            interactive = self.interactive

        logger.info(f"开始生成图片: {prompt[:50]}...")

        # 创建请求
        request = ImageRequest(
            prompt=prompt,
            ratio=ratio,
            quality=quality,
            style=style,
            reference_image=reference_image,
            output_path=output_path
        )
        request._mode = mode  # 存储模式供路由器使用

        # 执行生成（带重试和确认）
        result = self._execute_with_confirmation(
            request=request,
            mode=mode,
            auto_fallback=auto_fallback,
            interactive=interactive
        )

        # 日志
        if result.success:
            logger.info(f"✅ 生成成功！使用 {result.provider} ({result.metadata.get('generation_time', 0)}秒)")
            logger.info(f"图片已保存: {result.image_path}")
        else:
            logger.error(f"❌ 生成失败: {result.error}")
            if result.suggestions:
                logger.info(f"💡 恢复建议: {result.suggestions}")

        return result

    def _execute_with_confirmation(
        self,
        request: ImageRequest,
        mode: str,
        auto_fallback: bool,
        interactive: bool
    ) -> ImageResult:
        """执行生成（带确认检查）"""
        excluded_providers = []

        while True:
            # 路由决策
            decision = self.router.select_provider(request, mode, excluded_providers)

            # 交互式确认 (Feature B)
            if interactive:
                confirmed, action, value = self._interactive_confirm(request, decision)
                if not confirmed:
                    return ImageResult(success=False, error="用户取消生成", provider=None)
                
                if action == "prompt":
                    request.prompt = value
                    # 修改 Prompt 后重新路由（因为可能影响决策，虽然当前逻辑主要看 quality）
                    continue
                elif action == "provider":
                    # 用户想要切换 Provider
                    # 简单实现：将当前（首选）加入排除列表，强制选下一个
                    # 更高级实现应允许直接通过名称选
                    if decision.provider.name == value:
                         # 用户选了同一个，不需要变
                         pass
                    else:
                        # 这是一个简化的切换逻辑，实际上可能需要更复杂的选择器
                        # 这里我们假设 value 是用户想要排除的 provider，或者我们只支持“换一个”
                        # 为了支持 "切换到 X"，我们需要强制指定。
                        # 暂时实现为：如果用户选了 "switch"，我们将当前 provider 排除
                        excluded_providers.append(decision.provider.name)
                        continue

            # 检查是否需要确认 (Auto-fallback 逻辑)
            # 如果已经 interactive 确认过了，这里其实可以跳过，
            # 但 fallback 逻辑是针对 API *失败后* 的行为。
            # 这里是 "pre-flight" 确认。
            if decision.requires_confirmation and not auto_fallback and not interactive:
                # 只有在非交互模式下才抛出异常，交互模式下已经在上面确认过了(或者应该在上面处理)
                raise ProviderConfirmationRequired(decision, excluded_providers)

            # 执行生成
            try:
                result = self.retry.execute_with_retry(
                    request=request,
                    provider_selector=lambda req, excl: self._do_generate(req, excl, decision, mode),
                    original_mode=mode
                )
                return result
            except Exception as e:
                import traceback
                logger.error(f"Provider {decision.provider.name} failed: {e}")
                if self.debug:
                    traceback.print_exc()
                
                if "ProviderConfirmationRequired" in str(type(e)):
                    raise
                # 其他错误，继续降级
                excluded_providers.append(decision.provider.name)
                
                # 如果是交互模式，失败后可能也要通知用户
                if interactive:
                    print(f"\n❌ {decision.provider.name} 生成失败: {e}")
                    print("正在尝试下一个可用 Provider...")

    def _interactive_confirm(self, request: ImageRequest, decision: RouteDecision) -> tuple[bool, str, any]:
        """
        交互式确认界面
        Returns: (confirmed, action, value)
        action: 'continue', 'prompt', 'provider'
        """
        print("\n" + "="*50)
        print("🎨 all-image 生图确认")
        print("="*50)
        print(f"📝 提示词: {request.prompt}")
        print(f"📐 比例:   {request.ratio}")
        print(f"🤖 模型:   {decision.provider.name} ({decision.reason})")
        print(f"⚡ 模式:   {request._mode}")
        print("-" * 50)
        
        while True:
            choice = input("👉 操作 [Y]确认 / [M]修改提示词 / [S]切换模型 / [N]取消: ").strip().lower()
            
            if choice in ['', 'y', 'yes', 'ok']:
                return True, "continue", None
            
            elif choice in ['n', 'no', 'cancel']:
                return False, "cancel", None
            
            elif choice in ['m', 'modify', 'edit']:
                new_prompt = input("请输入新提示词: ").strip()
                if new_prompt:
                    return True, "prompt", new_prompt
            
            elif choice in ['s', 'switch', 'change']:
                print("\n当前可用 Provider:")
                # 这里简单处理，直接让用户排除当前这个，或者从列表选
                # 为了简单，直接触发“换一个”
                print(f"当前选择: {decision.provider.name}")
                print("切换模型将尝试使用下一个优先级的 Provider。")
                confirm_switch = input("确认切换到下一个推荐模型吗？(Y/N): ").strip().lower()
                if confirm_switch in ['y', 'yes']:
                    return True, "provider", "next"  # Value doesn't matter much with current logic
            
            else:
                print("无效输入，请重试。")

    def _do_generate(
        self,
        request: ImageRequest,
        excluded_providers: list[str],
        decision: RouteDecision,
        mode: str
    ) -> ImageResult:
        """实际执行生成"""
        provider = decision.provider
        logger.info(f"开始生成图片: {request.prompt[:50]}...")
        
        start_time = time.time()
        result = provider.generate(request)
        generation_time = time.time() - start_time
        
        result.metadata["generation_time"] = round(generation_time, 1)
        result.metadata["mode"] = mode
        result.metadata["router_reason"] = decision.reason
        
        return result

    def generate_batch(
        self,
        requests: list[Union[ImageRequest, dict]],
        max_concurrent: int = 3
    ) -> list[ImageResult]:
        """
        批量生成图片

        Args:
            requests: 请求列表（ImageRequest 或 dict）
            max_concurrent: 最大并发数

        Returns:
            list[ImageResult]: 结果列表
        """
        logger.info(f"开始批量生成，共 {len(requests)} 个请求")

        # 统一转换为 ImageRequest
        image_requests = []
        for req in requests:
            if isinstance(req, dict):
                image_requests.append(ImageRequest(**req))
            else:
                image_requests.append(req)

        results = []

        # 并发执行
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = {
                executor.submit(self.generate, **request.__dict__): i
                for i, request in enumerate(image_requests)
            }

            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                except Exception as e:
                    logger.error(f"请求 {idx} 失败: {e}")
                    results.append((idx, ImageResult(
                        success=False,
                        error=str(e),
                        provider=None
                    )))

        # 按原始顺序排序
        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]

    def check_provider_health(self) -> dict:
        """
        检查所有 Provider 健康状态

        Returns:
            dict: Provider 健康状态
        """
        health = {}
        available = self.router.get_available_providers()

        for provider_name in available:
            # 简单检查：是否可用
            health[provider_name] = {
                "healthy": True,
                "status": "available"
            }

        return health

    def get_available_providers(self) -> list[str]:
        """获取可用的 Provider 列表"""
        return self.router.get_available_providers()


# 函数式 API
def generate_image(
    prompt: str,
    ratio: str = "16:9",
    quality: str = "high",
    mode: str = "auto",
    style: Optional[str] = None,
    reference_image: Optional[str] = None,
    output_path: Optional[str] = None
) -> ImageResult:
    """
    函数式生图接口

    示例:
        result = generate_image("一只猫咪", ratio="16:9", quality="4k")
    """
    gen = ImageGenerator()
    return gen.generate(
        prompt=prompt,
        ratio=ratio,
        quality=quality,
        mode=mode,
        style=style,
        reference_image=reference_image,
        output_path=output_path
    )


__all__ = [
    "ImageGenerator",
    "generate_image",
    "ImageRequest",
    "ImageResult",
    "ProviderConfirmationRequired",
    "ConfirmationRequest",
]
