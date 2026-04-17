#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solution Creator Skill 验证脚本

验证 skill 的完整性和可用性
"""

import os
import sys
from pathlib import Path

# Windows 兼容：设置输出编码为 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def validate_skill():
    """验证 skill 结构"""
    base_path = Path(__file__).parent.parent

    print("=" * 60)
    print("Solution Creator Skill 验证")
    print("=" * 60)

    # 必需文件列表
    required_files = {
        "SKILL.md": "核心技能定义文件",
        "README.md": "技能说明文档",
        "assets/product-matrix.md": "产品价值矩阵模板",
        "assets/proposal-template.md": "方案建议书模板",
        "references/matrix-guide.md": "产品矩阵填写指南",
        "references/matrix-example.md": "产品矩阵完整示例",
        "references/elevation-patterns.md": "常见需求的拔高策略库",
        "references/value-framework.md": "价值主张撰写框架",
        "references/reality-checklist.md": "实施审计详细检查清单",
    }

    print("\n检查必需文件...")
    print("-" * 60)

    all_valid = True
    for file_path, description in required_files.items():
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            status = "[OK]" if size > 0 else "[EMPTY]"
            print(f"{status} {file_path:40s} - {description}")
            if size == 0:
                all_valid = False
        else:
            print(f"[MISSING] {file_path:40s} - {description}")
            all_valid = False

    print("\n检查 SKILL.md 格式...")
    print("-" * 60)

    skill_md = base_path / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text(encoding="utf-8")
        checks = {
            "name:": "技能名称",
            "description:": "技能描述",
            "# Solution Creator": "角色定义",
            "## 工作流程": "工作流程",
            "Phase 1": "阶段1：价值锚定",
            "Phase 2": "阶段2：拔高升华",
            "Phase 3": "阶段3：实施审计",
        }

        for check, desc in checks.items():
            if check in content:
                print(f"[OK] 包含 {desc}")
            else:
                print(f"[MISSING] 缺少 {desc}")
                all_valid = False

    print("\n检查产品矩阵模板...")
    print("-" * 60)

    matrix_md = base_path / "assets" / "product-matrix.md"
    if matrix_md.exists():
        content = matrix_md.read_text(encoding="utf-8")
        required_columns = [
            "功能模块",
            "对应痛点",
            "核心价值主张",
            "竞品差异化",
            "实施依赖",
        ]

        for col in required_columns:
            if col in content:
                print(f"[OK] 包含列：{col}")
            else:
                print(f"[MISSING] 缺少列：{col}")
                all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("[OK] 验证通过！Solution Creator Skill 已准备就绪。")
        print("\n下一步：")
        print("1. 编辑 assets/product-matrix.md，填写你的产品信息")
        print("2. 使用技能：'基于这个需求生成解决方案'")
    else:
        print("[ERROR] 验证失败，请检查上述问题。")
        return 1
    print("=" * 60)

    return 0

if __name__ == "__main__":
    sys.exit(validate_skill())
