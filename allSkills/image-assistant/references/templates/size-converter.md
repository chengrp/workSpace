# 尺寸参数统一转换层

## 问题描述

不同 API 使用不同的尺寸参数格式，导致切换 API 时需要手动调整：

| API | 参数名 | 格式 | 示例 |
|-----|--------|------|------|
| 云雾 API | prompt 内嵌 | 文本描述 | `"A cat. Aspect ratio: 16:9."` |
| Google AI | prompt 内嵌 | 文本描述 | `"A cat. Aspect ratio: 9:16."` |
| Google Imagen | aspectRatio | 比例字符串 | `"16:9"` |
| ModelScope | size | "宽x高" | `"1792x1024"` |
| APIMart | size | 比例字符串 | `"16:9"` |
| OpenAI | size | "宽x高" | `"1024x1792"` |

## 解决方案

使用统一的转换函数，自动将标准比例转换为各 API 所需格式。

---

## 一、尺寸映射表

```typescript
// 标准比例到实际像素的映射
const SIZE_MAP = {
  '16:9': { width: 1792, height: 1024 },
  '9:16': { width: 1024, height: 1792 },
  '1:1': { width: 1536, height: 1536 },
  '4:3': { width: 1536, height: 1152 },
  '3:4': { width: 1152, height: 1536 },
  '21:9': { width: 2048, height: 896 },
  '3:2': { width: 1536, height: 1024 },
} as const;
```

---

## 二、TypeScript 转换函数

```typescript
/**
 * 统一尺寸参数类型
 */
type AspectRatio = keyof typeof SIZE_MAP;
type ApiProvider = 'yunwu' | 'google' | 'imagen' | 'modelscope' | 'apimart' | 'openai';

/**
 * 转换尺寸参数到各 API 格式
 */
class SizeConverter {
  /**
   * 获取像素尺寸
   */
  static getPixels(ratio: AspectRatio): { width: number; height: number } {
    return SIZE_MAP[ratio];
  }

  /**
   * 云雾 API / Gemini 格式（嵌入提示词）
   */
  static forYunwu(ratio: AspectRatio): string {
    return `Aspect ratio: ${ratio}.`;
  }

  static forGemini(ratio: AspectRatio): string {
    return `Aspect ratio: ${ratio}.`;
  }

  /**
   * Google Imagen 格式（独立参数）
   */
  static forImagen(ratio: AspectRatio): string {
    return ratio; // "16:9"
  }

  /**
   * ModelScope 格式（"宽x高"）
   */
  static forModelScope(ratio: AspectRatio): string {
    const { width, height } = SIZE_MAP[ratio];
    return `${width}x${height}`;
  }

  /**
   * APIMart 格式（比例字符串）
   */
  static forApimart(ratio: AspectRatio): string {
    return ratio;
  }

  /**
   * OpenAI 格式（"宽x高"）
   */
  static forOpenAI(ratio: AspectRatio): string {
    const { width, height } = SIZE_MAP[ratio];
    return `${width}x${height}`;
  }

  /**
   * 通用转换函数
   */
  static convert(ratio: AspectRatio, provider: ApiProvider): string {
    switch (provider) {
      case 'yunwu':
        return this.forYunwu(ratio);
      case 'google':
        return this.forGemini(ratio);
      case 'imagen':
        return this.forImagen(ratio);
      case 'modelscope':
        return this.forModelScope(ratio);
      case 'apimart':
        return this.forApimart(ratio);
      case 'openai':
        return this.forOpenAI(ratio);
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }

  /**
   * 构建完整提示词（云雾/Gemini）
   */
  static buildPrompt(basePrompt: string, ratio: AspectRatio, provider: 'yunwu' | 'google'): string {
    const sizeDirective = this.convert(ratio, provider);
    return `${basePrompt.trim()} ${sizeDirective}`;
  }
}

// 使用示例
const prompt = "一只可爱的猫咪，奶油纸底，彩铅手绘风格";

// 云雾 API
SizeConverter.buildPrompt(prompt, '16:9', 'yunwu');
// 输出: "一只可爱的猫咪，奶油纸底，彩铅手绘风格 Aspect ratio: 16:9."

// ModelScope
SizeConverter.forModelScope('16:9');
// 输出: "1792x1024"

// Imagen
SizeConverter.forImagen('16:9');
// 输出: "16:9"
```

---

## 三、Python 转换函数

```python
from typing import Literal

# 标准比例到像素的映射
SIZE_MAP = {
    '16:9': (1792, 1024),
    '9:16': (1024, 1792),
    '1:1': (1536, 1536),
    '4:3': (1536, 1152),
    '3:4': (1152, 1536),
    '21:9': (2048, 896),
    '3:2': (1536, 1024),
}

AspectRatio = Literal['16:9', '9:16', '1:1', '4:3', '3:4', '21:9', '3:2']
Provider = Literal['yunwu', 'google', 'imagen', 'modelscope', 'apimart', 'openai']

class SizeConverter:
    """尺寸参数统一转换类"""

    @staticmethod
    def get_pixels(ratio: AspectRatio) -> tuple[int, int]:
        """获取像素尺寸"""
        return SIZE_MAP[ratio]

    @staticmethod
    def for_yunwu(ratio: AspectRatio) -> str:
        """云雾 API 格式"""
        return f"Aspect ratio: {ratio}."

    @staticmethod
    def for_gemini(ratio: AspectRatio) -> str:
        """Gemini 格式"""
        return f"Aspect ratio: {ratio}."

    @staticmethod
    def for_imagen(ratio: AspectRatio) -> str:
        """Imagen 格式"""
        return ratio

    @staticmethod
    def for_modelscope(ratio: AspectRatio) -> str:
        """ModelScope 格式 (宽x高)"""
        width, height = SIZE_MAP[ratio]
        return f"{width}x{height}"

    @staticmethod
    def for_apimart(ratio: AspectRatio) -> str:
        """APIMart 格式"""
        return ratio

    @staticmethod
    def for_openai(ratio: AspectRatio) -> str:
        """OpenAI 格式 (宽x高)"""
        width, height = SIZE_MAP[ratio]
        return f"{width}x{height}"

    @classmethod
    def convert(cls, ratio: AspectRatio, provider: Provider) -> str:
        """通用转换函数"""
        converters = {
            'yunwu': cls.for_yunwu,
            'google': cls.for_gemini,
            'imagen': cls.for_imagen,
            'modelscope': cls.for_modelscope,
            'apimart': cls.for_apimart,
            'openai': cls.for_openai,
        }
        converter = converters.get(provider)
        if not converter:
            raise ValueError(f"Unknown provider: {provider}")
        return converter(ratio)

    @classmethod
    def build_prompt(cls, base_prompt: str, ratio: AspectRatio, provider: Literal['yunwu', 'google']) -> str:
        """构建完整提示词（云雾/Gemini）"""
        size_directive = cls.convert(ratio, provider)
        return f"{base_prompt.strip()} {size_directive}"


# 使用示例
if __name__ == "__main__":
    prompt = "一只可爱的猫咪，奶油纸底，彩铅手绘风格"

    # 云雾 API
    print(SizeConverter.build_prompt(prompt, '16:9', 'yunwu'))
    # 输出: 一只可爱的猫咪，奶油纸底，彩铅手绘风格 Aspect ratio: 16:9.

    # ModelScope
    print(SizeConverter.for_modelscope('16:9'))
    # 输出: 1792x1024

    # Imagen
    print(SizeConverter.for_imagen('16:9'))
    # 输出: 16:9
```

---

## 四、请求体构建示例

### TypeScript 完整示例

```typescript
/**
 * 统一生图请求构建器
 */
class ImageRequestBuilder {
  static build(
    prompt: string,
    ratio: AspectRatio,
    provider: ApiProvider
  ): { url: string; headers: Record<string, string>; body: object } {
    const basePrompt = prompt.trim();

    switch (provider) {
      case 'yunwu':
        return {
          url: `https://yunwu.ai/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key=${process.env.YUNWU_API_KEY}`,
          headers: { 'Content-Type': 'application/json' },
          body: {
            contents: [{
              parts: [{ text: SizeConverter.buildPrompt(basePrompt, ratio, 'yunwu') }]
            }],
            generationConfig: {
              responseModalities: ['IMAGE', 'TEXT']
            }
          }
        };

      case 'google':
        return {
          url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=${process.env.GOOGLE_API_KEY}`,
          headers: { 'Content-Type': 'application/json' },
          body: {
            contents: [{
              parts: [{ text: SizeConverter.buildPrompt(basePrompt, ratio, 'google') }]
            }],
            generationConfig: {
              responseModalities: ['IMAGE', 'TEXT']
            }
          }
        };

      case 'imagen':
        return {
          url: `https://generativelanguage.googleapis.com/v1beta/openai/images/generations?key=${process.env.GOOGLE_API_KEY}`,
          headers: { 'Content-Type': 'application/json' },
          body: {
            model: 'imagen-3.0-generate-001',
            prompt: basePrompt,
            aspectRatio: SizeConverter.forImagen(ratio),
            responseFormat: 'b64_json',
            n: 1
          }
        };

      case 'modelscope':
        return {
          url: 'https://api-inference.modelscope.cn/v1/images/generations',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.MODELSCOPE_API_KEY}`,
            'X-ModelScope-Async-Mode': 'true'
          },
          body: {
            model: 'Tongyi-MAI/Z-Image-Turbo',
            prompt: basePrompt,
            size: SizeConverter.forModelScope(ratio)
          }
        };

      case 'apimart':
        return {
          url: 'https://api.apimart.ai/v1/images/generations',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.APIMART_TOKEN}`
          },
          body: {
            model: 'gemini-3-pro-image-preview',
            prompt: basePrompt,
            size: SizeConverter.forApimart(ratio),
            n: 1,
            resolution: '2K'
          }
        };

      case 'openai':
        return {
          url: 'https://api.openai.com/v1/images/generations',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`
          },
          body: {
            model: 'gpt-image-1',
            prompt: basePrompt,
            size: SizeConverter.forOpenAI(ratio),
            n: 1
          }
        };

      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }
}
```

---

## 五、Python 完整示例

```python
import os
from typing import Literal

Provider = Literal['yunwu', 'google', 'imagen', 'modelscope', 'apimart', 'openai']
AspectRatio = Literal['16:9', '9:16', '1:1', '4:3', '3:4', '21:9', '3:2']

class ImageRequestBuilder:
    """统一生图请求构建器"""

    @staticmethod
    def build(
        prompt: str,
        ratio: AspectRatio,
        provider: Provider
    ) -> dict[str, str | dict]:
        """构建请求"""
        base_prompt = prompt.strip()

        if provider == 'yunwu':
            return {
                'url': f"https://yunwu.ai/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key={os.getenv('YUNWU_API_KEY')}",
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'contents': [{
                        'parts': [{'text': SizeConverter.build_prompt(base_prompt, ratio, 'yunwu')}]
                    }],
                    'generationConfig': {
                        'responseModalities': ['IMAGE', 'TEXT']
                    }
                }
            }

        elif provider == 'modelscope':
            return {
                'url': 'https://api-inference.modelscope.cn/v1/images/generations',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {os.getenv('MODELSCOPE_API_KEY')}",
                    'X-ModelScope-Async-Mode': 'true'
                },
                'body': {
                    'model': 'Tongyi-MAI/Z-Image-Turbo',
                    'prompt': base_prompt,
                    'size': SizeConverter.for_modelscope(ratio)
                }
            }

        # ... 其他 provider 类似
```

---

## 六、使用速查表

```typescript
// 快速使用
const ratio = '16:9';

// 云雾 / Gemini - 嵌入提示词
const prompt = `A cat. ${SizeConverter.forYunwu(ratio)}`;
// "A cat. Aspect ratio: 16:9."

// ModelScope - 像素尺寸
const size = SizeConverter.forModelScope(ratio);
// "1792x1024"

// Imagen - 比例字符串
const aspectRatio = SizeConverter.forImagen(ratio);
// "16:9"
```

---

## 七、迁移指南

### 旧代码
```typescript
// ❌ 硬编码，切换 API 需要手动改
const size = "16:9";  // Imagen
const size = "1792x1024";  // ModelScope
const prompt = "A cat. Aspect ratio: 16:9.";  // Yunwu
```

### 新代码
```typescript
// ✅ 统一接口，自动转换
const ratio: AspectRatio = '16:9';
SizeConverter.convert(ratio, 'imagen');      // "16:9"
SizeConverter.convert(ratio, 'modelscope');  // "1792x1024"
SizeConverter.buildPrompt("A cat.", ratio, 'yunwu');  // "A cat. Aspect ratio: 16:9."
```

---

## 八、测试用例

```typescript
// 测试所有 API 的尺寸转换
describe('SizeConverter', () => {
  const ratio: AspectRatio = '16:9';

  test('yunwu format', () => {
    expect(SizeConverter.forYunwu(ratio)).toBe('Aspect ratio: 16:9.');
  });

  test('modelscope format', () => {
    expect(SizeConverter.forModelScope(ratio)).toBe('1792x1024');
  });

  test('imagen format', () => {
    expect(SizeConverter.forImagen(ratio)).toBe('16:9');
  });

  test('get pixels', () => {
    expect(SizeConverter.getPixels(ratio)).toEqual({ width: 1792, height: 1024 });
  });
});
```

---

## 九、文件位置

将此文件保存到：`templates/size-converter.md`

集成到你的项目时：
- TypeScript 版本 → `src/utils/size-converter.ts`
- Python 版本 → `scripts/size_converter.py`
