"""
主入口脚本 - 测试用例分析器 v1.1.0
"""

import os
import sys
import json
import argparse

# 设置控制台编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from analyze_requirement import RequirementAnalyzer
from generate_markdown import MarkdownGenerator
from generate_excel import ExcelGenerator
from evolution_manager import EvolutionManager
from document_converter import DocumentConverter


class TestCaseAnalyzer:
    """测试用例分析器主类"""

    def __init__(self):
        self.analyzer = RequirementAnalyzer()
        self.md_generator = MarkdownGenerator()
        self.excel_generator = ExcelGenerator()
        self.evolution = EvolutionManager()
        self.converter = DocumentConverter()

    def process(self, requirement_path: str, output_dir: str = None) -> dict:
        """
        处理需求文档，生成测试用例

        Args:
            requirement_path: 需求文档路径（支持多种格式）
            output_dir: 输出目录

        Returns:
            处理结果
        """
        # 检查文件格式，必要时转换
        ext = os.path.splitext(requirement_path)[1].lower()

        if ext not in ['.md', '.txt']:
            print(f"🔄 检测到非 Markdown 格式 ({ext})，正在转换...")
            try:
                requirement_text = self.converter.convert(requirement_path)
                print("✅ 文档转换成功")
            except Exception as e:
                print(f"❌ 文档转换失败: {e}")
                return {"error": str(e)}
        else:
            # 读取需求文档
            print(f"📄 读取需求文档: {requirement_path}")
            with open(requirement_path, 'r', encoding='utf-8') as f:
                requirement_text = f.read()

        # 分析需求
        print("🔍 分析需求...")
        analysis_result = self.analyzer.analyze(requirement_text)

        # 获取学习建议
        suggestions = self.evolution.get_suggestions(requirement_text)
        if suggestions:
            print(f"💡 学习建议: {len(suggestions)} 个")
            for suggestion in suggestions:
                print(f"   - {suggestion}")

        # 设置输出路径
        if output_dir is None:
            output_dir = "../output"

        title = analysis_result.get("summary", {}).get("title", "需求")
        safe_title = title.replace(" ", "_").replace("/", "_")
        timestamp = __import__('datetime').datetime.now().strftime("%Y%m%d_%H%M%S")

        # 生成 Markdown
        md_path = os.path.join(output_dir, "markdown", f"{safe_title}_测试用例_{timestamp}.md")
        print(f"📝 生成 Markdown: {md_path}")
        self.md_generator.generate(analysis_result, md_path)

        # 生成 Excel
        try:
            excel_path = os.path.join(output_dir, "excel", f"{safe_title}_测试用例_{timestamp}.xlsx")
            print(f"📊 生成 Excel: {excel_path}")
            self.excel_generator.generate(analysis_result, excel_path)
        except ImportError as e:
            print(f"⚠️  Excel 生成失败（请安装 openpyxl）: {e}")
            excel_path = None

        print("\n✅ 测试用例生成完成！")
        print(f"   - Markdown: {md_path}")
        if excel_path:
            print(f"   - Excel: {excel_path}")

        return {
            "analysis": analysis_result,
            "markdown": md_path,
            "excel": excel_path,
            "suggestions": suggestions
        }

    def collect_feedback(self, requirement_text: str) -> None:
        """
        收集用户反馈

        Args:
            requirement_text: 需求文本
        """
        print("\n" + "=" * 50)
        print("📝 帮助我们改进")
        print("=" * 50)

        from evolution_manager import collect_user_feedback

        feedback = collect_user_feedback()

        # 记录反馈
        req_type = self.analyzer._identify_requirement_type(requirement_text)
        self.evolution.record_feedback(req_type, feedback)

        # 学习遗漏的场景
        if feedback["coverage"]:
            self.evolution.learn_patterns(requirement_text, feedback["coverage"])

        print("\n✅ 感谢您的反馈！这些经验将被用于改进未来的分析质量。")


def cmd_evolve(args):
    """进化命令 - 查看和管理学习数据"""
    evolution = EvolutionManager()

    print("\n" + "=" * 50)
    print("🧬 测试用例分析器 - 进化管理")
    print("=" * 50)

    if args.summary:
        # 显示学习摘要
        print("\n📊 学习摘要\n")
        summary = evolution.summarize_learnings()
        print(summary)

    if args.patterns:
        # 显示已知模式
        print("\n🎯 已知需求模式\n")
        patterns_file = os.path.join(os.path.dirname(__file__), "../evolution.json")
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 遍历所有类别
            for category, patterns in data.get("patterns", {}).items():
                print(f"### [{category}]")
                for pattern_name, pattern_info in patterns.items():
                    keywords = pattern_info.get('priority_keywords', [])
                    scenarios = pattern_info.get('missed_scenarios', [])
                    print(f"  - {pattern_name}")
                    print(f"    关键词: {', '.join(keywords)}")
                    print(f"    场景数: {len(scenarios)}")
                print()

    if args.export:
        # 导出学习数据
        import shutil
        export_path = args.export
        evolution_file = os.path.join(os.path.dirname(__file__), "../evolution.json")
        shutil.copy2(evolution_file, export_path)
        print(f"✅ 学习数据已导出到: {export_path}")


def cmd_convert(args):
    """转换命令 - 将文档转换为 Markdown"""
    converter = DocumentConverter()

    print("\n" + "=" * 50)
    print("📄 文档转换")
    print("=" * 50)

    input_path = args.input
    output_path = args.output

    try:
        content = converter.convert(input_path, output_path)
        print(f"\n✅ 转换成功！")
        print(f"   内容长度: {len(content)} 字符")
        if output_path:
            print(f"   输出文件: {output_path}")
    except Exception as e:
        print(f"\n❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()


def cmd_batch(args):
    """批量处理命令"""
    analyzer = TestCaseAnalyzer()

    print("\n" + "=" * 50)
    print("📦 批量处理")
    print("=" * 50)

    input_dir = args.input
    output_dir = args.output or os.path.join(input_dir, "../output")

    success_count = 0
    fail_count = 0

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.md', '.txt', '.pdf', '.docx', '.pptx']:
                input_path = os.path.join(root, file)
                print(f"\n🔄 处理: {file}")

                try:
                    result = analyzer.process(input_path, output_dir)
                    if "error" not in result:
                        success_count += 1
                    else:
                        fail_count += 1
                except Exception as e:
                    print(f"   ❌ 失败: {e}")
                    fail_count += 1

    print(f"\n{'='*50}")
    print(f"✅ 批量处理完成！")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="测试用例分析器 v1.1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  分析单个文档:
    python main.py analyze examples/电商订单需求.md

  批量处理目录:
    python main.py batch ./examples -o ./output

  查看学习摘要:
    python main.py evolve --summary

  转换文档格式:
    python main.py convert document.docx -o document.md

支持的文档格式: .md, .txt, .pdf, .docx, .pptx
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析需求文档生成测试用例')
    analyze_parser.add_argument('input', help='需求文档路径')
    analyze_parser.add_argument('-o', '--output', help='输出目录')

    # evolve 命令
    evolve_parser = subparsers.add_parser('evolve', help='查看和管理学习数据')
    evolve_parser.add_argument('--summary', action='store_true', help='显示学习摘要')
    evolve_parser.add_argument('--patterns', action='store_true', help='显示已知模式')
    evolve_parser.add_argument('--export', help='导出学习数据到指定路径')

    # convert 命令
    convert_parser = subparsers.add_parser('convert', help='将文档转换为 Markdown')
    convert_parser.add_argument('input', help='输入文档路径')
    convert_parser.add_argument('-o', '--output', help='输出 Markdown 路径')

    # batch 命令
    batch_parser = subparsers.add_parser('batch', help='批量处理目录中的文档')
    batch_parser.add_argument('input', help='输入目录')
    batch_parser.add_argument('-o', '--output', help='输出目录')

    args = parser.parse_args()

    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行对应命令
    if args.command == 'analyze':
        requirement_path = args.input
        output_dir = args.output

        if not os.path.exists(requirement_path):
            print(f"❌ 错误: 文件不存在 - {requirement_path}")
            sys.exit(1)

        try:
            analyzer = TestCaseAnalyzer()
            result = analyzer.process(requirement_path, output_dir)
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    elif args.command == 'evolve':
        cmd_evolve(args)

    elif args.command == 'convert':
        cmd_convert(args)

    elif args.command == 'batch':
        if not os.path.isdir(args.input):
            print(f"❌ 错误: 目录不存在 - {args.input}")
            sys.exit(1)
        cmd_batch(args)


if __name__ == "__main__":
    main()
