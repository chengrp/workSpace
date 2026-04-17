#!/usr/bin/env python3
"""
mcp-chrome 使用演示脚本
演示如何直接调用 mcp-chrome 工具
"""

import json
import subprocess
import sys

def call_mcp_chrome_tool(method, params=None, tool_name=None, tool_args=None):
    """
    调用 mcp-chrome 工具

    Args:
        method: MCP 方法名，如 "tools/call" 或 "tools/list"
        params: 方法参数
        tool_name: 工具名称（仅用于 tools/call）
        tool_args: 工具参数（仅用于 tools/call）
    """
    # 构建请求
    request_id = 1

    if method == "tools/call" and tool_name:
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": {
                "name": tool_name,
                "arguments": tool_args or {}
            },
            "id": request_id
        }
    else:
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": request_id
        }

    # 转换为 JSON 字符串
    request_json = json.dumps(request, ensure_ascii=False)

    # 调用 mcp-chrome-bridge
    cmd = [
        "node",
        "C:\\Users\\RyanCh\\AppData\\Roaming\\npm\\node_modules\\mcp-chrome-bridge\\dist\\mcp\\mcp-server-stdio.js"
    ]

    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            input=request_json.encode('utf-8'),
            capture_output=True,
            timeout=10
        )

        if result.returncode == 0:
            response = json.loads(result.stdout.decode('utf-8'))
            return response.get("result")
        else:
            print(f"错误: {result.stderr.decode('utf-8')}")
            return None

    except Exception as e:
        print(f"调用失败: {e}")
        return None

def demo_get_windows_and_tabs():
    """演示：获取所有窗口和标签页"""
    print("=== 演示: 获取所有窗口和标签页 ===")
    result = call_mcp_chrome_tool("tools/call", tool_name="get_windows_and_tabs")

    if result:
        print(f"窗口数量: {result.get('windowCount', 0)}")
        print(f"标签页数量: {result.get('tabCount', 0)}")

        windows = result.get('windows', [])
        for i, window in enumerate(windows):
            print(f"\n窗口 {i+1} (ID: {window.get('windowId')}):")
            tabs = window.get('tabs', [])
            for j, tab in enumerate(tabs):
                active = "✓" if tab.get('active') else " "
                print(f"  {active} 标签页 {j+1}: {tab.get('title', '无标题')}")
                print(f"      URL: {tab.get('url', '无URL')}")
    else:
        print("获取失败")

def demo_navigate_to_url(url="https://www.baidu.com"):
    """演示：导航到指定URL"""
    print(f"\n=== 演示: 导航到 {url} ===")
    result = call_mcp_chrome_tool(
        "tools/call",
        tool_name="chrome_navigate",
        tool_args={"url": url}
    )

    if result:
        print(f"导航结果: {result}")
    else:
        print("导航失败")

def demo_get_web_content(url=None):
    """演示：获取网页内容"""
    print("\n=== 演示: 获取网页内容 ===")

    args = {"textContent": True}
    if url:
        args["url"] = url

    result = call_mcp_chrome_tool(
        "tools/call",
        tool_name="chrome_get_web_content",
        tool_args=args
    )

    if result:
        content = result.get('content', '')
        print(f"获取到内容长度: {len(content)} 字符")
        if content:
            # 显示前200个字符
            preview = content[:200].replace('\n', ' ')
            print(f"内容预览: {preview}...")
    else:
        print("获取内容失败")

def demo_list_all_tools():
    """演示：列出所有可用工具"""
    print("=== 演示: 列出所有可用工具 ===")
    result = call_mcp_chrome_tool("tools/list")

    if result:
        tools = result.get('tools', [])
        print(f"可用工具数量: {len(tools)}")

        # 按类别分组显示
        categories = {
            "浏览器管理": ["get_windows_and_tabs", "chrome_navigate", "chrome_close_tabs",
                        "chrome_go_back_or_forward", "chrome_switch_tab"],
            "截图功能": ["chrome_screenshot"],
            "内容分析": ["chrome_get_web_content", "chrome_get_interactive_elements",
                       "search_tabs_content", "chrome_console"],
            "交互操作": ["chrome_click_element", "chrome_fill_or_select", "chrome_keyboard"],
            "网络监控": ["chrome_network_request", "chrome_network_debugger_start",
                       "chrome_network_debugger_stop", "chrome_network_capture_start",
                       "chrome_network_capture_stop"],
            "数据管理": ["chrome_history", "chrome_bookmark_search", "chrome_bookmark_add",
                       "chrome_bookmark_delete"],
            "脚本注入": ["chrome_inject_script", "chrome_send_command_to_inject_script"]
        }

        for category, tool_names in categories.items():
            category_tools = [t for t in tools if t['name'] in tool_names]
            if category_tools:
                print(f"\n{category}:")
                for tool in category_tools:
                    print(f"  • {tool['name']}: {tool['description']}")
    else:
        print("获取工具列表失败")

def main():
    """主函数"""
    print("=" * 60)
    print("mcp-chrome 工具调用演示")
    print("=" * 60)

    # 1. 列出所有工具
    demo_list_all_tools()

    # 2. 获取当前窗口和标签页
    demo_get_windows_and_tabs()

    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n其他可用工具示例:")
    print("1. chrome_screenshot - 截图当前页面")
    print("2. chrome_history - 查看浏览历史")
    print("3. chrome_bookmark_search - 搜索书签")
    print("4. chrome_click_element - 点击页面元素")
    print("5. chrome_fill_or_select - 填写表单")

    print("\n在 Claude Code 中直接使用自然语言命令，例如:")
    print("  • '打开百度首页'")
    print("  • '截图当前页面'")
    print("  • '搜索我的浏览历史'")

    print("\n要测试导航功能，可以运行:")
    print("  demo_navigate_to_url('https://www.baidu.com')")
    print("  demo_get_web_content()")

if __name__ == "__main__":
    main()