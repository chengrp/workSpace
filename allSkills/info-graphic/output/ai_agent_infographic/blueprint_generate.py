#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成坐标蓝图·波普实验室风格信息图
"""
import os
import sys
import base64
import urllib.request
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
    print("错误: 未设置 GOOGLE_API_KEY")
    sys.exit(1)

# 坐标蓝图·波普实验室风格提示词
prompt = '''当智能不再稀缺 - 时代变革账单

Create a high-density infographic in Blueprint Pop Lab style (坐标蓝图·波普实验室).

=== CONTENT (7 modules with coordinates) ===
TITLE: 当智能不再稀缺 - 时代变革账单

[A-01] IBM暴跌13% - 一天蒸发310亿美元，认知劳动边际成本趋零的信号
[B-03] 六把刀理论 - DAU失效、平台化路径断裂、SaaS转向2A、AI应用概念错误、注意力经济过时、出海概念消亡
[C-07] 奇点推演 - 智能可无限生产，200美金就能买到CEO级能力，窗口正在关闭
[D-12] 三层社会 - 第一层算力拥有者(定义规则)、第二层算力驱动者(调度Agent)、第三层算力依附者(被边缘化)
[E-05] 变化信号 - Obsidian CLI发布、EvoMap进化型系统、Agent雇佣人类、企业减员增效引入AI
[F-09] 行动清单 - 重新审视可替代性、学会驱动Agent协作、关注算力和能源分布、创业做新世界基建、教育重心转移
[G-15] 金句收尾 - "悲观者是远见，乐观者才是智慧"

=== STYLE: Blueprint Pop Lab (坐标蓝图·波普实验室) ===
- LABORATORY BLUEPRINT AESTHETIC with fluorescent color accents
- Background: Professional grayish-white #F2F2F2 with blueprint grid texture
- Base Colors: Muted Teal/Sage Green #B8D8BE
- Accent Colors: Vibrant Fluorescent Pink #E91E63, Vivid Lemon Yellow #FFF200, Ultra-fine Charcoal Brown #2D2926

LAYOUT STYLE:
- INFORMATION AS COORDINATES: Each module has coordinate labels (A-01, B-03, C-07, etc.)
- HIGH DENSITY: 7 modules packed tightly, minimal margins
- VISUAL CONTRAST: Ultra-bold headers vs tiny technical annotations
- LAB MANUAL AESTHETIC: Mix of microscopic details and macro data

VISUAL ELEMENTS:
- TECHNICAL DIAGRAMS: Explosion views, cross-sections, architectural skeleton lines
- COORDINATE SYSTEMS: Precision rulers (0.5mm, 1.8mm, 45° angle marks)
- DATA BLOCKS: "Marker-over-Print" effect with color blocks slightly offset from text
- SYMBOLS: Crosshair reticles, mathematical symbols (Σ, Δ, ∞), directional arrows
- Corner metadata: Barcodes, timestamps, technical parameters

TYPOGRAPHY:
- Headers: Bold Brutalist Chinese characters, high impact
- Body: Professional sans-serif or crisp handwritten technical print
- Numbers: Large, highlighted with Yellow or Blue

Style Keywords: technical, blueprint, laboratory, coordinates, precision, industrial design

CRITICAL: All content text MUST be in CHINESE (中文). DO NOT translate to English.
- Aspect ratio: 3:4 portrait vertical
- High information density with 7 modules
- No empty white space, fully packed with information'''

print("开始生成信息图...")
print(f"风格: 坐标蓝图·波普实验室 (Blueprint Pop Lab)")
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
        output_path = f"{output_dir}/ai_agent_blueprint_{timestamp}.png"

        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_data))

        print("-" * 50)
        print("生成成功！")
        print(f"Provider: Google AI ({MODEL})")
        print(f"图片路径: {output_path}")
        print(f"生成时间: {generation_time:.1f} 秒")
        print(f"文件大小: {len(image_data)/1024:.1f} KB")
        sys.exit(0)
    else:
        print("生成失败: 未返回图片数据")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        sys.exit(1)

except urllib.error.HTTPError as e:
    print(f"HTTP 错误: {e.code} {e.reason}")
    try:
        error_body = e.read().decode("utf-8")
        print(f"详情: {error_body}")
    except:
        pass
    sys.exit(1)
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
