"""
ModelScope API配置
"""

# API配置
API_KEY = "ms-51dd7494-0706-45d9-a901-c395522c55f2"
BASE_URL = "https://api-inference.modelscope.cn/"

# 模型配置
DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo"

# 轮询配置
DEFAULT_CHECK_INTERVAL = 5  # 秒

# 输出配置
DEFAULT_OUTPUT_PATH = "result_image.jpg"

# 额度信息
DAILY_FREE_QUOTA = 2000  # 每日免费额度
