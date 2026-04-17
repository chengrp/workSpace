#!/usr/bin/env python3
"""
测试all-image技能生成图片
"""
import sys
import os
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

def test_generate_image():
    """测试生成图片"""
    try:
        # 导入模块
        from all_image import ImageGenerator

        # 创建生成器
        gen = ImageGenerator()

        # 定义提示词
        prompts = [
            {
                "name": "封面图",
                "prompt": "奶油纸底，彩铅手绘风格，一辆赛车在高速公路上狂奔，前方出现分叉路口，一条路向上通往星空，一条路向下通向迷雾，背景是模糊的代码流和数据符号，16:9比例，标题AI狂飙之后，我们留下了什么，副标题当所有人都在加速时，谁在思考方向？"
            },
            {
                "name": "价值判断三问",
                "prompt": "奶油纸底，彩铅手绘风格，三个问号悬浮在画面中央，每个问号下面对应一句话：三个月后，这东西还有人用吗？、它离钱近吗？、AI没来时，我会做吗？背景是淡色思考气泡和灯泡图标，16:9比例"
            },
            {
                "name": "术与道",
                "prompt": "奶油纸底，彩铅手绘风格，上下对比布局，上方是术：工具技巧，配有齿轮、闪电等图标，标注快速响应、效率提升、短期收益；下方是道：本质洞察，配有大脑、眼睛等图标，标注行业理解、用户洞察、深度思考，中间有渐变过渡，16:9比例"
            }
        ]

        # 生成图片
        for item in prompts:
            print(f"\n🎨 正在生成 {item['name']}...")
            result = gen.generate(
                prompt=item['prompt'],
                ratio="16:9",
                quality="4k",
                auto_fallback=True  # 自动降级
            )

            if result.success:
                print(f"✅ {item['name']} 生成成功！")
                print(f"   路径：{result.image_path}")
                print(f"   使用的模型：{result.metadata.get('model', 'unknown')}")
                print(f"   生成时间：{result.metadata.get('generation_time', 0)}秒")
            else:
                print(f"❌ {item['name']} 生成失败：{result.error}")
                if result.suggestions:
                    print(f"   建议：{result.suggestions}")

        print("\n🎉 所有图片生成完成！")

    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generate_image()