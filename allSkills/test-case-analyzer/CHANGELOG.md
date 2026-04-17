# 变更日志

## [1.0.0] - 2026-02-28

### 新增
- ✨ 初始版本发布
- ✨ 五维度需求分析框架
- ✨ Markdown + Excel 双格式输出
- ✨ 学习进化机制
- ✨ 行业测试模式库（电商、金融、通用）
- ✨ 示例需求文档

### 功能
- 需求文档智能分析
- 分层测试用例生成（功能/边界/状态/回归/交互/配置）
- 待确认事项自动提取
- 反馈收集与学习

### 文档
- SKILL.md - 技能主文档
- README.md - 使用说明
- DESIGN.md - 设计文档

---

## [1.0.0] - 2026-02-28 - 完整实现 ✅

### 实现
- ✅ Markdown 生成脚本实现
- ✅ Excel 生成脚本实现（支持4个工作表）
- ✅ 进化管理器脚本实现
- ✅ 主入口脚本实现
- ✅ 完整的工作流集成

### 技术实现
- `MarkdownGenerator` - 结构化Markdown输出
- `ExcelGenerator` - 使用openpyxl创建专业Excel表格
- `EvolutionManager` - 反馈收集与学习机制
- `TestCaseAnalyzer` - 主入口类，整合所有组件

### 文件结构
```
scripts/
├── analyze_requirement.py   # 需求分析引擎
├── generate_markdown.py     # Markdown生成器
├── generate_excel.py        # Excel生成器
├── evolution_manager.py     # 进化管理器
└── main.py                  # 主入口脚本
```

---

## [1.1.0] - 2026-02-28 - 增强版 ✅

### 新增功能
- ✨ **文档转换模块** - 支持 PDF/DOCX/PPTX/XLSX 等多种格式自动转换为 Markdown
- ✨ **命令行界面升级** - 新增多命令支持 (analyze/evolve/convert/batch)
- ✨ **模式自动匹配** - 基于学习数据自动识别需求类型并应用对应测试模式
- ✨ **进化命令** - `/evolve` 命令查看学习摘要、导出学习数据
- ✨ **批量处理** - 支持批量处理整个目录的需求文档
- ✨ **测试场景扩展** - 从学习模式中自动补充测试场景

### 技术实现
- `DocumentConverter` - 文档格式转换器
- 命令行参数解析 (argparse)
- 模式自动匹配算法
- 增强的测试用例生成逻辑

### 新增命令
```bash
# 分析单个文档
python main.py analyze <文档路径>

# 查看学习摘要
python main.py evolve --summary

# 转换文档格式
python main.py convert <文档路径> -o <输出路径>

# 批量处理目录
python main.py batch <目录> -o <输出目录>
```

### 支持的输入格式
- Markdown (.md)
- 纯文本 (.txt)
- PDF (.pdf)
- Word 文档 (.docx, .doc)
- PowerPoint (.pptx, .ppt)
- Excel (.xlsx, .xls)

---

## 规划中的功能

### [1.2.0] - 计划中
- [ ] 测试用例导入模板
- [ ] Node.js 备用脚本
- [ ] 行业模式库扩展
- [ ] 测试数据自动生成
- [ ] 用例优先级自动评估

---

## 版本说明

- **Major.Minor.Patch**
  - Major: 重大功能变更
  - Minor: 新增功能
  - Patch: Bug 修复
