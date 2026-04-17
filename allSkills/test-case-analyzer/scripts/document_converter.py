"""
文档转换模块 - 支持多种格式转换为 Markdown
"""

import os
import subprocess
import json
from typing import Optional, Dict, Any
from pathlib import Path


class DocumentConverter:
    """文档转换器 - 将各种格式转换为 Markdown"""

    def __init__(self):
        self.supported_formats = {
            '.md': 'markdown',
            '.txt': 'text',
            '.pdf': 'pdf',
            '.docx': 'docx',
            '.doc': 'doc',
            '.pptx': 'pptx',
            '.ppt': 'ppt',
            '.xlsx': 'xlsx',
            '.xls': 'xls',
        }

    def convert(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        转换文档为 Markdown

        Args:
            input_path: 输入文档路径
            output_path: 可选的输出路径

        Returns:
            Markdown 文本内容
        """
        input_path = os.path.abspath(input_path)

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")

        ext = Path(input_path).suffix.lower()

        if ext not in self.supported_formats:
            raise ValueError(f"不支持的文件格式: {ext}")

        # 如果本身就是 Markdown 或文本，直接读取
        if ext in ['.md', '.txt']:
            with open(input_path, 'r', encoding='utf-8') as f:
                return f.read()

        # 使用 all-2md 技能转换
        return self._convert_with_all2md(input_path, output_path)

    def _convert_with_all2md(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        使用 all-2md 技能进行转换

        Args:
            input_path: 输入文档路径
            output_path: 可选的输出路径

        Returns:
            Markdown 文本内容
        """
        # 确定输出路径
        if output_path is None:
            base_name = Path(input_path).stem
            output_dir = os.path.dirname(input_path)
            output_path = os.path.join(output_dir, f"{base_name}.md")

        output_path = os.path.abspath(output_path)

        # 构建命令
        # 使用 bash 调用 all-2md 技能
        cmd = [
            'claude',
            '--skill', 'all-2md',
            '--',
            input_path,
            output_path
        ]

        try:
            print(f"🔄 正在转换: {input_path}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8'
            )

            if result.returncode == 0:
                # 读取转换后的内容
                with open(output_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"✅ 转换成功: {output_path}")
                return content
            else:
                # 如果 all-2md 不可用，尝试备用方案
                print(f"⚠️  all-2md 不可用，尝试备用转换方法")
                return self._fallback_convert(input_path, ext=Path(input_path).suffix.lower())

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"⚠️  转换超时或命令不可用: {e}")
            return self._fallback_convert(input_path, ext=Path(input_path).suffix.lower())

    def _fallback_convert(self, input_path: str, ext: str) -> str:
        """
        备用转换方法

        Args:
            input_path: 输入文档路径
            ext: 文件扩展名

        Returns:
            Markdown 文本内容
        """
        # 简单的文本提取提示
        fallback_prompt = f"""请分析以下 {ext} 文件的内容，提取其中的需求信息。

文件路径: {input_path}

请以 Markdown 格式输出：
1. 需求标题
2. 需求背景
3. 需求描述
4. 核心规则
5. 预期结果

如果无法读取文件，请说明原因。
"""

        # 返回提示信息，由上层处理
        return f"""# 需求文档转换

**原文件**: {input_path}
**格式**: {ext}

> 注意：需要手动将此文件转换为 Markdown 格式，或使用 all-2md 技能进行转换。

{fallback_prompt}
"""

    def batch_convert(self, input_dir: str, output_dir: str = None) -> Dict[str, str]:
        """
        批量转换目录中的所有支持文件

        Args:
            input_dir: 输入目录
            output_dir: 输出目录

        Returns:
            转换结果字典 {文件路径: Markdown 内容}
        """
        results = {}

        if output_dir is None:
            output_dir = os.path.join(input_dir, "converted")

        os.makedirs(output_dir, exist_ok=True)

        for root, dirs, files in os.walk(input_dir):
            for file in files:
                ext = Path(file).suffix.lower()

                if ext in self.supported_formats:
                    input_path = os.path.join(root, file)
                    rel_path = os.path.relpath(input_path, input_dir)
                    output_path = os.path.join(output_dir, f"{Path(file).stem}.md")

                    try:
                        content = self.convert(input_path, output_path)
                        results[rel_path] = {
                            'status': 'success',
                            'content': content,
                            'output': output_path
                        }
                    except Exception as e:
                        results[rel_path] = {
                            'status': 'error',
                            'error': str(e)
                        }

        return results

    def get_supported_formats(self) -> Dict[str, str]:
        """获取支持的文件格式"""
        return self.supported_formats.copy()

    def is_supported(self, file_path: str) -> bool:
        """检查文件格式是否支持"""
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_formats


# 便捷函数
def convert_document(input_path: str, output_path: str = None) -> str:
    """
    便捷函数：转换文档为 Markdown

    Args:
        input_path: 输入文档路径
        output_path: 可选的输出路径

    Returns:
        Markdown 文本内容
    """
    converter = DocumentConverter()
    return converter.convert(input_path, output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python document_converter.py <文件路径> [输出路径]")
        print("\n支持的格式:")
        converter = DocumentConverter()
        for ext, name in converter.get_supported_formats().items():
            print(f"  {ext} - {name}")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        content = convert_document(input_file, output_file)
        print(f"\n📄 转换完成，内容长度: {len(content)} 字符")

        if output_file:
            print(f"💾 输出文件: {output_file}")
        else:
            print(f"\n{'='*50}")
            print(content[:500] + "..." if len(content) > 500 else content)

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
