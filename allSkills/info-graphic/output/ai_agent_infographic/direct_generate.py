#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接调用 Google AI 生成信息图
"""
import os
import sys
import base64
import urllib.request
import urllib.parse
import json
import time

# 设置 UTF-8 编码输出
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
env_path = "d:/ProjectAI/CC/CC_record/skills/all-image/.env"
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

# API 配置
API_KEY = os.getenv("ALL_IMAGE_GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("ALL_IMAGE_GOOGLE_MODEL", "gemini-3-pro-image-preview")
BASE_URL = os.getenv("ALL_IMAGE_GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")

if not API_KEY:
    print("❌ 错误: 未设置 GOOGLE_API_KEY")
    sys.exit(1)

# 提示词
prompt = '''当智能不再稀缺 - 时代变革账单

Create a high-density infographic in Receipt Ticket Aesthetic style (打印热敏纸风).

=== CONTENT (7 modules) ===
TITLE: 当智能不再稀缺 - 时代变革账单

Module 01: IBM暴跌13% - 一天蒸发310亿美元，认知劳动边际成本趋零的信号
Module 02: 六把刀理论 - DAU失效、平台化路径断裂、SaaS转向2A、AI应用概念错误、注意力经济过时、出海概念消亡
Module 03: 奇点推演 - 智能可无限生产，200美金就能买到CEO级能力，窗口正在关闭
Module 04: 三层社会 - 第一层算力拥有者(定义规则)、第二层算力驱动者(调度Agent)、第三层算力依附者(被边缘化)
Module 05: 变化信号 - Obsidian CLI发布、EvoMap进化型系统、Agent雇佣人类、企业减员增效引入AI
Module 06: 行动清单 - 重新审视可替代性、学会驱动Agent协作、关注算力和能源分布、创业做新世界基建、教育重心转移
Module 07: 金句收尾 - "悲观者是远见，乐观者才是智慧"

=== STYLE: Receipt Ticket Aesthetic ===
- Receipt format vertical layout with perforated edges on both sides
- 3D/Claymorphism rendered icons (currency, charts, AI chip, social hierarchy, signal lights)
- Monospace/pixel font headers (retro digital receipt printer style)
- Clean sans-serif body text with high readability
- White/Off-white thermal paper texture background
- Colors: Pure black text, Cyan accents #00AEEF, Yellow highlights #FFD100, Orange call-to-action #FF6B35
- Receipt sequence numbers, date stamps, time stamps
- Hand-drawn style checkboxes with fluorescent marker effects
- High information density, no empty white space
- Modern skeuomorphism design with claymorphism icons
- Aspect ratio: 3:4 (portrait vertical)

CRITICAL: All content text MUST be in CHINESE (中文). DO NOT translate to English.'''

print("🎨 开始生成信息图...")
print(f"模型: {MODEL}")
print(f"比例: 3:4 竖版")
print("-" * 50)

# 构建请求
url = f"{BASE_URL}/models/{MODEL}:generateContent?key={API_KEY}"

headers = {
    "Content-Type": "application/json",
}

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

# 发送请求
try:
    start_time = time.time()

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    # 设置代理（如果配置）- 先尝试直连
    proxy = os.getenv("ALL_IMAGE_PROXY")
    # 暂时不使用代理，因为代理可能不可用
    # if proxy:
    #     req.set_proxy(proxy, "https")
    #     req.set_proxy(proxy, "http")
    #     print(f"使用代理: {proxy}")

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    generation_time = time.time() - start_time

    # 解析结果
    if "candidates" in result and len(result["candidates"]) > 0:
        image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

        # 保存图片
        output_dir = "C:/Users/RyanCh/.claude/skills/info-graphic/output/ai_agent_infographic/images"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_dir}/ai_agent_receipt_{timestamp}.png"

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print("-" * 50)
        print("✅ 生成成功！")
        print(f"Provider: Google AI ({MODEL})")
        print(f"图片路径: {output_path}")
        print(f"生成时间: {generation_time:.1f} 秒")
        print(f"文件大小: {len(image_data)/1024:.1f} KB")
        sys.exit(0)
    else:
        print("❌ 生成失败: 未返回图片数据")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        sys.exit(1)

except urllib.error.HTTPError as e:
    print(f"❌ HTTP 错误: {e.code} {e.reason}")
    try:
        error_body = e.read().decode("utf-8")
        print(f"详情: {error_body}")
    except:
        pass
    sys.exit(1)
except urllib.error.URLError as e:
    print(f"❌ 网络错误: {e.reason}")
    print("💡 建议: 检查代理设置或网络连接")
    sys.exit(1)
except Exception as e:
    print(f"❌ 未知错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
