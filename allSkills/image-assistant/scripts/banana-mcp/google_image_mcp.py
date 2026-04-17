#!/usr/bin/env python3
"""
Google Image Generation MCP Server
使用 Google AI Studio API 生成图片
"""

import asyncio
import base64
import json
import os
import sys
from pathlib import Path
from typing import Any

# 尝试导入 mcp 相关包，如果没有安装则提示
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("错误: 需要安装 mcp 包", file=sys.stderr)
    print("请运行: pip install mcp", file=sys.stderr)
    sys.exit(1)

import httpx


# 从环境变量获取 API Key
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    print("警告: 未设置 GOOGLE_API_KEY 环境变量", file=sys.stderr)
    print("请设置: export GOOGLE_API_KEY='your-key'", file=sys.stderr)

# 创建 MCP server
server = Server("google-image-generator")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出生图工具"""
    return [
        Tool(
            name="generate_image",
            description="使用 Google AI Studio 生成图片。支持多种模型如 gemini-3-pro-image-preview 和 imagen-3.0。",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "图片生成提示词（描述你想要生成的图片内容）"
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "输出文件名（如: image.png）"
                    },
                    "model": {
                        "type": "string",
                        "description": "模型名称（可选）: gemini-3-pro-image-preview (默认) 或 imagen-3.0-generate-001",
                        "default": "gemini-3-pro-image-preview"
                    },
                    "aspect_ratio": {
                        "type": "string",
                        "description": "宽高比（可选）: 16:9, 9:16, 1:1 等",
                        "default": "1:1"
                    }
                },
                "required": ["prompt", "output_filename"]
            }
        )
    ]


async def generate_with_gemini_multimodal(
    prompt: str,
    model: str = "gemini-3-pro-image-preview"
) -> bytes:
    """使用 Gemini 多模态模型生成图片"""
    # 动态获取 API Key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("未设置 GOOGLE_API_KEY 环境变量")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    # 构建请求
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    # 添加 API Key 到 URL
    params = {"key": api_key}

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers,
            params=params
        )
        response.raise_for_status()
        result = response.json()

    # 提取图片数据
    try:
        candidates = result.get("candidates", [])
        if candidates and candidates[0]:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                inline_data = part.get("inlineData", {})
                if inline_data and "data" in inline_data:
                    return base64.b64decode(inline_data["data"])
    except Exception as e:
        raise ValueError(f"无法从响应中提取图片: {e}")

    raise ValueError("响应中未找到图片数据")


async def generate_with_imagen(
    prompt: str,
    model: str = "imagen-3.0-generate-001",
    aspect_ratio: str = "1:1"
) -> bytes:
    """使用 Imagen 模型生成图片（通过 AI SDK 风格的 API）"""
    # 动态获取 API Key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("未设置 GOOGLE_API_KEY 环境变量")

    # 使用 OpenAI 兼容端点
    url = "https://generativelanguage.googleapis.com/v1beta/openai/images/generations"

    payload = {
        "model": model,
        "prompt": prompt,
        "response_format": "b64_json",
        "n": 1,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()

    # 提取图片数据
    try:
        data = result.get("data", [])
        if data and data[0]:
            b64_json = data[0].get("b64_json")
            if b64_json:
                return base64.b64decode(b64_json)
    except Exception as e:
        raise ValueError(f"无法从响应中提取图片: {e}")

    raise ValueError("响应中未找到图片数据")


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """处理工具调用"""
    if name != "generate_image":
        raise ValueError(f"未知工具: {name}")

    prompt = arguments.get("prompt")
    output_filename = arguments.get("output_filename")
    model = arguments.get("model", "gemini-3-pro-image-preview")
    aspect_ratio = arguments.get("aspect_ratio", "1:1")

    if not prompt:
        return [TextContent(type="text", text="错误: prompt 参数是必需的")]
    if not output_filename:
        return [TextContent(type="text", text="错误: output_filename 参数是必需的")]

    if not API_KEY:
        return [TextContent(type="text", text="错误: 未设置 GOOGLE_API_KEY 环境变量")]

    try:
        # 添加宽高比到 prompt
        full_prompt = f"{prompt} Aspect ratio: {aspect_ratio}."

        # 根据模型选择生成方式
        if "imagen" in model.lower():
            image_bytes = await generate_with_imagen(full_prompt, model, aspect_ratio)
        else:
            image_bytes = await generate_with_gemini_multimodal(full_prompt, model)

        # 保存图片 - 默认到 image 文件夹
        script_dir = Path(__file__).parent
        image_dir = script_dir / "image"
        image_dir.mkdir(parents=True, exist_ok=True)

        output_path = image_dir / output_filename
        output_path.write_bytes(image_bytes)

        return [TextContent(
            type="text",
            text=f"✅ 图片已成功生成并保存到: {output_path.absolute()}\n"
                f"模型: {model}\n"
                f"宽高比: {aspect_ratio}\n"
                f"文件大小: {len(image_bytes)} 字节"
        )]

    except httpx.HTTPStatusError as e:
        error_text = e.response.text
        return [TextContent(
            type="text",
            text=f"❌ HTTP 错误: {e.response.status_code}\n详情: {error_text}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 生成失败: {str(e)}"
        )]


async def main():
    """启动 MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
