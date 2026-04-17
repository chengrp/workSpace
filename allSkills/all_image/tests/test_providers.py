"""
测试 all-image Provider 可用性
"""
import os
import sys

# 添加父目录到 Python 路径
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def test_provider(provider_name: str, provider_module_path: str):
    """测试单个 Provider"""
    print(f"\n{'='*60}")
    print(f"测试 {provider_name} Provider")
    print('='*60)

    try:
        # 动态导入 Provider 类
        module_path, class_name = provider_module_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        provider_class = getattr(module, class_name)

        # 初始化 Provider
        provider = provider_class()
        print(f"[OK] {provider_name} Provider 初始化成功")
        print(f"   模型: {provider.model}")
        print(f"   基础 URL: {provider.base_url}")

        # 检查环境变量
        print(f"\n[环境变量检查]")
        if provider_name == "Google AI":
            api_key = os.getenv("ALL_IMAGE_GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            status = "[OK] 已设置" if api_key else "[FAIL] 未设置"
            print(f"   ALL_IMAGE_GOOGLE_API_KEY: {status}")
        elif provider_name == "ModelScope":
            api_key = os.getenv("ALL_IMAGE_MODELSCOPE_API_KEY") or os.getenv("MODELSCOPE_API_KEY")
            status = "[OK] 已设置" if api_key else "[FAIL] 未设置"
            print(f"   ALL_IMAGE_MODELSCOPE_API_KEY: {status}")

        # 检查支持的功能
        print(f"\n[支持的功能]")
        i2i_status = "[OK] 支持" if provider.supports_image2image() else "[INFO] 不支持"
        print(f"   图生图: {i2i_status}")
        print(f"   支持的比例: {', '.join(provider.get_supported_ratios())}")

        print(f"\n[OK] {provider_name} Provider 测试通过")
        return True

    except Exception as e:
        print(f"\n[FAIL] {provider_name} Provider 测试失败")
        print(f"   错误类型: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        import traceback
        print(f"\n详细错误:")
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("[START] 开始测试 all-image Provider")

    results = {}

    # 测试 Google AI Provider
    results['Google AI'] = test_provider("Google AI", "providers.google_ai.GoogleAIProvider")

    # 测试 ModelScope Provider
    results['ModelScope'] = test_provider("ModelScope", "providers.modelscope.ModelScopeProvider")

    # 汇总
    print(f"\n\n{'='*60}")
    print("测试结果汇总")
    print('='*60)

    for name, passed in results.items():
        status = "[OK] 通过" if passed else "[FAIL] 失败"
        print(f"{name}: {status}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n[SUCCESS] 所有 Provider 测试通过!")
    else:
        print(f"\n[WARNING] {total - passed} 个 Provider 测试失败，请检查配置")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
