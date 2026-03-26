# Spider Proxy 🕷️

**轻量级、开源、移动端优先的手机抓包工具**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Android-green.svg)]()
[![API](https://img.shields.io/badge/API-24%2B-brightgreen.svg)]()

---

## 📖 项目简介

Spider Proxy 是一款专为移动开发者设计的轻量级抓包工具，支持 HTTP/HTTPS 流量捕获、查看、过滤和导出。

### ✨ 核心特性

- 🔒 **HTTPS 解密** - 完整支持 SSL/TLS 流量解密
- 📱 **移动端优先** - 专为手机操作优化的界面设计
- 🚀 **轻量快速** - 内存占用 < 200MB，抓包延迟 < 100ms
- 🔍 **智能过滤** - 域名过滤、关键词搜索、状态码筛选
- 📤 **多格式导出** - 支持 PCAP、HAR、JSON 格式
- 🆓 **完全开源** - Apache 2.0 协议，免费使用

---

## 📸 应用截图

| 首页 | 详情页 | 设置页 |
|-----|--------|--------|
| 📱 流量列表 | 📱 请求响应 | 📱 证书管理 |

*(截图待补充)*

---

## 🚀 快速开始

### 系统要求

- Android 7.0 (API 24) 及以上
- 需要安装 CA 证书以解密 HTTPS 流量

### 安装使用

1. **下载安装**
   ```bash
   # 从 Google Play 下载
   # 或从 Releases 页面下载 APK
   ```

2. **安装证书**
   - 打开应用
   - 点击「安装证书」
   - 按提示完成证书安装

3. **开始抓包**
   - 点击首页「开始」按钮
   - 允许 VPN 连接
   - 开始浏览应用，查看流量

---

## 📋 功能清单

### v1.0 (MVP) ✅

| 功能模块 | 功能 | 状态 |
|---------|------|------|
| 基础抓包 | HTTP/HTTPS 抓包 | ✅ |
| 基础抓包 | SSL 证书管理 | ✅ |
| 基础抓包 | 流量列表展示 | ✅ |
| 流量查看 | 请求/响应详情 | ✅ |
| 流量查看 | JSON 格式化 | ✅ |
| 流量查看 | 图片预览 | ✅ |
| 过滤搜索 | 域名过滤 | ✅ |
| 过滤搜索 | 关键词搜索 | ✅ |
| 导出分享 | PCAP 导出 | ✅ |
| 导出分享 | HAR 导出 | ✅ |

### v2.0 (高级功能) 🔄

| 功能模块 | 功能 | 说明 |
|---------|------|------|
| 流量分析 | 实时流量统计图表 | 请求量/流量大小趋势图 |
| 流量分析 | 请求/响应时间线 | 瀑布图展示各阶段耗时 |
| 流量分析 | 域名/IP 分布热力图 | 识别高频访问服务器 |
| 过滤系统 | 多条件组合过滤 | AND/OR 逻辑组合 |
| 过滤系统 | 正则表达式过滤 | 高级匹配模式 |
| 过滤系统 | 过滤预设管理 | 快速切换过滤方案 |
| 搜索功能 | 全文搜索 | 请求头/响应头/Body 搜索 |
| 搜索功能 | JSON/XML 高亮 | 语法高亮 + 路径搜索 |
| 搜索功能 | 搜索历史 | 快速重用搜索词 |
| 请求重写 | 请求头修改 | 添加/修改/删除 Header |
| 请求重写 | 响应头修改 | 调试 CORS、缓存等 |
| 请求重写 | URL 重定向 | 本地开发调试 |
| 请求重写 | 请求重放 | 修改后重发 |
| 脚本系统 | 内置脚本模板 | 常用功能一键应用 |
| 脚本系统 | 自定义脚本 | JavaScript/Python |
| 数据导出 | cURL 命令 | 生成可执行命令 |
| 数据导出 | Markdown 报告 | 可读性好的报告 |
| 数据导出 | 批量导出 | 多种格式同时导出 |
| 协作功能 | 会话分享 | 生成分享链接 |

### v3.0 (专业功能) ⏳

| 功能模块 | 功能 | 说明 |
|---------|------|------|
| 请求重写 | Body 替换 | Map Local/Remote |
| 断点调试 | 请求前断点 | 修改后发送 |
| 断点调试 | 响应前断点 | 修改后返回 |
| 断点调试 | 手动修改 | 编辑请求/响应 |
| 脚本系统 | 脚本市场 | 社区分享脚本 |
| 脚本系统 | 脚本调试器 | 断点/单步执行 |
| WebSocket | WebSocket 抓包 | 实时通信调试 |
| WebSocket | 消息查看 | 消息序列分析 |
| 性能分析 | 耗时统计 | 性能瓶颈分析 |
| 协作功能 | 项目共享 | 团队协作 |
| 协作功能 | 团队注释 | 请求上添加注释 |
| 协作功能 | 评论系统 |  threaded comments |

---

## 🏗 技术架构

```
┌─────────────────────────────────────┐
│         Flutter Widgets UI          │
├─────────────────────────────────────┤
│         flutter_redux 状态管理        │
├─────────────────────────────────────┤
│     Proxy Engine (Dart + Platform)  │
├─────────────────────────────────────┤
│     Hive + Platform Channel         │
└─────────────────────────────────────┘
```

### 技术栈

| 层次 | 技术 | 说明 |
|-----|------|------|
| **框架** | Flutter 3.24+ | 跨平台 UI 框架 |
| **语言** | Dart 3.5+ | 主开发语言 |
| **状态管理** | flutter_redux 6.0+ | 全局状态管理 |
| **本地存储** | Hive 2.2+ | 轻量级 NoSQL 数据库 |
| **HTTP 服务** | dart:io HttpServer | 内置 HTTP 服务器 |
| **MITM 代理** | 自研 | 基于 dart:io 实现 |
| **VPN 服务** | Platform Channel | 调用原生能力 |
| **证书管理** | Platform Channel | Android Keystore / iOS Keychain |

详细架构设计见 [docs/技术栈决策.md](docs/技术栈决策.md)

---

## 📚 文档

### 需求与设计

| 文档 | 说明 |
|-----|------|
| [竞品调研报告](docs/竞品调研报告.md) | 市面主流抓包工具对比分析 |
| [需求规格说明书](docs/需求规格说明书.md) | 完整功能需求定义 |
| [功能设计详细文档](docs/功能设计详细文档.md) | v2.0-v3.0 功能详细设计 |
| [技术架构设计](docs/技术架构设计.md) | 技术栈和架构设计 |
| [API 接口设计](docs/API 接口设计.md) | 内部数据接口定义 |

### UI/UX 设计

| 文档 | 说明 |
|-----|------|
| [UI 设计规范](docs/UI 设计规范.md) | 设计原则、色彩、字体、组件 |
| [页面线框图](docs/页面线框图.md) | 页面布局和交互 (ASCII) |
| [交互流程说明](docs/交互流程说明.md) | 用户操作流程、状态转换 |

### 开发指南

| 文档 | 说明 |
|-----|------|
| [开发路线图](docs/开发路线图.md) | 分阶段开发计划 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |

---

## 🔧 开发指南

### 环境准备

**系统要求:**
- macOS 12+ / Windows 10+ / Linux
- 内存：8GB+
- 磁盘：10GB+

**安装步骤:**

```bash
# 1. 安装 Flutter (如未安装)
$ git clone https://github.com/flutter/flutter.git -b stable
$ export PATH="$PATH:`pwd`/flutter/bin"

# 2. 验证安装
$ flutter doctor

# 3. 克隆项目
$ git clone https://github.com/your-org/spider-proxy.git
$ cd spider-proxy

# 4. 安装依赖
$ cd code
$ flutter pub get

# 5. 运行应用
$ flutter run
```

### 项目结构

```
code/
├── lib/                   # Dart 源代码
│   ├── main.dart         # 应用入口
│   ├── core/             # 核心模块
│   │   ├── proxy/        # 代理引擎
│   │   ├── vpn/          # VPN 服务 (Platform Channel)
│   │   └── ssl/          # 证书管理
│   ├── features/         # 功能模块
│   │   ├── traffic/      # 流量监控
│   │   ├── filter/       # 过滤系统
│   │   └── ai/           # AI 分析
│   └── ui/               # UI 界面
│       ├── pages/        # 页面
│       └── widgets/      # 组件
├── android/              # Android 原生代码
├── ios/                  # iOS 原生代码
├── test/                 # 测试代码
└── pubspec.yaml          # Flutter 依赖配置
```

### 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

详细贡献指南见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## ⚠️ 注意事项

### HTTPS 固定证书

部分应用使用 SSL Pinning 技术，无法通过常规方式抓包。这是正常的安全机制，不是工具缺陷。

### 隐私说明

- 所有流量数据仅存储在本地
- 不会上传任何用户数据到服务器
- 证书私钥安全存储在应用沙盒

### 使用限制

- 仅限开发调试使用
- 请勿用于非法目的
- 尊重应用隐私政策

---

## 📄 开源协议

本项目采用 Apache 2.0 协议开源。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

感谢以下开源项目：

- [Flutter](https://flutter.dev/) - 跨平台 UI 框架
- [Dart](https://dart.dev/) - 开发语言
- [flutter_redux](https://pub.dev/packages/flutter_redux) - 状态管理
- [Hive](https://docs.hivedb.dev/) - 本地数据库
- [permission_handler](https://pub.dev/packages/permission_handler) - 权限管理

参考项目：

- HttpCanary (黄鸟抓包)
- Proxyman
- PCAPdroid
- Charles

---

## 📬 联系方式

- 📧 Email: contact@spiderproxy.dev
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/spider-proxy/issues)
- 💬 Discussion: [GitHub Discussions](https://github.com/your-org/spider-proxy/discussions)

---

## 📊 项目状态

| 阶段 | 状态 | 预计完成 |
|-----|------|---------|
| 需求分析 | ✅ 完成 | 2026-03-24 |
| 架构设计 | ✅ 完成 | 2026-03-24 |
| **技术栈确认** | ✅ 完成 (Flutter) | 2026-03-25 |
| MVP 开发 | 🔄 进行中 | 2026-05-20 |
| 公开测试 | ⏳ 计划中 | 2026-06-01 |
| 正式发布 | ⏳ 计划中 | 2026-06-15 |

**当前版本:** v0.1 (原型验证阶段)

---

Made with ❤️ by Spider Proxy Team

*Last Updated: 2026-03-25*
