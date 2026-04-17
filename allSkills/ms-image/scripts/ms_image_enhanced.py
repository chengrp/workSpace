"""
ModelScope AI图片生成器 - 增强版
支持批量生成、Prompt优化、额度管理、预设模板
"""

import sys
import io
import requests
import time
import json
import base64
import os
from datetime import datetime
from PIL import Image
from io import BytesIO
from typing import Optional, Dict, Any, List
import argparse

# 设置stdout为utf-8编码
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass


# ==================== 预设风格模板 ====================
STYLE_TEMPLATES = {
    "cyberpunk": {
        "name": "赛博朋克",
        "keywords": "Cyberpunk style, neon lights, futuristic architecture, night city, rain, dark atmosphere, highly detailed, digital art",
        "quality": "4K, cinematic lighting, professional quality"
    },
    "watercolor": {
        "name": "水彩画",
        "keywords": "Watercolor painting style, soft edges, artistic, pastel colors, hand-painted, traditional art",
        "quality": "high quality art, masterpiece"
    },
    "realistic": {
        "name": "写实摄影",
        "keywords": "Photorealistic, professional photography, natural lighting, high detail, sharp focus",
        "quality": "4K, DSLR quality, professional camera"
    },
    "anime": {
        "name": "日系动漫",
        "keywords": "Anime style, manga art, vibrant colors, clean lines, Japanese animation",
        "quality": "high quality anime, detailed illustration"
    },
    "oilpainting": {
        "name": "油画",
        "keywords": "Oil painting style, textured brushstrokes, classic art, rich colors, masterpiece",
        "quality": "museum quality, classical painting"
    },
    "3drender": {
        "name": "3D渲染",
        "keywords": "3D render, octane render, blender, cgi, highly detailed, volumetric lighting",
        "quality": "8K, photorealistic 3D, professional render"
    },
    "pixelart": {
        "name": "像素艺术",
        "keywords": "Pixel art, retro game style, 8-bit, 16-bit, nostalgic",
        "quality": "high quality pixel art, detailed sprite"
    },
    "minimalist": {
        "name": "极简主义",
        "keywords": "Minimalist, clean design, simple composition, negative space, modern art",
        "quality": "professional design, high quality"
    }
}


# ==================== Prompt优化器 ====================
class PromptOptimizer:
    """Prompt优化助手"""

    # 质量增强词库
    QUALITY_ENHANCERS = [
        "highly detailed",
        "professional quality",
        "sharp focus",
        "best quality",
        "masterpiece"
    ]

    # 风格增强词库
    STYLE_ENHANCERS = {
        "角色": "character design, detailed features, expressive",
        "风景": "scenic view, atmospheric, beautiful landscape",
        "建筑": "architectural, detailed structure, professional photography",
        "动物": "wildlife photography, detailed fur, natural pose",
        "抽象": "abstract art, creative, unique composition"
    }

    @staticmethod
    def enhance(prompt: str, style: str = None, auto_enhance: bool = True) -> str:
        """
        增强prompt

        Args:
            prompt: 原始prompt
            style: 风格模板名称（如 cyberpunk）
            auto_enhance: 是否自动增强

        Returns:
            增强后的prompt
        """
        parts = []

        # 添加原始内容
        parts.append(prompt)

        # 应用风格模板
        if style and style in STYLE_TEMPLATES:
            style_template = STYLE_TEMPLATES[style]
            parts.append(style_template["keywords"])
            parts.append(style_template["quality"])

        # 自动增强
        elif auto_enhance:
            # 添加质量词
            parts.extend(PromptOptimizer.QUALITY_ENHANCERS[:2])

            # 检测内容类型并添加相应增强词
            for keyword, enhancer in PromptOptimizer.STYLE_ENHANCERS.items():
                if keyword in prompt:
                    parts.append(enhancer)
                    break

        return ", ".join(parts)

    @staticmethod
    def translate_to_english(text: str) -> str:
        """
        简单的中英文转换（基础版）
        TODO: 可以接入翻译API实现完整翻译
        """
        # 常用词汇映射
        common_words = {
            "猫": "cat", "狗": "dog", "风景": "landscape",
            "城市": "city", "森林": "forest", "山": "mountain",
            "海": "ocean", "日落": "sunset", "日出": "sunrise",
            "人物": "person", "女孩": "girl", "男孩": "boy",
            "未来": "futuristic", "科技": "technology", "霓虹灯": "neon lights"
        }

        result = text
        for cn, en in common_words.items():
            result = result.replace(cn, en)

        return result


# ==================== 额度管理器 ====================
class QuotaManager:
    """额度管理器"""

    def __init__(self, quota_file: str = "quota.json"):
        self.quota_file = quota_file
        self.daily_quota = 2000
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """加载额度数据"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 检查日期是否重置
                today = datetime.now().strftime("%Y-%m-%d")
                if data.get("date") != today:
                    data = {"date": today, "used": 0}
                return data
        else:
            return {"date": datetime.now().strftime("%Y-%m-%d"), "used": 0}

    def _save_data(self):
        """保存额度数据"""
        with open(self.quota_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def record_usage(self, count: int = 1):
        """记录使用次数"""
        self.data["used"] += count
        self._save_data()

    def get_remaining(self) -> int:
        """获取剩余额度"""
        return max(0, self.daily_quota - self.data["used"])

    def get_used(self) -> int:
        """获取已使用数量"""
        return self.data["used"]

    def show_status(self):
        """显示额度状态"""
        used = self.get_used()
        remaining = self.get_remaining()
        percentage = (used / self.daily_quota) * 100

        print(f"\n{'='*50}")
        print(f"📊 额度使用情况")
        print(f"{'='*50}")
        print(f"日期: {self.data['date']}")
        print(f"已用: {used}/{self.daily_quota} ({percentage:.1f}%)")
        print(f"剩余: {remaining}")
        print(f"{'='*50}\n")


# ==================== 增强版图片生成器 ====================
class EnhancedImageGenerator:
    """增强版图片生成器"""

    def __init__(
        self,
        api_key: str = None,
        quota_manager: QuotaManager = None
    ):
        self.api_key = api_key or "ms-51dd7494-0706-45d9-a901-c395522c55f2"
        self.base_url = 'https://api-inference.modelscope.cn/'
        self.quota_manager = quota_manager or QuotaManager()
        self.common_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = "Tongyi-MAI/Z-Image-Turbo",
        size: Optional[str] = None,
        reference_image: Optional[str] = None,
        loras: Optional[Dict[str, float] | str] = None,
        output_path: str = "image/result_image.jpg",
        check_interval: int = 5,
        verbose: bool = True,
        style: Optional[str] = None,
        enhance_prompt: bool = True
    ) -> Dict[str, Any]:
        """
        生成AI图片（增强版）

        Args:
            prompt: 图片描述
            style: 风格模板（如 cyberpunk）
            enhance_prompt: 是否优化prompt
            其他参数同基础版
        """
        try:
            # Prompt优化
            optimized_prompt = PromptOptimizer.enhance(
                prompt,
                style=style,
                auto_enhance=enhance_prompt
            )

            if verbose and optimized_prompt != prompt:
                print(f"📝 Prompt优化:")
                print(f"   原始: {prompt}")
                print(f"   优化: {optimized_prompt}\n")

            # 提交任务
            if verbose:
                print(f"📤 正在提交图片生成任务...")
                print(f"   Prompt: {optimized_prompt}")
                print(f"   Model: {model}")
                if size:
                    print(f"   Size: {size}")
                if style:
                    print(f"   风格: {STYLE_TEMPLATES[style]['name']}")

            task_id = self._submit_task(optimized_prompt, model, size, reference_image, loras)

            if verbose:
                print(f"✅ 任务已提交，Task ID: {task_id}")
                print(f"⏳ 正在等待生成完成...")

            # 轮询状态
            result = self._poll_task_status(task_id, check_interval, verbose)

            # 下载图片
            if result["task_status"] == "SUCCEED":
                image_url = result["output_images"][0]
                self._download_and_save_image(image_url, output_path)

                # 记录额度使用
                self.quota_manager.record_usage(1)

                if verbose:
                    print(f"✅ 图片已成功生成并保存到: {output_path}")
                    print(f"💰 剩余额度: {self.quota_manager.get_remaining()}")

                return {
                    "success": True,
                    "output_path": output_path,
                    "image_url": image_url,
                    "task_id": task_id,
                    "prompt_used": optimized_prompt
                }
            else:
                if verbose:
                    print(f"❌ 图片生成失败: {result.get('error_message', '未知错误')}")

                return {
                    "success": False,
                    "error": result.get('error_message', '未知错误'),
                    "task_id": task_id
                }

        except Exception as e:
            if verbose:
                print(f"❌ 发生错误: {str(e)}")

            return {"success": False, "error": str(e)}

    def generate_batch(
        self,
        prompt: str,
        count: int = 4,
        output_dir: str = "image/batch",
        style: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        批量生成图片

        Args:
            prompt: 图片描述
            count: 生成数量
            output_dir: 输出目录
            style: 风格模板
            **kwargs: 其他参数

        Returns:
            生成结果列表
        """
        results = []
        os.makedirs(output_dir, exist_ok=True)

        print(f"🔄 开始批量生成 {count} 张图片...")

        for i in range(count):
            output_path = f"{output_dir}/batch_{i+1}_{int(time.time())}.jpg"

            print(f"\n[{i+1}/{count}] 生成第 {i+1} 张图片...")

            result = self.generate_image(
                prompt=prompt,
                output_path=output_path,
                style=style,
                **kwargs
            )

            results.append(result)

            # 检查额度
            if self.quota_manager.get_remaining() <= 0:
                print(f"\n⚠️ 额度已用完，停止生成")
                break

            # 避免过快请求
            if i < count - 1:
                time.sleep(2)

        # 统计结果
        success_count = sum(1 for r in results if r.get("success"))
        print(f"\n{'='*50}")
        print(f"批量生成完成: {success_count}/{len(results)} 成功")
        print(f"{'='*50}")

        return results

    def _submit_task(
        self,
        prompt: str,
        model: str,
        size: Optional[str],
        reference_image: Optional[str],
        loras: Optional[Dict[str, float] | str]
    ) -> str:
        """提交图片生成任务"""
        payload = {
            "model": model,
            "prompt": prompt
        }

        if size:
            payload["size"] = size

        if reference_image:
            with open(reference_image, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            payload["image"] = image_data

        if loras:
            payload["loras"] = loras

        response = requests.post(
            f"{self.base_url}v1/images/generations",
            headers={
                **self.common_headers,
                "X-ModelScope-Async-Mode": "true"
            },
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )

        response.raise_for_status()
        return response.json()["task_id"]

    def _poll_task_status(
        self,
        task_id: str,
        check_interval: int,
        verbose: bool
    ) -> Dict[str, Any]:
        """轮询任务状态直到完成"""
        while True:
            response = requests.get(
                f"{self.base_url}v1/tasks/{task_id}",
                headers={
                    **self.common_headers,
                    "X-ModelScope-Task-Type": "image_generation"
                }
            )

            response.raise_for_status()
            data = response.json()

            if verbose:
                status = data["task_status"]
                if status in ["PENDING", "RUNNING"]:
                    print(f"   状态: {status}... (等待{check_interval}秒)")

            if data["task_status"] == "SUCCEED":
                return data
            elif data["task_status"] == "FAILED":
                return data

            time.sleep(check_interval)

    def _download_and_save_image(self, url: str, output_path: str):
        """下载并保存图片"""
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)


# ==================== 命令行入口 ====================
def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='ModelScope AI图片生成器 - 增强版'
    )

    # 基础参数
    parser.add_argument(
        'prompt',
        nargs='?',
        help='图片描述提示词'
    )

    # 新增参数
    parser.add_argument(
        '--style',
        choices=list(STYLE_TEMPLATES.keys()),
        help='预设风格模板'
    )
    parser.add_argument(
        '--batch',
        type=int,
        help='批量生成数量'
    )
    parser.add_argument(
        '--no-enhance',
        action='store_true',
        help='禁用prompt自动优化'
    )
    parser.add_argument(
        '--quota',
        action='store_true',
        help='查看额度使用情况'
    )
    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='列出所有可用风格'
    )

    # 原有参数
    parser.add_argument('-o', '--output', default='image/result_image.jpg')
    parser.add_argument('-m', '--model', default='Tongyi-MAI/Z-Image-Turbo')
    parser.add_argument('-s', '--size', help='图片尺寸，如1920x1080')
    parser.add_argument('-r', '--reference', help='参考图片路径（图生图）')
    parser.add_argument('-i', '--interval', type=int, default=5)
    parser.add_argument('-k', '--api-key')
    parser.add_argument('-q', '--quiet', action='store_true')

    args = parser.parse_args()

    # 创建生成器
    generator = EnhancedImageGenerator(api_key=args.api_key)

    # 列出风格
    if args.list_styles:
        print("\n🎨 可用风格模板:")
        print("="*50)
        for key, value in STYLE_TEMPLATES.items():
            print(f"{key:15} - {value['name']}")
        print("="*50)
        return

    # 显示额度
    if args.quota:
        generator.quota_manager.show_status()
        return

    # 检查prompt
    if not args.prompt:
        parser.print_help()
        return

    # 批量生成
    if args.batch:
        generator.generate_batch(
            prompt=args.prompt,
            count=args.batch,
            output_dir=os.path.dirname(args.output) or "image/batch",
            style=args.style,
            model=args.model,
            size=args.size,
            reference_image=args.reference,
            check_interval=args.interval,
            verbose=not args.quiet,
            enhance_prompt=not args.no_enhance
        )
    else:
        # 单张生成
        result = generator.generate_image(
            prompt=args.prompt,
            output_path=args.output,
            style=args.style,
            model=args.model,
            size=args.size,
            reference_image=args.reference,
            check_interval=args.interval,
            verbose=not args.quiet,
            enhance_prompt=not args.no_enhance
        )

        exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()