# 微信群分析报告索引

本目录包含所有通过 wx-group-analysis Skill 生成的群分析报告。

## 报告类型

| 报告类型 | 说明 | 模板 |
|----------|------|------|
| 群日报 | 日度运营监控 | [daily-report-template.md](../templates/daily-report-template.md) |
| 成员贡献榜 | 成员激励体系 | [member-ranking-template.md](../templates/member-ranking-template.md) |
| 内容质量报告 | 内容运营优化 | [content-quality-template.md](../templates/content-quality-template.md) |
| 成员成长报告 | 成员运营分析 | [member-growth-template.md](../templates/member-growth-template.md) |
| 综合月报 | 决策层汇报 | - |

## 报告列表

### 按时间排序

| 文件名 | 报告类型 | 群名 | 时间范围 | 生成时间 |
|--------|----------|------|----------|----------|
| 2026-04-09-daily-report-【AI登山社】.md | 群日报 | AI 登山社 | 2026-04-09 | 2026-04-09 |
| 2026-04-07-to-2026-04-09-member-ranking-【AI登山社】.md | 成员贡献榜 | AI 登山社 | 2026-04-07 ~ 2026-04-09 | 2026-04-09 |
| 2026-04-07-to-2026-04-09-content-quality-【AI登山社】.md | 内容质量报告 | AI 登山社 | 2026-04-07 ~ 2026-04-09 | 2026-04-09 |
| 2026-04-07-to-2026-04-09-member-growth-【AI登山社】.md | 成员成长报告 | AI 登山社 | 2026-04-07 ~ 2026-04-09 | 2026-04-09 |

---

## 快速查看

### 查看最新报告

```bash
# 查看最新的群日报
ls -t ~/wx-group-analysis/reports/*daily-report*.md | head -1 | xargs cat

# 查看最新的成员贡献榜
ls -t ~/wx-group-analysis/reports/*member-ranking*.md | head -1 | xargs cat

# 查看所有报告
ls -la ~/wx-group-analysis/reports/
```

### 搜索特定群的报告

```bash
# 搜索 AI 登山社 的所有报告
ls ~/wx-group-analysis/reports/*【AI登山社】*.md

# 搜索特定类型的所有报告
ls ~/wx-group-analysis/reports/*daily-report*.md
```

---

_本索引由 wx-group-analysis Skill 自动维护_
_最后更新: 2026-04-09_
