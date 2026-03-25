# Spider Proxy AI 配置管理

> 文档版本：1.0  
> 创建日期：2026-03-24  
> 任务 ID: JJC-20260324-004

---

## 📋 概述

本文档定义 AI 功能的配置管理方案，包括 API Key 管理、模型选择、限额控制、隐私设置等。

---

## 🔑 1. API Key 管理

### 配置项

| 字段 | 类型 | 说明 |
|------|------|------|
| provider | string | 提供商 (openai/anthropic/aliyun/ollama) |
| apiKey | string (加密) | API 密钥 |
| apiHost | string | 自定义 API 端点 (可选) |
| enabled | boolean | 是否启用 |
| priority | number | 优先级 (数字越小优先级越高) |

### 多 Key 轮换策略

```yaml
providers:
  - name: openai
    keys:
      - key: "sk-***1"  # 主 Key
        dailyLimit: 100
        used: 45
      - key: "sk-***2"  # 备用 Key
        dailyLimit: 100
        used: 12
    rotationStrategy: "round-robin"  # 轮换策略
    failover: true  # 自动故障转移
```

### 存储方案

**macOS (Keychain):**
```bash
# 存储
security add-generic-password -a "spider-proxy" -s "ai.openai.key1" -w "sk-***"

# 读取
security find-generic-password -a "spider-proxy" -s "ai.openai.key1" -w
```

**Linux (Secret Service):**
```bash
secrettool store --label="Spider Proxy OpenAI Key" ai.openai.key1 sk-***
```

**Windows (Credential Manager):**
```powershell
cmdkey /generic:"SpiderProxy:OpenAI:Key1" /user:"key" /pass:"sk-***"
```

### 加密方案
- 本地存储：AES-256-GCM
- 密钥派生：PBKDF2 (100000 次迭代)
- 密钥来源：用户主密码 + 随机 salt

---

## 🌐 2. API Host 配置

### 预设端点

| 提供商 | 默认端点 | 可配置 |
|--------|----------|--------|
| OpenAI | https://api.openai.com/v1 | ✅ |
| Anthropic | https://api.anthropic.com | ✅ |
| 阿里云 | https://dashscope.aliyuncs.com | ✅ |
| Ollama | http://localhost:11434 | ✅ |

### 自定义端点场景
- 企业代理：`https://proxy.company.com/openai`
- 本地服务：`http://192.168.1.100:8080`
- 第三方中转：`https://api.example.com/v1`

### 配置示例
```json
{
  "provider": "openai",
  "apiHost": "https://api.openai.com/v1",
  "timeout": 30000,
  "retryCount": 3,
  "retryDelay": 1000
}
```

---

## 🤖 3. 模型选择

### 支持模型列表

| 提供商 | 模型 | 上下文 | 输入价格 | 输出价格 | 适用场景 |
|--------|------|--------|----------|----------|----------|
| OpenAI | GPT-4o | 128K | $2.5/1M | $10/1M | 通用分析、代码生成 |
| OpenAI | GPT-4o-mini | 128K | $0.15/1M | $0.6/1M | 简单任务、批量处理 |
| Anthropic | Claude-3.5-Sonnet | 200K | $3/1M | $15/1M | 长文本、安全审查 |
| 阿里云 | Qwen-Max | 32K | ¥0.04/1K | ¥0.12/1K | 中文场景 |
| 阿里云 | Qwen-Plus | 32K | ¥0.004/1K | ¥0.012/1K | 低成本场景 |
| Ollama | Llama3-8B | 8K | 免费 | 免费 | 离线、隐私敏感 |

### 模型选择策略

```yaml
modelSelection:
  default: "gpt-4o-mini"  # 默认模型
  rules:
    - condition: "taskType == 'security-analysis'"
      model: "claude-3.5-sonnet"  # 安全分析用 Claude
    - condition: "inputLength > 50000"
      model: "claude-3.5-sonnet"  # 长文本用 Claude
    - condition: "taskType == 'code-generation'"
      model: "gpt-4o"  # 代码生成用 GPT-4o
    - condition: "privacyMode == true"
      model: "ollama/llama3"  # 隐私模式用本地模型
```

### 配置界面设计

```
┌─────────────────────────────────────┐
│  模型选择                            │
├─────────────────────────────────────┤
│  ○ GPT-4o        (最强大，适合复杂任务)  │
│  ● GPT-4o-mini   (性价比高，推荐)      │
│  ○ Claude-3.5    (长文本分析)         │
│  ○ Qwen-Max      (中文优化)           │
│  ○ Llama3 (本地)  (离线可用)           │
├─────────────────────────────────────┤
│  高级设置 ▼                          │
│  - 温度：0.7                         │
│  - 最大 Token: 4096                  │
│  - 响应格式：JSON                    │
└─────────────────────────────────────┘
```

---

## 📊 4. 请求限额

### 限额类型

| 类型 | 说明 | 配置项 |
|------|------|--------|
| 每日限额 | 每天最大调用次数 | dailyLimit |
| 每月限额 | 每月最大调用次数 | monthlyLimit |
| 并发限制 | 同时进行的请求数 | maxConcurrent |
| 速率限制 | 每分钟最大请求数 | rateLimitPerMin |

### 限额配置示例

```json
{
  "limits": {
    "openai": {
      "dailyLimit": 100,
      "monthlyLimit": 2000,
      "maxConcurrent": 5,
      "rateLimitPerMin": 10
    },
    "anthropic": {
      "dailyLimit": 50,
      "monthlyLimit": 1000,
      "maxConcurrent": 3,
      "rateLimitPerMin": 5
    }
  },
  "actions": {
    "onDailyLimitExceeded": "switch-to-backup",
    "onMonthlyLimitExceeded": "disable-until-next-month",
    "onRateLimitExceeded": "queue-and-retry"
  }
}
```

### 用量追踪

```
今日用量统计:
├─ OpenAI GPT-4o: 45/100 (45%)
├─ OpenAI GPT-4o-mini: 23/200 (11.5%)
└─ Anthropic Claude: 12/50 (24%)

本月用量统计:
├─ OpenAI: 890/2000 (44.5%)
└─ Anthropic: 340/1000 (34%)

预计耗尽时间: 15 天 (按当前速率)
```

### 超额处理策略

| 策略 | 说明 |
|------|------|
| switch-to-backup | 切换到备用 Key |
| queue-and-retry | 加入队列，次日重试 |
| disable-until-reset | 禁用直到限额重置 |
| notify-user | 通知用户确认 |

---

## 🔒 5. 隐私模式

### 隐私级别

| 级别 | 说明 | 数据发送 |
|------|------|----------|
| 🔴 完全离线 | 仅使用本地模型 | 无 |
| 🟡 脱敏模式 | 发送前脱敏处理 | 脱敏后数据 |
| 🟢 标准模式 | 正常发送 | 完整数据 |

### 脱敏规则

```yaml
sensitiveFields:
  - pattern: "password|passwd|pwd"
    action: "redact"  # 替换为 ***
  - pattern: "token|api_key|secret"
    action: "redact"
  - pattern: "email"
    action: "mask"  # 显示前缀 + ***
  - pattern: "phone"
    action: "mask"
  - pattern: "id_card|social_security"
    action: "redact"

customRules:
  - field: "authorization"
    action: "remove"  # 完全移除
  - field: "cookie"
    action: "remove"
```

### 脱敏示例

**原始请求:**
```json
{
  "username": "zhangsan",
  "password": "secret123",
  "email": "zhangsan@example.com",
  "phone": "13800138000"
}
```

**脱敏后:**
```json
{
  "username": "zhangsan",
  "password": "***",
  "email": "zhang***@example.com",
  "phone": "138****8000"
}
```

### 隐私模式配置界面

```
┌─────────────────────────────────────┐
│  隐私设置                            │
├─────────────────────────────────────┤
│  隐私模式：                          │
│  ● 标准模式 (发送完整数据)            │
│  ○ 脱敏模式 (自动隐藏敏感信息)        │
│  ○ 完全离线 (仅本地模型)              │
├─────────────────────────────────────┤
│  敏感字段识别：                      │
│  ☑ 密码                              │
│  ☑ Token/API Key                    │
│  ☑ 邮箱                              │
│  ☑ 手机号                            │
│  ☑ 身份证号                          │
│  [添加自定义规则]                    │
└─────────────────────────────────────┘
```

---

## 📁 6. 配置文件结构

### 配置文件位置

| 系统 | 路径 |
|------|------|
| macOS | `~/Library/Application Support/SpiderProxy/ai-config.json` |
| Linux | `~/.config/spider-proxy/ai-config.json` |
| Windows | `%APPDATA%\SpiderProxy\ai-config.json` |

### 完整配置示例

```json
{
  "version": "1.0",
  "providers": {
    "openai": {
      "enabled": true,
      "keys": [
        {
          "id": "key-1",
          "keyRef": "keychain:spider-proxy:openai:1",
          "dailyLimit": 100,
          "monthlyLimit": 2000,
          "priority": 1
        }
      ],
      "apiHost": "https://api.openai.com/v1",
      "models": ["gpt-4o", "gpt-4o-mini"],
      "defaultModel": "gpt-4o-mini"
    },
    "anthropic": {
      "enabled": true,
      "keys": [
        {
          "id": "key-1",
          "keyRef": "keychain:spider-proxy:anthropic:1",
          "dailyLimit": 50,
          "monthlyLimit": 1000,
          "priority": 1
        }
      ],
      "apiHost": "https://api.anthropic.com",
      "models": ["claude-3.5-sonnet"],
      "defaultModel": "claude-3.5-sonnet"
    },
    "ollama": {
      "enabled": true,
      "apiHost": "http://localhost:11434",
      "models": ["llama3:8b"],
      "defaultModel": "llama3:8b"
    }
  },
  "modelSelection": {
    "default": "gpt-4o-mini",
    "rules": []
  },
  "privacy": {
    "mode": "masked",
    "sensitiveFields": ["password", "token", "email", "phone"]
  },
  "limits": {
    "maxConcurrent": 5,
    "rateLimitPerMin": 10
  }
}
```

---

## ✅ 验收标准

- [ ] 支持至少 4 种 LLM 提供商配置
- [ ] API Key 加密存储 (系统钥匙串)
- [ ] 多 Key 自动轮换
- [ ] 每日/每月限额追踪
- [ ] 隐私模式 + 自动脱敏
- [ ] 配置界面友好易用
