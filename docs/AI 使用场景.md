# Spider Proxy AI 使用场景

> 文档版本：1.0  
> 创建日期：2026-03-24  
> 任务 ID: JJC-20260324-004

---

## 📋 概述

本文档提供 Spider Proxy AI 功能的典型使用场景和 Prompt 示例，帮助用户快速上手。

---

## 🎯 场景 1: API 文档生成

### 场景描述
捕获一批 API 请求，自动生成接口文档。

### 操作步骤
1. 选择多个相关请求 (如同一模块的 API)
2. 点击 "AI 分析" → "生成文档"
3. 选择输出格式 (Markdown/Postman)
4. 导出文档

### Prompt 示例
```
你是 API 技术文档工程师。请分析以下 HTTP 请求，生成 API 文档：

要求:
1. 说明每个接口的功能
2. 列出所有请求参数 (名称、类型、必填、说明)
3. 列出所有响应字段
4. 提供使用示例
5. 标注安全风险

请求列表:
[请求 1: POST /api/login ...]
[请求 2: GET /api/user ...]
[请求 3: PUT /api/user ...]
```

### 输出示例
```markdown
# 用户模块 API 文档

## 1. 用户登录

**接口:** `POST /api/login`

**功能:** 用户认证，返回访问令牌

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 (加密传输) |

### 响应

```json
{
  "token": "eyJhbGc...",
  "expiresIn": 3600
}
```

### 安全提示
⚠️ 密码字段需加密传输，建议使用 HTTPS
```

---

## 🎯 场景 2: 数据抓取与导出

### 场景描述
从网页 API 响应中提取结构化数据，导出为 Excel。

### 操作步骤
1. 捕获商品列表 API 响应
2. 点击 "AI 提取" → 输入 "提取所有商品信息"
3. 预览提取结果
4. 导出为 Excel

### Prompt 示例
```
从以下 JSON 响应中提取商品数据：

要求:
1. 提取字段：商品 ID、名称、价格、库存、分类
2. 格式化价格 (保留 2 位小数)
3. 识别缺货商品 (库存=0)
4. 输出为 CSV 格式

响应:
{
  "products": [
    {"id": 1, "name": "商品 A", "price": 99.9, "stock": 100, "category": "数码"},
    ...
  ]
}
```

### 输出示例
```csv
id,name,price,stock,category,status
1,商品 A,99.90,100,数码,有货
2,商品 B,199.00,0,数码,缺货
3,商品 C,49.50,50,家居，有货
```

---

## 🎯 场景 3: 安全审计

### 场景描述
分析所有捕获的请求，生成安全审计报告。

### 操作步骤
1. 选择 "全部请求" 或特定时间段
2. 点击 "AI 安全分析"
3. 查看风险列表
4. 导出安全报告

### Prompt 示例
```
你是安全审计专家。请分析以下 HTTP 请求，识别安全风险：

检查项:
1. HTTP 明文传输 (非 HTTPS)
2. 敏感数据暴露 (密码/token/个人信息)
3. 弱认证机制
4. 不安全响应头
5. 信息泄露

对每个风险:
- 描述问题
- 标注严重程度 (严重/高/中/低)
- 提供修复建议

请求列表:
[请求 1: http://api.example.com/login ...]
[请求 2: POST /api/user ...]
```

### 输出示例
```markdown
# 安全审计报告

## 严重风险 (2)

### 1. HTTP 明文传输密码
**请求:** `POST http://api.example.com/login`
**问题:** 密码通过 HTTP 明文传输，可被中间人窃取
**修复:** 强制使用 HTTPS

### 2. 响应含身份证号
**请求:** `GET http://api.example.com/user/profile`
**问题:** 响应体包含完整身份证号
**修复:** 脱敏处理 (显示前 6 后 4 位)

## 高风险 (3)
...

## 修复优先级
1. [严重] 所有认证接口迁移到 HTTPS
2. [严重] 敏感字段脱敏
3. [高] 添加安全响应头
```

---

## 🎯 场景 4: 性能优化建议

### 场景描述
分析慢请求，识别瓶颈并提供优化方案。

### 操作步骤
1. 筛选响应时间 > 1s 的请求
2. 点击 "AI 性能分析"
3. 查看瓶颈分析
4. 应用优化建议

### Prompt 示例
```
你是性能优化专家。请分析以下慢请求：

要求:
1. 识别性能瓶颈 (DNS/连接/TTFB/下载)
2. 分析可能原因
3. 提供优化建议
4. 预估优化效果

请求列表:
[GET /api/search - 3.2s - TTFB: 2.8s]
[POST /api/upload - 2.1s - 下载：1.9s]
[GET /api/products - 1.5s - TTFB: 1.2s]
```

### 输出示例
```markdown
# 性能分析报告

## 慢请求 TOP3

### 1. GET /api/search - 3.2s
**瓶颈:** TTFB (2.8s)
**原因:** 数据库查询无缓存
**建议:** 
- 添加 Redis 缓存 (TTL: 5 分钟)
- 优化 SQL 查询 (添加索引)
**预估效果:** 降低至 200ms

### 2. POST /api/upload - 2.1s
**瓶颈:** 下载时间 (1.9s)
**原因:** 响应未压缩
**建议:**
- 启用 Gzip 压缩
- 使用 CDN 分发
**预估效果:** 降低至 500ms

## 总体建议
1. 启用响应压缩 (预计节省 60% 带宽)
2. 添加 CDN 缓存 (预计降低 50% 延迟)
3. 数据库查询优化 (预计降低 80% TTFB)
```

---

## 🎯 场景 5: 代码生成

### 场景描述
根据捕获的请求生成可执行代码。

### 操作步骤
1. 选择目标请求
2. 点击 "AI 生成代码"
3. 选择目标语言 (Python/JS/cURL)
4. 复制生成的代码

### Prompt 示例
```
生成 Python 代码调用以下 API:

要求:
1. 使用 requests 库
2. 添加错误处理
3. 添加必要注释
4. 敏感信息用环境变量

请求:
POST https://api.example.com/v1/chat/completions
Headers: 
  Authorization: Bearer sk-***
  Content-Type: application/json
Body:
  {"model": "gpt-4", "messages": [...]}
```

### 输出示例
```python
import requests
import os

def call_chat_api(messages):
    """
    调用 OpenAI Chat API
    
    Args:
        messages: 消息列表
    
    Returns:
        API 响应 JSON
    """
    url = "https://api.example.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": messages
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 调用失败：{e}")
        raise
```

---

## 🎯 场景 6: 自然语言搜索

### 场景描述
用中文搜索请求历史。

### 操作示例

| 自然语言查询 | AI 转换的过滤条件 |
|--------------|------------------|
| 查找所有 POST 请求 | `method == "POST"` |
| 查找失败的请求 | `status >= 400` |
| 查找发送到 api.example.com 的请求 | `host == "api.example.com"` |
| 查找包含 token 的请求 | `body contains "token" OR headers contains "token"` |
| 查找慢请求 (超过 1 秒) | `responseTime > 1000` |
| 查找昨天的登录请求 | `path contains "/login" AND time >= yesterday` |

### Prompt 示例
```
将以下自然语言查询转换为过滤条件：

查询："查找所有包含敏感信息的 POST 请求"

可用字段:
- method: 请求方法
- host: 目标主机
- path: 请求路径
- status: 响应状态码
- body: 请求体
- responseTime: 响应时间 (ms)

输出格式：JSON 过滤表达式
```

### 输出示例
```json
{
  "and": [
    {"field": "method", "op": "==", "value": "POST"},
    {"or": [
      {"field": "body", "op": "contains", "value": "password"},
      {"field": "body", "op": "contains", "value": "token"},
      {"field": "body", "op": "contains", "value": "secret"}
    ]}
  ]
}
```

---

## 🎯 场景 7: 测试用例生成

### 场景描述
根据 API 请求自动生成测试用例。

### 操作步骤
1. 选择目标 API 请求
2. 点击 "AI 生成测试"
3. 选择测试框架 (pytest/Jest)
4. 导出测试文件

### Prompt 示例
```
为以下 API 生成 pytest 测试用例：

要求:
1. 覆盖正常场景
2. 覆盖边界情况
3. 覆盖错误场景
4. 使用 pytest 框架
5. 添加断言

API:
POST /api/user
Body: {"username": string, "email": string, "age": number}
```

### 输出示例
```python
import pytest
import requests

BASE_URL = "https://api.example.com"

class TestUserAPI:
    """用户 API 测试"""
    
    def test_create_user_success(self):
        """测试成功创建用户"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "age": 25
        }
        response = requests.post(f"{BASE_URL}/api/user", json=payload)
        assert response.status_code == 201
        assert "id" in response.json()
    
    def test_create_user_missing_email(self):
        """测试缺少邮箱字段"""
        payload = {
            "username": "testuser",
            "age": 25
        }
        response = requests.post(f"{BASE_URL}/api/user", json=payload)
        assert response.status_code == 400
    
    def test_create_user_invalid_age_negative(self):
        """测试年龄为负数"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "age": -1
        }
        response = requests.post(f"{BASE_URL}/api/user", json=payload)
        assert response.status_code == 400
    
    def test_create_user_invalid_age_type(self):
        """测试年龄类型错误"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "age": "twenty"
        }
        response = requests.post(f"{BASE_URL}/api/user", json=payload)
        assert response.status_code == 400
```

---

## 🎯 场景 8: 请求聚类分析

### 场景描述
自动聚类相似请求，识别 API 使用模式。

### Prompt 示例
```
分析以下请求列表，将相似请求分组：

分组依据:
1. 相同 API 端点
2. 相同功能模块
3. 相似请求模式

对每组:
- 命名分组
- 列出成员
- 总结特征

请求列表:
[GET /api/user/1, GET /api/user/2, POST /api/user, ...]
```

### 输出示例
```markdown
# 请求聚类分析

## 组 1: 用户查询 API
**端点:** `/api/user/{id}`
**请求数:** 15
**特征:** GET 请求，获取单个用户信息

## 组 2: 用户管理 API
**端点:** `/api/user`
**请求数:** 8
**特征:** POST/PUT/DELETE，用户增删改

## 组 3: 认证 API
**端点:** `/api/auth/*`
**请求数:** 12
**特征:** 登录/登出/刷新令牌
```

---

## 💡 Prompt 编写技巧

### 1. 明确角色
```
你是 [角色]，请 [任务]...
```

### 2. 结构化输出
```
请以 JSON 格式输出，包含以下字段：
- field1: ...
- field2: ...
```

### 3. 提供示例
```
示例输入：...
示例输出：...
```

### 4. 设定约束
```
要求:
- 输出不超过 500 字
- 使用中文
- 避免专业术语
```

---

## ✅ 验收标准

- [ ] 8 大场景全部覆盖
- [ ] 每个场景有操作步骤
- [ ] 每个场景有 Prompt 示例
- [ ] 每个场景有输出示例
- [ ] 提供 Prompt 编写技巧
