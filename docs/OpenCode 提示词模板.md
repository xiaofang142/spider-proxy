# OpenCode 提示词模板

> Spider Proxy 项目专用 | 版本：1.0 | 更新时间：2026-03-24

---

## 📋 使用说明

每个模板都可以通过 `opencode run` 命令直接使用。根据场景选择合适的模板，替换 `{{变量}}` 部分。

---

## 🏗️ 一、项目创建类

### 1.1 创建新项目
```bash
opencode run "创建一个新的 Flutter 项目，项目名称 spider_proxy，描述为'HTTP/HTTPS 抓包工具'，支持 Android 和 iOS 平台，使用 Material Design 3"
```

### 1.2 初始化目录结构
```bash
opencode run "为 Flutter 项目创建标准目录结构：lib/core, lib/features, lib/ui, test/unit, test/widget, assets, scripts"
```

### 1.3 配置依赖
```bash
opencode run "分析 pubspec.yaml，添加网络请求 (http)、状态管理 (provider/riverpod)、本地存储 (hive)、日志 (logger) 依赖，使用最新稳定版本"
```

---

## 📄 二、页面生成类

### 2.1 生成页面模板
```bash
opencode run "生成一个 Flutter 页面模板，页面名 {{HomePage}}，包含 AppBar、body 内容区域、底部导航栏，使用 Provider 状态管理"
```

### 2.2 生成列表页面
```bash
opencode run "生成一个抓包列表页面，使用 ListView.builder，每个列表项显示请求方法、URL、状态码、响应时间，支持下拉刷新和无限加载"
```

### 2.3 生成详情页面
```bash
opencode run "生成一个请求详情页面，使用 TabBar 分为请求头、请求体、响应头、响应体四个标签页，支持语法高亮和复制功能"
```

### 2.4 生成设置页面
```bash
opencode run "生成设置页面，包含代理设置 (端口、主机)、证书管理、过滤规则、关于页面，使用 SettingsList 组件"
```

---

## 🔧 三、数据模型类

### 3.1 生成数据模型
```bash
opencode run "生成一个 HttpRequest 数据模型，包含字段：id, method, url, headers, body, timestamp, responseCode, responseTime，支持 JSON 序列化"
```

### 3.2 生成 Repository
```bash
opencode run "生成一个 CaptureRepository，实现 CRUD 操作：add, get, getAll, update, delete, search，使用 Hive 本地存储"
```

### 3.3 生成 Service
```bash
opencode run "生成一个 ProxyService，实现代理服务器的启动、停止、状态查询，使用单例模式"
```

---

## 🧪 四、测试用例类

### 4.1 生成单元测试
```bash
opencode run "为 {{lib/core/proxy/http_proxy.dart}} 生成单元测试，覆盖 start, stop, handleRequest 方法，使用 mockito 模拟依赖"
```

### 4.2 生成 Widget 测试
```bash
opencode run "为 {{lib/ui/pages/home_page.dart}} 生成 Widget 测试，测试页面渲染、按钮点击、状态更新"
```

### 4.3 生成集成测试
```bash
opencode run "生成集成测试，测试完整的抓包流程：启动代理 -> 发送请求 -> 捕获请求 -> 查看详情 -> 停止代理"
```

---

## 🔁 五、代码重构类

### 5.1 代码审查
```bash
opencode run "审查 {{lib/}} 目录下的代码，识别代码异味、性能问题、潜在 bug，提供改进建议"
```

### 5.2 提取方法
```bash
opencode run "分析 {{lib/ui/pages/capture_page.dart}} 中的 build 方法，提取可复用的 Widget 组件，减少代码重复"
```

### 5.3 优化性能
```bash
opencode run "分析 {{lib/features/traffic/analyzer.dart}} 的性能，识别瓶颈，提供优化建议，减少内存占用和 CPU 使用"
```

### 5.4 添加错误处理
```bash
opencode run "为 {{lib/core/proxy/proxy_server.dart}} 添加完善的错误处理，包括网络异常、证书错误、连接超时"
```

---

## 🐛 六、Bug 修复类

### 6.1 分析崩溃日志
```bash
opencode run "分析以下崩溃日志，定位问题原因，提供修复方案：{{粘贴崩溃日志}}"
```

### 6.2 修复内存泄漏
```bash
opencode run "分析 {{lib/}} 目录，识别可能的内存泄漏点 (未关闭的 Stream、未释放的 Controller、循环引用)，提供修复代码"
```

### 6.3 修复 UI 问题
```bash
opencode run "修复以下 UI 问题：{{描述问题，如'列表滚动卡顿'、'图片加载闪烁'}}，提供优化方案"
```

---

## 🤖 七、AI 功能类

### 7.1 流量分析
```bash
opencode run "生成 AI 流量分析功能，分析抓包数据，识别异常请求、性能瓶颈、安全问题，提供可视化报告"
```

### 7.2 智能建议
```bash
opencode run "生成智能建议功能，基于抓包历史，推荐过滤规则、性能优化建议、API 调用优化"
```

### 7.3 自动生成测试
```bash
opencode run "根据抓包的 API 请求，自动生成对应的 API 测试用例，包括正常场景和异常场景"
```

---

## 📦 八、数据导出类

### 8.1 HAR 导出
```bash
opencode run "生成 HAR 格式导出功能，将抓包数据转换为标准 HAR 格式，支持导出和导入"
```

### 8.2 JSON 导出
```bash
opencode run "生成 JSON 格式导出功能，导出抓包数据，支持自定义字段和过滤条件"
```

### 8.3 CSV 导出
```bash
opencode run "生成 CSV 格式导出功能，导出请求摘要信息 (方法、URL、状态码、时间)"
```

---

## 🔐 九、安全相关类

### 9.1 证书管理
```bash
opencode run "生成 CA 证书管理功能，包括证书生成、安装引导、证书导入导出、证书吊销"
```

### 9.2 SSL 拦截
```bash
opencode run "生成 SSL 拦截功能，实现 HTTPS 流量的解密和重新加密，支持自定义证书"
```

### 9.3 安全检测
```bash
opencode run "生成安全检测功能，识别不安全的 HTTP 请求、弱加密、敏感信息泄露"
```

---

## 🎨 十、UI 组件类

### 10.1 请求卡片
```bash
opencode run "生成请求卡片组件，显示请求方法 (带颜色)、URL (截断)、状态码 (带颜色)、响应时间，支持点击跳转详情"
```

### 10.2 流量图表
```bash
opencode run "生成流量统计图表组件，使用 fl_chart，显示请求数量随时间变化、方法分布、状态码分布"
```

### 10.3 过滤编辑器
```bash
opencode run "生成过滤规则编辑器组件，支持添加、编辑、删除规则，规则类型包括 URL 匹配、方法过滤、状态码过滤"
```

### 10.4 代码查看器
```bash
opencode run "生成代码查看器组件，支持 JSON、XML、HTML 语法高亮，支持折叠、展开、复制"
```

---

## 🚀 十一、CI/CD 类

### 11.1 GitHub Actions
```bash
opencode run "生成 GitHub Actions CI 配置，包含 build、test、deploy 三个 job，支持 Android 和 iOS"
```

### 11.2 发布脚本
```bash
opencode run "生成发布脚本，自动版本号递增、构建 Release、上传应用商店"
```

---

## 💡 十二、提示词编写技巧

### 好的提示词特征
1. **具体明确**：说明要做什么，而不是"优化代码"
2. **提供上下文**：附加相关文件或指定目录
3. **指定输出格式**：说明需要代码、文档还是测试
4. **分步执行**：复杂任务拆分为多个小任务

### 示例对比

❌ **不好**：
```bash
opencode run "优化这个文件"
```

✅ **好**：
```bash
opencode run -f lib/core/proxy.dart "分析这个文件的性能瓶颈，提供 3 个具体的优化建议，并给出修改后的代码"
```

❌ **不好**：
```bash
opencode run "生成测试"
```

✅ **好**：
```bash
opencode run -f lib/core/proxy/http_proxy.dart "为 HttpProxy 类生成单元测试，覆盖 start、stop、handleRequest 三个方法，使用 mockito 模拟 ServerSocket"
```

---

## 📚 十三、常用参数组合

### 快速开发
```bash
opencode run -m alibaba-coding-plan-cn/qwen3.5-plus --dir /path/to/project "任务描述"
```

### 代码审查
```bash
opencode run -f file1.dart -f file2.dart "审查这两个文件的代码质量和潜在问题"
```

### 持续开发
```bash
opencode run --continue "继续昨天的工作，完成剩余功能"
```

### 导出会话
```bash
opencode run --share "任务描述"  # 生成可分享的会话链接
```

---

**文档路径**: `/Users/xiaofang/documents/www/docker/spider-proxy/docs/OpenCode 提示词模板.md`
