# PicGo 图床管理 Skill

## 描述

PicGo 图床管理 - 支持图片上传到七牛云等图床服务，可扩展支持多种图床（SM.MS、阿里云OSS、腾讯云COS、GitHub、Imgur等）。

## 何时使用

当用户需要：
- 上传图片到图床获取 URL
- 批量上传图片
- 检查 PicGo 配置
- 切换不同的图床服务

触发关键词：
- "上传图片"、"上传到图床"
- "picgo upload"
- "图床上传"
- "获取图片链接"

## 环境要求

- 已安装 `picgo` CLI 工具（通过 `npm install -g picgo` 安装）
- 配置文件位于 `~/.picgo/config.json`

## 当前配置

- **图床服务**：七牛云 (Qiniu)
- **存储桶**：imgbed67
- **域名**：http://tbeq8bmje.hn-bkt.clouddn.com
- **路径**：img/
- **区域**：z2 (华南)
- **图片处理**：?imageView2/2/w/1200 (宽度限制1200px)

## 使用方法

### 1. 上传单个图片

```bash
picgo upload /path/to/image.png
```

### 2. 上传多个图片

```bash
picgo upload image1.png image2.jpg image3.png
```

### 3. 上传整个文件夹

```bash
picgo upload /path/to/folder/*
```

### 4. 查看配置

```bash
cat ~/.picgo/config.json
```

### 5. 设置默认图床

```bash
# 在配置文件中修改 "current" 字段
# 可选值: qiniu, smms, aliyun, tcyun, github, imgur, upyun
```

## 输出格式

上传成功后返回图片 URL：
```
http://tbeq8bmje.hn-bkt.clouddn.com/img/your-image.png?imageView2/2/w/1200
```

## 支持的图床服务

| 服务 | 配置键 | 说明 |
|------|--------|------|
| 七牛云 | qiniu | 当前使用 |
| SM.MS | smms | 免费图床 |
| 阿里云OSS | aliyun | 阿里云对象存储 |
| 腾讯云COS | tcyun | 腾讯云对象存储 |
| GitHub | github | 仓库作为图床 |
| Imgur | imgur | 国外图床 |
| 又拍云 | upyun | 又拍云存储 |

## Claude Code 使用示例

```markdown
用户: 帮我上传这张图片到图床
Claude: 我将使用 PicGo 上传图片...
[执行 picgo upload 命令]
上传成功！图片链接：http://...

---

用户: 把这个文件夹里的所有图片都上传
Claude: 正在上传文件夹中的所有图片...
[执行批量上传]
完成！共上传 N 张图片：
1. http://...
2. http://...
```

## 配置管理

### 添加新的图床服务

编辑 `~/.picgo/config.json`，在 `picBed` 下添加对应配置：

```json
{
  "picBed": {
    "uploader": "qiniu",
    "current": "qiniu",
    "qiniu": { ... },
    "github": {
      "repo": "username/repo",
      "token": "your_token",
      "path": "img/",
      "customUrl": "https://cdn.jsdelivr.net/gh/username/repo"
    }
  }
}
```

### 安装 PicGo 插件

```bash
picgo install super-prefix
picgo install md-wizard
```

## 故障排查

### 上传失败

1. 检查网络连接
2. 验证七牛云 AccessKey/SecretKey 是否正确
3. 确认存储桶名称和区域配置正确

### 配置文件位置

- Windows: `C:\Users\用户名\.picgo\config.json`
- Linux/Mac: `~/.picgo/config.json`

## Obsidian 集成配置

### 方法一：PicGo 服务端（已启动）

PicGo 服务端已在后台运行：
```
地址: http://127.0.0.1:36677
```

在 Obsidian 中配置：
1. 安装插件：`Image auto upload Plugin` 或 `Easy Image Uploader`
2. 插件设置：
   - **上传器**: PicGo
   - **PicGo 路径**: `picgo` (CLI命令) 或 `http://127.0.0.1:36677` (服务端地址)
   - **工作目录**: 留空或设置图片存储路径

### 方法二：直接调用 CLI

Obsidian 插件配置直接调用 `picgo` 命令：
```
上传器: CLI
命令: picgo upload
```

### 自动上传设置

在 Obsidian 插件中启用：
- ✅ 粘贴图片时自动上传
- ✅ 拖拽图片时自动上传
- ✅ 选择图片时自动上传

### 启动/停止 PicGo 服务

#### 方法一：开机自启动（推荐）

已配置开机自启动，重启电脑后自动运行：
- 脚本位置：`C:\Users\RyanCh\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start-picgo-server.bat`

#### 方法二：手动启动

```bash
# 启动服务
picgo server

# 指定端口启动
picgo server -p 36677

# Windows 后台启动（PowerShell）
Start-Process -WindowStyle Hidden picgo -ArgumentList "server"
```

#### 方法三：使用 PowerShell 脚本（带状态检测）

```powershell
# 运行智能启动脚本
D:\ProjectAI\CC\CC_record\skills\picgo\start-picgo-server.ps1
```

功能：
- ✅ 自动检测是否已运行
- ✅ 后台启动，不显示窗口
- ✅ 启动成功/失败提示

## 相关链接

- PicGo 官网: https://picgo.github.io/PicGo-Doc/
- 七牛云控制台: https://portal.qiniu.com/
- Obsidian 插件市场: https://obsidian.md/plugins
