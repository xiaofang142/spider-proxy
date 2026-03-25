# OpenCode CLI 开发指南

> 版本：1.2.24 | 更新时间：2026-03-24

---

## 📦 一、安装方法

### 方式 1：Homebrew（推荐 macOS 用户）
```bash
brew install opencode
```

### 方式 2：npm
```bash
npm install -g opencode-ai
```

### 方式 3：pnpm
```bash
pnpm add -g opencode-ai
```

### 验证安装
```bash
opencode --version
# 输出：1.2.24
```

---

## 🔑 二、配置 API Key

### 配置 Providers
```bash
opencode providers
```

支持的主流 Provider：
- `alibaba-coding-plan-cn` - 阿里通义千问系列
- `siliconflow` - 硅基流动（DeepSeek、Llama 等）
- `opencode` - OpenCode 官方模型

### 设置默认模型
在 `~/.opencode/config.json` 或通过命令行参数：
```bash
opencode run -m alibaba-coding-plan-cn/qwen3.5-plus "你的提示词"
```

### 可用模型列表
```bash
opencode models
# 或指定 provider
opencode models alibaba-coding-plan-cn
```

---

## 🛠️ 三、核心命令

### 1. 运行代码生成任务
```bash
# 基本用法
opencode run "创建一个新的 Flutter 项目"

# 指定模型
opencode run -m alibaba-coding-plan-cn/qwen3.5-plus "生成 HTTP 代理服务器代码"

# 指定目录
opencode run --dir /path/to/project "重构核心模块"

# 附加文件
opencode run -f main.dart -f config.dart "分析这两个文件的依赖关系"

# 继续上次会话
opencode run --continue "继续昨天的工作"
```

### 2. 项目管理
```bash
# 启动 TUI 交互模式
opencode /path/to/project

# 附加到运行中的服务器
opencode attach http://localhost:4096

# 启动 Web 界面
opencode web
```

### 3. GitHub 集成
```bash
# 安装 GitHub Agent
opencode github install

# 拉取并 checkout PR
opencode pr 123

# 运行 GitHub Agent
opencode github run
```

### 4. 会话管理
```bash
# 导出会话
opencode export <sessionID>

# 导入会话
opencode import session.json

# 查看使用统计
opencode stats
```

### 5. MCP 服务器管理
```bash
opencode mcp
```

---

## 📋 四、工作流配置

### 常用工作流模式

#### 模式 1：单次任务执行
```bash
opencode run --format json "生成单元测试" > output.json
```

#### 模式 2：交互式开发
```bash
opencode /path/to/project
# 进入 TUI 后持续对话
```

#### 模式 3：后台服务
```bash
opencode serve --port 4096
# 其他客户端可 attach
```

### 环境变量配置
```bash
export OPENCODE_MODEL=alibaba-coding-plan-cn/qwen3.5-plus
export OPENCODE_PROVIDER=alibaba-coding-plan-cn
```

---

## 🎯 五、最佳实践

### 提示词编写技巧
1. **明确任务类型**：说明是"创建"、"修改"、"重构"还是"调试"
2. **提供上下文**：附加相关文件或使用 `--dir` 指定项目目录
3. **指定输出格式**：明确需要代码、文档还是测试
4. **分步执行**：复杂任务拆分为多个小任务

### 示例：Flutter 项目开发
```bash
# 1. 创建项目结构
opencode run "创建 Flutter 项目目录结构，包含 lib/core, lib/features, lib/ui"

# 2. 生成核心模块
opencode run -f pubspec.yaml "生成 HTTP 代理服务器核心代码"

# 3. 生成测试
opencode run -f lib/core/proxy.dart "为代理模块生成单元测试"

# 4. 代码审查
opencode run "审查 lib/ 目录下的代码质量问题"
```

---

## 🔧 六、调试工具

```bash
# 查看配置
opencode debug config

# 查看路径
opencode debug paths

# 查看可用技能
opencode debug skill

# LSP 调试
opencode debug lsp

# 文件调试
opencode debug file
```

---

## 📊 七、支持的编程语言和框架

OpenCode CLI 支持主流编程语言：
- **Dart/Flutter** - 移动应用开发
- **TypeScript/JavaScript** - Web 开发
- **Python** - 后端/脚本
- **Go** - 系统编程
- **Rust** - 系统编程
- **Java/Kotlin** - Android 开发
- **Swift** - iOS 开发

---

## ⚠️ 八、注意事项

1. **API Key 安全**：不要将密钥提交到版本控制
2. **会话管理**：长时间任务使用 `--session` 保存进度
3. **文件限制**：大文件建议分批处理
4. **网络要求**：需要稳定的网络连接访问 AI 服务

---

**文档路径**: `/Users/xiaofang/documents/www/docker/spider-proxy/docs/OpenCode CLI 开发指南.md`
