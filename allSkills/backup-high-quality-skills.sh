#!/bin/bash
# 高质量技能备份脚本
# 检查时间: 2026-04-18 06:27:02

SOURCE_DIR="D:/ProjectAI/CC/CC_record/skills"
BACKUP_DIR="D:/ProjectAI/CC/workSpace/skills-backup"
GITHUB_USER="chengrp"
REPO_NAME="workSpace"

# 高质量技能列表 (19个，评分≥80分)
HIGH_QUALITY_SKILLS=(
    "all-2md"
    "huashu-slides"
    "hv-analysis"
    "image-assistant"
    "info-graphic"
    "knowledge-site-creator"
    "life-reset"
    "ms-image"
    "notebooklm"
    "req-change-workflow"
    "req-record"
    "skill-creator"
    "skill-hud"
    "solution-creator"
    "web-access"
    "wechat-article-formatter"
    "wechat-product-manager-writer"
    "wechat-tech-writer"
    "zhang-xiaolong-perspective"
)

echo "=== 高质量技能备份脚本 ==="
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 复制高质量技能
echo "正在复制高质量技能..."
for skill in "${HIGH_QUALITY_SKILLS[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        echo "✓ 复制: $skill"
        cp -r "$SOURCE_DIR/$skill" "$BACKUP_DIR/"
    else
        echo "✗ 跳过: $skill (目录不存在)"
    fi
done

echo ""
echo "=== 复制完成 ==="
echo "备份位置: $BACKUP_DIR"
echo "技能数量: ${#HIGH_QUALITY_SKILLS[@]}"
echo ""

# 统计信息
echo "=== 备份统计 ==="
echo "总大小: $(du -sh "$BACKUP_DIR" | cut -f1)"
echo "文件数量: $(find "$BACKUP_DIR" -type f | wc -l)"
echo ""

# 推送到 GitHub (可选)
read -p "是否推送到 GitHub? (y/n): " push_to_github

if [ "$push_to_github" = "y" ]; then
    echo ""
    echo "正在推送到 GitHub..."

    # 初始化 Git 仓库
    cd "$BACKUP_DIR"
    git init
    git add .
    git commit -m "Add high-quality skills backup (19 skills, ≥80 score)"

    # 添加远程仓库
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"

    # 推送到新分支
    git branch -M skills-backup
    git push -u origin skills-backup

    echo ""
    echo "✓ 推送完成!"
    echo "仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME/tree/skills-backup"
fi

echo ""
echo "=== 脚本执行完成 ==="
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
