# OpenCode CLI 命令示例

> Spider Proxy 项目 | 常用命令速查 | 更新时间：2026-03-24

---

## 📋 目录

1. [创建新项目](#创建新项目)
2. [生成页面模板](#生成页面模板)
3. [生成数据模型](#生成数据模型)
4. [生成 Repository](#生成-repository)
5. [生成测试用例](#生成测试用例)
6. [代码重构](#代码重构)
7. [Bug 修复](#bug-修复)

---

## 创建新项目

### 基础项目创建
```bash
# 创建 Flutter 项目
opencode run "创建一个新的 Flutter 项目，项目名称 spider_proxy，描述为'HTTP/HTTPS 抓包工具'，支持 Android 和 iOS 平台"

# 创建项目并指定目录
opencode run --dir /Users/xiaofang/documents/www/docker "在指定目录创建 Flutter 项目 spider_proxy"

# 创建项目并配置 Material 3
opencode run "创建 Flutter 项目，启用 Material Design 3，使用深色模式支持"
```

### 项目初始化
```bash
# 生成目录结构
opencode run "为 Flutter 项目创建标准目录结构：lib/core, lib/features, lib/ui, test, assets"

# 配置 pubspec.yaml
opencode run -f pubspec.yaml "配置项目依赖：http, provider, hive, logger, fl_chart，使用最新稳定版本"

# 生成 .gitignore
opencode run "生成 Flutter 项目的 .gitignore 文件，包含所有必要的忽略规则"

# 初始化 Git 仓库
opencode run "初始化 Git 仓库，创建 .gitignore，添加初始 commit"
```

### CI/CD 配置
```bash
# 生成 GitHub Actions
opencode run "生成 GitHub Actions CI 配置，包含 build 和 test 两个 job，支持 Android 和 iOS"

# 生成发布工作流
opencode run "生成 GitHub Actions 发布工作流，自动构建 APK 和 IPA，上传到 Release"
```

---

## 生成页面模板

### 首页
```bash
opencode run "生成 Flutter 首页 home_page.dart，包含：
- AppBar 显示标题和状态指示器
- 流量统计图表 (使用 fl_chart)
- 启动/停止代理按钮
- 抓包数量显示
- 底部导航栏

使用 Provider 状态管理，支持深色模式"
```

### 列表页
```bash
opencode run "生成抓包列表页 capture_page.dart，包含：
- 搜索栏
- 筛选按钮 (方法、状态码、域名)
- ListView.builder 显示请求列表
- 下拉刷新
- 无限加载

每个列表项显示：方法、URL、状态码、响应时间"
```

### 详情页
```bash
opencode run "生成请求详情页 detail_page.dart，包含：
- TabBar (请求头、请求体、响应头、响应体)
- 代码高亮显示
- 复制按钮
- 分享按钮

支持 JSON、XML、HTML 格式化"
```

### 设置页
```bash
opencode run "生成设置页 settings_page.dart，包含：
- 代理设置 (端口、主机)
- 证书管理 (生成、安装、导出)
- 过滤规则管理
- 关于页面

使用 SettingsList 组件"
```

### 通用页面模板
```bash
opencode run "生成一个通用的 Flutter 页面模板，包含：
- StatefulWidget
- Provider 监听
- AppBar
- Scaffold
- 错误处理
- 加载状态

文件位置：lib/ui/pages/{{page_name}}_page.dart"
```

---

## 生成数据模型

### 基础模型
```bash
# HttpRequest 模型
opencode run "生成 HttpRequest 数据模型，包含：
- id: String (唯一标识)
- method: String (GET/POST/PUT/DELETE)
- url: String (完整 URL)
- headers: Map<String, String>
- body: String
- timestamp: DateTime
- responseCode: int
- responseTime: int (毫秒)

支持 JSON 序列化 (json_serializable) 和 Hive 存储"

# 生成到指定文件
opencode run "生成 HttpRequest 模型到 lib/models/http_request.dart"
```

### 带注解的模型
```bash
opencode run "生成 CaptureFilter 数据模型，使用 HiveType 注解：
- id: int @HiveField(0)
- name: String @HiveField(1)
- pattern: String @HiveField(2)
- enabled: bool @HiveField(3)
- createdAt: DateTime @HiveField(4)

生成对应的 .g.dart 文件"
```

### 枚举类型
```bash
opencode run "生成 HttpMethod 枚举，包含：GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS，支持从字符串解析和转字符串"
```

---

## 生成 Repository

### 基础 Repository
```bash
opencode run "生成 CaptureRepository 类，实现以下方法：
- Future<void> init() - 初始化 Hive
- Future<void> add(HttpRequest request) - 添加请求
- Future<HttpRequest?> get(String id) - 获取单个请求
- Future<List<HttpRequest>> getAll({int limit, int offset}) - 获取列表
- Future<void> update(HttpRequest request) - 更新请求
- Future<void> delete(String id) - 删除请求
- Future<void> clear() - 清空所有
- Future<List<HttpRequest>> search(String query) - 搜索

使用 Hive 本地存储，单例模式"
```

### 带缓存的 Repository
```bash
opencode run "生成 ProxyConfigRepository 类，实现：
- 内存缓存层
- Hive 持久化层
- 配置变更通知 (StreamController)
- 默认配置
- 配置导入导出

方法：getConfig, setConfig, resetConfig, exportConfig, importConfig"
```

### Repository 测试
```bash
opencode run "为 CaptureRepository 生成单元测试，测试所有 CRUD 方法，使用 Hive 内存适配器"
```

---

## 生成测试用例

### 单元测试
```bash
# 测试 Service
opencode run -f lib/core/proxy/http_proxy.dart "为 HttpProxy 类生成单元测试：
- 测试 start() 方法
- 测试 stop() 方法
- 测试 handleRequest() 方法
- 测试异常情况 (端口占用、网络错误)

使用 mockito 模拟 ServerSocket 和 Socket"

# 测试 Repository
opencode run -f lib/repositories/capture_repository.dart "为 CaptureRepository 生成单元测试，测试所有 CRUD 操作"

# 测试 ViewModel
opencode run -f lib/viewmodels/home_viewmodel.dart "为 HomeViewModel 生成单元测试，测试状态管理和业务逻辑"
```

### Widget 测试
```bash
# 测试页面
opencode run -f lib/ui/pages/home_page.dart "为 HomePage 生成 Widget 测试：
- 测试页面渲染
- 测试按钮点击
- 测试状态更新
- 测试 Provider 集成"

# 测试组件
opencode run -f lib/ui/widgets/request_card.dart "为 RequestCard 生成 Widget 测试，测试不同状态下的显示"
```

### 集成测试
```bash
opencode run "生成集成测试 app_test.dart：
1. 启动应用
2. 点击启动代理按钮
3. 验证状态变化
4. 模拟网络请求
5. 验证抓包列表更新
6. 点击列表项
7. 验证详情页显示
8. 停止代理

使用 integration_test 包"
```

### 测试覆盖率
```bash
# 运行测试并生成覆盖率
opencode run "生成脚本 coverage.sh，运行测试并生成 HTML 覆盖率报告"
```

---

## 代码重构

### 代码审查
```bash
# 审查单个文件
opencode run -f lib/core/proxy/http_proxy.dart "审查这个文件的代码质量，识别：
- 代码异味
- 潜在 bug
- 性能问题
- 安全漏洞

提供具体的改进建议和修改后的代码"

# 审查整个目录
opencode run --dir lib/core "审查 lib/core 目录下的所有代码，提供重构建议"
```

### 提取组件
```bash
opencode run -f lib/ui/pages/capture_page.dart "分析这个文件，提取可复用的 Widget 组件：
- RequestList
- FilterBar
- SearchBar
- RequestCard

减少 build 方法的复杂度"
```

### 优化性能
```bash
# 分析内存
opencode run "分析 lib/features/traffic/analyzer.dart 的内存使用，识别内存泄漏风险，提供优化建议"

# 分析 CPU
opencode run "分析 lib/core/proxy/proxy_server.dart 的 CPU 使用，识别性能瓶颈，提供优化建议"

# 优化列表渲染
opencode run -f lib/ui/pages/capture_page.dart "优化 ListView 性能：
- 使用 const 构造函数
- 添加 RepaintBoundary
- 优化 itemBuilder
- 添加缓存"
```

### 添加类型安全
```bash
opencode run "为 lib/models/ 目录下的所有模型添加严格的类型检查，使用 freezed 包生成不可变模型"
```

### 添加错误处理
```bash
opencode run -f lib/core/proxy/proxy_server.dart "为这个文件添加完善的错误处理：
- 网络异常
- 证书错误
- 连接超时
- 资源泄漏

使用 try-catch-finally，确保资源正确释放"
```

---

## Bug 修复

### 分析崩溃
```bash
# 分析崩溃日志
opencode run "分析以下崩溃日志，定位问题原因，提供修复方案：

FlutterError caught:
Null check operator used on a null value
#0 HomePage.build (package:spider_proxy/ui/pages/home_page.dart:45)

粘贴完整的崩溃堆栈..."

# 修复空安全
opencode run -f lib/ui/pages/home_page.dart "修复这个文件中的空安全问题，添加必要的空值检查"
```

### 修复内存泄漏
```bash
opencode run "分析 lib/ 目录，识别可能的内存泄漏：
- 未关闭的 StreamController
- 未释放的 AnimationController
- 未取消的定时器
- 循环引用

提供修复代码"
```

### 修复 UI 问题
```bash
# 修复布局溢出
opencode run -f lib/ui/widgets/request_card.dart "修复这个组件的布局溢出问题，使用 Expanded 和 Flexible"

# 修复列表卡顿
opencode run -f lib/ui/pages/capture_page.dart "优化列表滚动性能，解决卡顿问题"

# 修复图片加载
opencode run "修复图片加载闪烁问题，使用 FadeInImage 和预缓存"
```

### 修复网络问题
```bash
opencode run -f lib/core/proxy/http_proxy.dart "修复网络连接问题：
- 连接超时处理
- 重试机制
- 连接池管理
- 错误恢复"
```

### 修复数据一致性问题
```bash
opencode run "修复 Hive 数据库的数据一致性问题：
- 事务处理
- 数据迁移
- 版本兼容
- 数据校验"
```

---

## 🎯 高级用法

### 多文件操作
```bash
# 同时处理多个文件
opencode run -f lib/core/proxy.dart -f lib/core/vpn.dart "分析这两个文件的依赖关系，识别循环依赖"

# 批量重构
opencode run --dir lib/ui "重构所有页面，统一使用相同的 AppBar 样式"
```

### 会话管理
```bash
# 继续上次会话
opencode run --continue "继续昨天的工作，完成剩余功能"

# 指定会话
opencode run --session <session_id> "在指定会话中继续"

# 导出会话
opencode export <session_id> > session.json

# 导入会话
opencode import session.json
```

### 模型选择
```bash
# 使用特定模型
opencode run -m alibaba-coding-plan-cn/qwen3.5-plus "生成复杂的代理服务器代码"

# 使用快速模型
opencode run -m opencode/gpt-5-nano "快速生成简单的 UI 组件"
```

### 附加文件
```bash
# 附加多个文件
opencode run -f pubspec.yaml -f analysis_options.yaml "分析项目配置，提供优化建议"

# 附加整个目录
opencode run --dir lib/core "分析核心模块，提供架构建议"
```

---

## 📊 命令速查表

| 场景 | 命令模板 |
|------|---------|
| 创建项目 | `opencode run "创建 Flutter 项目 {{name}}"` |
| 生成页面 | `opencode run "生成 {{page}} 页面，包含 {{features}}"` |
| 生成模型 | `opencode run "生成 {{model}} 模型，字段 {{fields}}"` |
| 生成测试 | `opencode run -f {{file}} "生成单元测试"` |
| 代码审查 | `opencode run -f {{file}} "审查代码质量"` |
| 重构 | `opencode run --dir {{dir}} "重构 {{aspect}}"` |
| 修复 Bug | `opencode run -f {{file}} "修复 {{issue}}"` |
| 继续会话 | `opencode run --continue "{{task}}"` |

---

**文档路径**: `/Users/xiaofang/documents/www/docker/spider-proxy/docs/OpenCode CLI 命令示例.md`
