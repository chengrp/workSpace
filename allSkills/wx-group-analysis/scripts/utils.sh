#!/bin/bash
# wx-group-analysis 工具函数库

# 获取当前日期时间
get_current_date() {
    date +%Y-%m-%d
}

# 获取周几
get_weekday() {
    date +%u | awk '{
        days["1"]="周一"; days["2"]="周二"; days["3"]="周三";
        days["4"]="周四"; days["5"]="周五"; days["6"]="周六"; days["7"]="周日";
        print days[$1];
    }'
}

# 解析时间范围，返回开始和结束日期
parse_time_range() {
    local time_input="$1"
    local start_date=""
    local end_date=""

    case "$time_input" in
        "今天")
            start_date=$(date +%Y-%m-%d)
            end_date=$(date +%Y-%m-%d)
            ;;
        "昨天")
            start_date=$(date -d "yesterday" +%Y-%m-%d)
            end_date=$(date -d "yesterday" +%Y-%m-%d)
            ;;
        "本周"|"这周")
            # 获取本周一
            start_date=$(date -d "monday" +%Y-%m-%d)
            end_date=$(date +%Y-%m-%d)
            ;;
        "上周")
            # 获取上周一
            start_date=$(date -d "last monday" +%Y-%m-%d)
            end_date=$(date -d "last sunday" +%Y-%m-%d)
            ;;
        "本月"|"这个月")
            start_date=$(date +%Y-%m-01)
            end_date=$(date +%Y-%m-%d)
            ;;
        "上月"|"上个月")
            start_date=$(date -d "$(date +%Y-%m-01) -1 month" +%Y-%m-%d)
            end_date=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m-%d)
            ;;
        *)
            # 尝试解析具体日期或范围
            if echo "$time_input" | grep -qE "^\d{4}-\d{2}-\d{2}$"; then
                start_date="$time_input"
                end_date="$time_input"
            elif echo "$time_input" | grep -qE "最近(\d+)天"; then
                days=$(echo "$time_input" | grep -oP "最近\K\d+")
                start_date=$(date -d "$days days ago" +%Y-%m-%d)
                end_date=$(date +%Y-%m-%d)
            else
                # 默认本周
                start_date=$(date -d "monday" +%Y-%m-%d)
                end_date=$(date +%Y-%m-%d)
            fi
            ;;
    esac

    echo "$start_date|$end_date"
}

# 检查 wechat-cli 是否安装
check_wechat_cli() {
    if ! command -v wechat-cli &> /dev/null; then
        echo "❌ wechat-cli 未安装"
        echo ""
        echo "安装方法："
        echo "npm install -g @canghe_ai/wechat-cli"
        return 1
    fi

    if [ ! -f ~/.wechat-cli/config.json ]; then
        echo "❌ wechat-cli 未初始化"
        echo ""
        echo "初始化方法："
        echo "wechat-cli init"
        return 1
    fi

    return 0
}

# 获取群列表（用于匹配）
get_groups_list() {
    wechat-cli sessions --limit 100 --format text 2>/dev/null | \
    grep -oP "\[.*?\] \K[^[]+(?=\[)" | \
    sed 's/ (.*//g' | \
    sort | uniq
}

# 匹配群名称
match_group_name() {
    local keyword="$1"
    local groups=$(get_groups_list)

    # 先尝试精确匹配
    local exact_match=$(echo "$groups" | grep -ix "$keyword" | head -1)
    if [ -n "$exact_match" ]; then
        echo "$exact_match"
        return 0
    fi

    # 尝试模糊匹配
    local fuzzy_match=$(echo "$groups" | grep -i "$keyword" | head -1)
    if [ -n "$fuzzy_match" ]; then
        echo "$fuzzy_match"
        return 0
    fi

    return 1
}

# 获取聊天记录
get_chat_history() {
    local group_name="$1"
    local start_date="$2"
    local end_date="$3"
    local limit="${4:-1000}"

    wechat-cli history "$group_name" \
        --start-time "$start_date" \
        --end-time "$end_date" \
        --limit "$limit" \
        --format text
}

# 获取统计数据
get_chat_stats() {
    local group_name="$1"
    local start_date="$2"
    local end_date="$3"

    wechat-cli stats "$group_name" \
        --start-time "$start_date" \
        --end-time "$end_date" \
        --format text
}

# 统计发言排行（从聊天记录）
count_speakers() {
    local history_file="$1"

    grep -oP "(?<=^\[2026-\d{2}-\d{2} \d{2}:\d{2}\] ).+?(?=: )" "$history_file" | \
        sort | uniq -c | sort -rn
}

# 统计链接分享
count_link_shares() {
    local history_file="$1"

    grep -E "\[链接\]|\[链接/文件\]" "$history_file" | \
        grep -oP "(?<=^\[2026-\d{2}-\d{2} \d{2}:\d{2}\] ).+?(?=: )" | \
        sort | uniq -c | sort -rn
}

# 统计被回复次数
count_replies() {
    local history_file="$1"

    grep "↳ 回复" "$history_file" | \
        grep -oP "↳ 回复 \K[^:]+" | \
        sort | uniq -c | sort -rn
}

# 计算综合得分（归一化处理）
calculate_score() {
    local activity=$1  # 发言数
    local sharing=$2   # 链接数
    local interaction=$3 # 被回复数
    local work_hours=$4  # 工作时段发言数

    # 这里需要传入最大值进行归一化
    # 实际使用时需要先获取各项的最大值
    # score = (activity/max_activity * 0.4) + (sharing/max_sharing * 0.25) + (interaction/max_interaction * 0.2) + (work_hours/max_work_hours * 0.15)
}

# 创建报告目录
ensure_reports_dir() {
    local reports_dir="$HOME/wx-group-analysis/reports"
    mkdir -p "$reports_dir"
    echo "$reports_dir"
}

# 生成报告文件名
generate_report_filename() {
    local report_type="$1"
    local group_name="$2"
    local start_date="$3"
    local end_date="$4"

    # 清理群名中的特殊字符
    local clean_name=$(echo "$group_name" | sed 's/[][]//g' | sed 's/【/[/g' | sed 's/】/]/g' | sed 's/ /_/g')

    echo "${start_date}-to-${end_date}-${report_type}-${clean_name}.md"
}

# 显示报告生成成功信息
show_success_message() {
    local report_file="$1"

    echo "✅ 报告生成成功！"
    echo ""
    echo "📄 文件位置: $report_file"
    echo ""
    echo "查看报告："
    echo "cat \"$report_file\""
    echo ""
    echo "或用编辑器打开："
    echo "code \"$report_file\""
}
