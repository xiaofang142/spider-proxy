# Spider Proxy AI 功能设计

> 文档版本：1.0  
> 创建日期：2026-03-24  
> 任务 ID: JJC-20260324-004

---

## 📊 概述

本文档定义 Spider Proxy 的 7 大核心 AI 功能模块，利用 LLM 实现智能请求分析、数据提取、安全检测、代码生成等能力。

---

## 1️⃣ 智能请求分析

### 功能描述
自动分析 HTTP/HTTPS 请求，识别 API 类型、参数含义和敏感数据。

### 核心能力

| 能力 | 说明 | 实现方式 |
|------|------|----------|
| API 类型识别 | 自动判断 REST/GraphQL/gRPC | 基于 URL 结构、Content-Type、请求体特征 |
| 参数解析 | 解释每个参数的业务含义 | LLM 语义分析 |
| 敏感数据识别 | 标记密码/token/个人信息 | 正则 + LLM 双重检测 |
| 文档生成 | 自动生成请求说明 | LLM 生成 Markdown |

### 输入输出
```
输入：HTTP 请求 (method/url/headers/body)
输出：{
  apiType: "REST|GraphQL|gRPC",
  parameters: [{name, type, description, isSensitive}],
  summary: "请求功能说明",
  riskLevel: "low|medium|high"
}
```

### Prompt 示例
```
分析以下 HTTP 请求：
- 识别 API 类型
- 解释每个参数的含义
- 标记敏感字段
- 评估安全风险等级

请求：POST /api/login
Body: {"username": "test", "password": "***"}
```

---

## 2️⃣ 数据提取与结构化

### 功能描述
从 HTML/JSON/XML 响应中提取关键数据，转换为结构化格式。

### 核心能力

| 能力 | 说明 | 实现方式 |
|------|------|----------|
| HTML 提取 | 从网页中提取表格/列表/关键信息 | LLM + DOM 解析 |
| JSON 格式化 | 美化 + 字段解释 | LLM 添加注释 |
| 数据聚合 | 多请求结果合并分析 | 数据规范化 + 聚合 |
| 导出 | CSV/Excel/JSON 导出 | 格式转换 |

### 输入输出
```
输入：HTTP 响应 (body/content-type) + 提取指令
输出：{
  extractedData: [...],
  format: "json|csv|excel",
  fieldDescriptions: [{field, description}]
}
```

### 使用场景
- 抓取商品列表 → 导出 Excel
- 解析 API 响应 → 添加字段说明
- 多页数据 → 合并为单一数据集

---

## 3️⃣ 智能过滤与搜索

### 功能描述
支持自然语言搜索请求历史，AI 生成过滤规则。

### 核心能力

| 能力 | 说明 | 示例 |
|------|------|------|
| 自然语言搜索 | 用中文搜索请求 | "查找所有 POST 请求" |
| AI 过滤规则 | 根据描述生成过滤条件 | "包含 token 的请求" → `headers.authorization exists` |
| 请求聚类 | 相似请求自动分组 | 同一 API 的不同调用 |
| 异常标记 | 识别异常请求 | 状态码 5xx、超时、大响应 |

### 搜索语法
```
自然语言：查找所有失败的请求
AI 转换：status >= 500 OR error != null

自然语言：查找发送到 api.example.com 的 GET 请求
AI 转换：host == "api.example.com" AND method == "GET"
```

---

## 4️⃣ 安全分析

### 功能描述
检测不安全的 HTTP 请求，识别潜在安全风险。

### 检测项

| 检测项 | 说明 | 风险等级 |
|--------|------|----------|
| HTTP 明文传输 | 非 HTTPS 请求 | 🔴 高 |
| 敏感数据未加密 | 密码/token 明文传输 | 🔴 高 |
| 弱认证机制 | Basic Auth 无 HTTPS | 🟡 中 |
| 信息泄露 | 响应含敏感信息 | 🟡 中 |
| 不安全 Header | 缺少安全头 | 🟢 低 |

### 安全报告
```markdown
## 安全分析报告

### 高风险 (2)
1. [HTTP 明文] POST http://api.example.com/login - 密码明文传输
2. [敏感数据] GET http://api.example.com/user - 响应含身份证号

### 中风险 (3)
...

### 建议
1. 所有认证请求强制使用 HTTPS
2. 敏感字段加密传输
3. 添加安全响应头
```

---

## 5️⃣ 性能分析

### 功能描述
识别慢请求，分析原因并给出优化建议。

### 分析维度

| 维度 | 说明 |
|------|------|
| 响应时间 | 识别 >1s 的慢请求 |
| 瓶颈定位 | DNS/连接/TTFB/下载 |
| 趋势分析 | 同一接口历史性能对比 |
| 优化建议 | 缓存/压缩/并发建议 |

### 性能报告
```
慢请求 TOP5:
1. GET /api/search - 3.2s (TTFB: 2.8s) - 建议：添加缓存
2. POST /api/upload - 2.1s (下载：1.9s) - 建议：压缩响应
3. ...

优化建议:
- 启用响应压缩 (预计节省 60% 带宽)
- 添加 CDN 缓存 (预计降低 50% 延迟)
- 使用 HTTP/2 多路复用
```

---

## 6️⃣ 自动化脚本生成

### 功能描述
根据捕获的请求生成可执行代码/命令。

### 生成目标

| 目标 | 说明 | 示例 |
|------|------|------|
| cURL 命令 | 直接可执行的命令行 | `curl -X POST ...` |
| Python 代码 | requests 库调用 | `requests.post(...)` |
| JavaScript | fetch/axios 调用 | `fetch(...)` |
| Postman 集合 | 导入 Postman 使用 | JSON 格式 |
| 测试用例 | pytest/Jest 测试 | 断言响应 |

### 生成示例
```python
# 根据请求自动生成
import requests

response = requests.post(
    'https://api.example.com/login',
    headers={'Content-Type': 'application/json'},
    json={'username': 'test', 'password': '***'}
)
print(response.json())
```

---

## 7️⃣ 智能重放与测试

### 功能描述
AI 辅助修改请求参数，生成测试用例。

### 核心能力

| 能力 | 说明 |
|------|------|
| 参数建议 | AI 建议参数修改值 |
| 边界测试 | 自动生成边界值用例 |
| 模糊测试 | 生成异常输入测试 |
| 回归测试 | 自动化验证功能 |

### 测试用例生成
```
原始请求：POST /api/user {age: 25}

AI 生成的边界测试:
1. {age: -1} - 负数边界
2. {age: 0} - 零值
3. {age: 150} - 超大值
4. {age: "abc"} - 类型错误
5. {age: null} - 空值
```

---

## 🔧 技术实现

### LLM 调用流程
```
1. 用户触发 AI 功能
2. 构建 Prompt (请求数据 + 任务描述)
3. 调用 LLM API
4. 解析响应 (JSON/Markdown)
5. 渲染结果到 UI
```

### 支持模型
- OpenAI GPT-4o/GPT-4o-mini
- Anthropic Claude-3.5
- 阿里云 Qwen-Max
- 本地 Ollama (Llama3)

### 成本优化
- 简单任务 → GPT-4o-mini
- 复杂分析 → GPT-4o/Claude
- 批量处理 → 本地模型

---

## 📋 验收标准

- [ ] 7 大功能全部实现
- [ ] 支持至少 3 种 LLM 提供商
- [ ] 响应时间 < 5s (简单任务)
- [ ] 支持中文自然语言输入
- [ ] 生成代码可直接执行
