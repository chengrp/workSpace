# 微信公众号文章存档

此目录用于存放由 `wechat-product-manager-writer` 技能生成的所有公众号文章。

## 目录结构

```
Article/
├── {文章主题}/
│   ├── {文章主题}.md      # 文章正文
│   ├── cover.png          # 封面图
│   └── structure.png      # 内容结构图
└── README.md              # 本文件
```

## 使用说明

当使用 `wechat-product-manager-writer` 技能生成新文章时，所有文件将自动保存到此目录下的对应子文件夹中。

### 文件命名规则

- 子目录名称：文章主题（如 `影刀RPA产品拆解`）
- Markdown 文件：与子目录同名
- 封面图：固定为 `cover.png`
- 结构图：固定为 `structure.png`

### 示例

```
Article/
├── 影刀RPA产品拆解/
│   ├── 影刀RPA产品拆解.md
│   ├── cover.png
│   └── structure.png
└── Cursor产品拆解/
    ├── Cursor产品拆解.md
    ├── cover.png
    └── structure.png
```

## 文章类型

本技能支持生成以下类型的公众号文章：

1. **AI 产品拆解** - 分析产品设计逻辑、商业模式
2. **场景解决方案** - 用 AI 解决具体业务问题
3. **效率提升实战** - 工具使用技巧和工作流优化
4. **产品方法论** - AI 时代产品经理的思维方式
5. **行业观察** - 新产品、新趋势的产品化解读

---

**注意**：此目录由 `wechat-product-manager-writer` 技能自动管理，请勿手动修改文件结构。
