#!/bin/bash
#
# Tavily 搜索封装脚本
#
# 用法:
#   ./search.sh "搜索关键词" [选项]
#
# 选项:
#   --topic <type>     搜索类型：general（默认）或 news
#   --max <number>     最大结果数（默认：5）
#   --depth <level>    搜索深度：basic（默认）或 advanced
#   --help, -h         显示帮助
#

# ===========================================
# 功能 1: 自动配置代理
# ===========================================
configure_proxy() {
    # 如果已配置代理，跳过
    if [ -n "$http_proxy" ] && [ -n "$https_proxy" ]; then
        return 0
    fi

    # 尝试从 resolv.conf 获取网关 IP 作为代理
    if [ -f /etc/resolv.conf ]; then
        local host_ip
        host_ip=$(grep nameserver /etc/resolv.conf 2>/dev/null | awk '{print $2}' | head -1)

        if [ -n "$host_ip" ]; then
            export http_proxy="http://${host_ip}:7890"
            export https_proxy="http://${host_ip}:7890"
            export HTTP_PROXY="http://${host_ip}:7890"
            export HTTPS_PROXY="http://${host_ip}:7890"
        fi
    fi
}

# ===========================================
# 功能 2: 自动获取 API 密钥
# ===========================================
get_api_key() {
    # 优先级：1. 环境变量  2. 本地 .env 文件  3. OpenClaw 配置文件
    if [ -n "$TAVILY_API_KEY" ]; then
        return 0
    fi

    # 尝试从脚本所在目录的 .env 文件读取
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local env_file="$script_dir/.env"
    if [ -f "$env_file" ]; then
        TAVILY_API_KEY=$(grep "^TAVILY_API_KEY=" "$env_file" | cut -d'=' -f2)
    fi

    # 如果 .env 没有，尝试 OpenClaw 配置
    if [ -z "$TAVILY_API_KEY" ]; then
        local config_file="$HOME/.openclaw/openclaw.json"
        if [ -f "$config_file" ]; then
            # 精确匹配 web.search.apiKey
            TAVILY_API_KEY=$(grep -A1 '"search"' "$config_file" 2>/dev/null | grep '"apiKey"' | head -1 | sed 's/.*"apiKey"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
        fi
    fi

    if [ -z "$TAVILY_API_KEY" ]; then
        echo "错误：未设置 Tavily API 密钥" >&2
        echo "" >&2
        echo "配置方法：" >&2
        echo "  1. 在脚本目录创建 .env 文件：TAVILY_API_KEY=tvly-your-key" >&2
        echo "  2. 或设置环境变量：export TAVILY_API_KEY=tvly-your-key" >&2
        echo "  3. 或使用 OpenClaw：openclaw config set tools.web.search.apiKey \"tvly-your-key\"" >&2
        exit 1
    fi

    # 功能 3: 密钥格式预验证
    if [[ ! "$TAVILY_API_KEY" =~ ^tvly- ]]; then
        echo "警告：API 密钥格式可能不正确（应以 tvly- 开头）" >&2
        echo "当前密钥前缀：${TAVILY_API_KEY:0:10}..." >&2
    fi
}

# ===========================================
# 功能 4: 改进错误提示
# ===========================================
parse_error() {
    local response="$1"
    local http_code="$2"

    # HTTP 级别错误
    if [ -n "$http_code" ] && [ "$http_code" != "200" ]; then
        case "$http_code" in
            401) echo "认证失败：API 密钥无效或过期" ;;
            403) echo "权限不足：检查 API 密钥配额" ;;
            404) echo "API 端点不存在" ;;
            429) echo "请求超限：达到速率限制" ;;
            500) echo "服务器错误：Tavily 服务暂时不可用" ;;
            502|503|504) echo "网关错误：网络连接问题" ;;
            *) echo "HTTP 错误：状态码 $http_code" ;;
        esac
        return 1
    fi

    # API 返回的错误
    if echo "$response" | grep -q '"error"'; then
        local error_msg
        error_msg=$(echo "$response" | grep -o '"message"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | cut -d'"' -f4)

        if [ -n "$error_msg" ]; then
            echo "API 错误：$error_msg"
        else
            echo "API 返回错误响应"
        fi
        return 1
    fi

    return 0
}

# ===========================================
# 主程序
# ===========================================

# 默认参数
QUERY=""
TOPIC="general"
MAX_RESULTS=5
SEARCH_DEPTH="basic"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --topic)
            TOPIC="$2"
            shift 2
            ;;
        --max)
            MAX_RESULTS="$2"
            shift 2
            ;;
        --depth)
            SEARCH_DEPTH="$2"
            shift 2
            ;;
        --help|-h)
            echo "Tavily 搜索工具"
            echo ""
            echo "用法:"
            echo "  $0 \"搜索关键词\" [选项]"
            echo ""
            echo "选项:"
            echo "  --topic <type>     搜索类型：general（默认）或 news"
            echo "  --max <number>     最大结果数（默认：5）"
            echo "  --depth <level>    搜索深度：basic（默认）或 advanced"
            echo "  --help, -h         显示帮助"
            echo ""
            echo "示例:"
            echo "  $0 \"AI 技术突破\""
            echo "  $0 \"科技新闻\" --topic news --max 10"
            exit 0
            ;;
        -*)
            echo "未知选项：$1" >&2
            echo "使用 --help 查看用法" >&2
            exit 1
            ;;
        *)
            if [ -z "$QUERY" ]; then
                QUERY="$1"
            fi
            shift
            ;;
    esac
done

# 检查查询词
if [ -z "$QUERY" ]; then
    echo "错误：请提供搜索关键词" >&2
    echo "使用 --help 查看用法" >&2
    exit 1
fi

# 获取 API 密钥
get_api_key

# 配置代理
configure_proxy

# 调用 API
TEMP_FILE=$(mktemp)
HTTP_CODE=$(curl -s -w "%{http_code}" -o "$TEMP_FILE" -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$TAVILY_API_KEY\",
    \"query\": \"$QUERY\",
    \"search_depth\": \"$SEARCH_DEPTH\",
    \"max_results\": $MAX_RESULTS,
    \"topic\": \"$TOPIC\"
  }")

RESPONSE=$(cat "$TEMP_FILE")
rm -f "$TEMP_FILE"

# 检查错误
ERROR_MSG=$(parse_error "$RESPONSE" "$HTTP_CODE")
if [ $? -ne 0 ]; then
    echo "搜索失败：$ERROR_MSG" >&2

    # 显示调试信息
    if [ "$HTTP_CODE" != "200" ]; then
        echo "调试信息：HTTP 状态码 $HTTP_CODE" >&2
    fi

    exit 1
fi

# 格式化输出
echo "搜索：$QUERY"
echo ""

if command -v jq &> /dev/null; then
    RESULT_COUNT=$(echo "$RESPONSE" | jq -r '.results | length' 2>/dev/null || echo "0")
    echo "找到 $RESULT_COUNT 条结果"
    echo "═══════════════════════════════════════"
    echo ""

    echo "$RESPONSE" | jq -r '
      .results[] |
        "📌 \(.title)\n",
        "🔗 \(.url)\n",
        "📝 \(.content)\n",
        "⭐ 评分：\(.score)\n",
        "═══════════════════════════════════════\n"
    ' 2>/dev/null
else
    # 简单输出模式（无 jq）
    echo "$RESPONSE" | grep -o '"title":"[^"]*"' | cut -d'"' -f4 | while read -r title; do
        echo "📌 $title"
    done
    echo ""
    echo "$RESPONSE" | grep -o '"url":"[^"]*"' | cut -d'"' -f4 | while read -r url; do
        echo "🔗 $url"
    done
fi
