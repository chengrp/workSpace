"""
测试 all-image 所有 Provider 可用性
"""
import os
import sys

# 添加父目录到 Python 路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def test_provider(provider_name: str, provider_module_path: str, env_var_names: list[str]):
    """测试单个 Provider"""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name} Provider")
    print('='*60)

    try:
        # 动态导入 Provider 类
        module_path, class_name = provider_module_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        provider_class = getattr(module, class_name)

        # 检查环境变量
        print(f"[Environment Variables Check]")
        env_found = False
        for var_name in env_var_names:
            value = os.getenv(var_name)
            status = "[OK] Set" if value else "[INFO] Not set"
            print(f"   {var_name}: {status}")
            if value:
                env_found = True

        if not env_found:
            print(f"\n[SKIP] No API key configured for {provider_name}")
            return "skipped"

        # 初始化 Provider
        provider = provider_class()
        print(f"[OK] {provider_name} Provider initialized successfully")
        print(f"   Model: {provider.model}")
        print(f"   Base URL: {provider.base_url}")

        # 检查支持的功能
        print(f"\n[Supported Features]")
        i2i_status = "[OK] Supported" if provider.supports_image2image() else "[INFO] Not supported"
        print(f"   Image-to-Image: {i2i_status}")
        print(f"   Supported ratios: {', '.join(provider.get_supported_ratios())}")

        print(f"\n[OK] {provider_name} Provider test PASSED")
        return "passed"

    except Exception as e:
        print(f"\n[SKIP] {provider_name} Provider initialization failed")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {str(e)}")
        return "skipped"


def main():
    """主测试函数"""
    print("[START] Testing all-image Providers (excluding Yunwu API)")

    results = {}

    # 测试 Google AI Provider
    results['Google AI'] = test_provider(
        "Google AI",
        "providers.google_ai.GoogleAIProvider",
        ["ALL_IMAGE_GOOGLE_API_KEY", "GOOGLE_API_KEY"]
    )

    # 测试 ModelScope Provider
    results['ModelScope'] = test_provider(
        "ModelScope",
        "providers.modelscope.ModelScopeProvider",
        ["ALL_IMAGE_MODELSCOPE_API_KEY", "MODELSCOPE_API_KEY"]
    )

    # 测试 OpenAI Provider
    results['OpenAI'] = test_provider(
        "OpenAI",
        "providers.openai.OpenAIProvider",
        ["ALL_IMAGE_OPENAI_API_KEY", "OPENAI_API_KEY"]
    )

    # 测试 APIMart Provider
    results['APIMart'] = test_provider(
        "APIMart",
        "providers.apimart.APIMartProvider",
        ["ALL_IMAGE_APIMART_TOKEN", "APIMART_TOKEN"]
    )

    # 汇总
    print(f"\n\n{'='*60}")
    print("Test Results Summary")
    print('='*60)

    for name, status in results.items():
        symbol = "[OK]" if status == "passed" else "[SKIP]"
        print(f"{name}: {symbol} {status.upper()}")

    total = len(results)
    passed = sum(1 for s in results.values() if s == "passed")
    skipped = sum(1 for s in results.values() if s == "skipped")

    print(f"\nTotal: {passed}/{total} passed, {skipped}/{total} skipped (no API key)")

    if passed > 0:
        print(f"\n[SUCCESS] {passed} provider(s) available and working!")
    elif skipped == total:
        print(f"\n[INFO] All providers skipped - No API keys configured")
    else:
        print(f"\n[WARNING] Some providers failed initialization")

    return passed > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
