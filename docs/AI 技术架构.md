# Spider Proxy AI 技术架构

> 文档版本：1.0  
> 创建日期：2026-03-24  
> 任务 ID: JJC-20260324-004

---

## 📐 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Spider Proxy App                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   UI Layer (React/Vue)                │  │
│  │  - AI 功能入口    - 结果展示    - 配置界面            │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↕                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               AI Service Layer                        │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │ 请求分析器  │ │ 数据提取器  │ │ 安全分析器  │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │  │
│  │  │ 代码生成器  │ │ 性能分析器  │ │ 搜索过滤器  │     │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘     │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↕                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              AI Configuration Manager                 │  │
│  │  - API Key 管理 (加密)  - 模型选择  - 限额控制        │  │
│  │  - 隐私设置  - 配额追踪                               │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↕                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 LLM Client                            │  │
│  │  - Prompt 构建    - 响应解析    - 错误处理            │  │
│  │  - 重试机制    - 速率限制    - 故障转移              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                  LLM API Providers                          │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   OpenAI     │ │  Anthropic   │ │   阿里云     │        │
│  │  GPT-4o      │ │  Claude-3.5  │ │   Qwen       │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐                                          │
│  │   Ollama     │  (本地部署)                               │
│  │  Llama3      │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 数据流

### AI 功能调用流程

```
1. 用户操作
   └─> 点击"AI 分析"按钮

2. 请求捕获
   └─> 从请求历史中选择目标请求
   └─> 提取：method/url/headers/body/response

3. Prompt 构建
   └─> 加载对应功能的 Prompt 模板
   └─> 注入请求数据
   └─> 应用脱敏规则 (隐私模式)

4. LLM 调用
   └─> 选择模型 (根据配置/规则)
   └─> 检查限额
   └─> 发送 API 请求
   └─> 处理响应/错误/重试

5. 结果处理
   └─> 解析 LLM 响应 (JSON/Markdown)
   └─> 数据验证
   └─> 渲染到 UI

6. 用量更新
   └─> 记录调用次数
   └─> 更新配额统计
```

### 序列图

```
用户     UI      AIService   LLMClient   LLM API
 │        │          │           │           │
 │─点击──>│          │           │           │
 │        │─获取请求─│           │           │
 │        │<─────────│           │           │
 │        │          │           │           │
 │        │─构建 Prompt─────────>│           │
 │        │          │           │           │
 │        │          │─检查限额─>│           │
 │        │          │<─────────│           │
 │        │          │           │           │
 │        │          │─调用 API────────────>│
 │        │          │           │           │
 │        │          │<────────────────────│
 │        │          │           │           │
 │        │          │─解析响应─>│           │
 │        │          │<─────────│           │
 │        │          │           │           │
 │        │<─渲染结果────────────│           │
 │<─显示──│          │           │           │
 │        │          │           │           │
 │        │─更新用量─│           │           │
```

---

## 🔐 安全设计

### 1. API Key 加密存储

**存储流程:**
```
用户输入 API Key
     ↓
生成随机 Salt (16 bytes)
     ↓
PBKDF2(主密码 + Salt, 100000 次) → 派生密钥
     ↓
AES-256-GCM 加密 API Key
     ↓
存储：{salt, iv, ciphertext, tag} 到系统钥匙串
```

**读取流程:**
```
从钥匙串读取加密数据
     ↓
用户输入主密码 (或生物识别)
     ↓
PBKDF2(主密码 + Salt) → 派生密钥
     ↓
AES-256-GCM 解密
     ↓
验证 Tag → 返回明文 API Key
```

### 2. 数据脱敏

**脱敏引擎:**
```javascript
class DataMasker {
  mask(request, rules) {
    // 1. 识别敏感字段
    const sensitiveFields = this.identifyFields(request, rules.patterns);
    
    // 2. 应用脱敏规则
    for (const field of sensitiveFields) {
      const value = getValue(request, field.path);
      const maskedValue = this.applyRule(value, field.rule);
      setValue(request, field.path, maskedValue);
    }
    
    return request;
  }
  
  applyRule(value, rule) {
    switch (rule.action) {
      case 'redact': return '***';
      case 'mask': return this.maskPartial(value);
      case 'remove': return undefined;
      default: return value;
    }
  }
}
```

**脱敏规则配置:**
```yaml
patterns:
  - name: password
    regex: /password|passwd|pwd/i
    action: redact
    
  - name: email
    regex: /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/i
    action: mask
    maskFormat: "{prefix}***@{domain}"
    
  - name: phone
    regex: /1[3-9]\d{9}/
    action: mask
    maskFormat: "{prefix}****{suffix}"
```

### 3. 本地处理优先

**策略:**
```
请求类型          处理位置
─────────────────────────────
简单格式化         本地 (无需 LLM)
敏感数据分析       本地模型 (Ollama)
通用分析          云端模型
复杂代码生成       云端模型 (GPT-4o)
```

**路由决策:**
```javascript
function selectModel(task, privacyMode) {
  if (privacyMode === 'offline') {
    return 'ollama/llama3';
  }
  
  if (task.containsSensitiveData && privacyMode === 'masked') {
    return 'ollama/llama3';  // 敏感数据用本地
  }
  
  if (task.complexity === 'high') {
    return 'gpt-4o';
  }
  
  return 'gpt-4o-mini';  // 默认
}
```

### 4. 传输安全

**所有云端调用:**
- 强制 HTTPS (TLS 1.3)
- 证书验证
- 请求签名 (HMAC)

**本地通信:**
- Ollama: localhost 仅允许
- 可选启用 mTLS

---

## 🧩 模块设计

### 1. 请求分析器 (RequestAnalyzer)

```typescript
interface RequestAnalyzer {
  analyze(request: HttpRequest): Promise<AnalysisResult>;
}

interface AnalysisResult {
  apiType: 'REST' | 'GraphQL' | 'gRPC' | 'WebSocket';
  parameters: Parameter[];
  sensitiveFields: string[];
  riskLevel: 'low' | 'medium' | 'high';
  summary: string;
}

// 实现
class LLMRequestAnalyzer implements RequestAnalyzer {
  async analyze(request: HttpRequest): Promise<AnalysisResult> {
    const prompt = this.buildPrompt(request);
    const response = await this.llm.call(prompt);
    return this.parseResponse(response);
  }
  
  buildPrompt(request: HttpRequest): string {
    return `分析以下 HTTP 请求：
- 识别 API 类型
- 解释每个参数含义
- 标记敏感字段
- 评估安全风险

请求:
${formatRequest(request)}`;
  }
}
```

### 2. 数据提取器 (DataExtractor)

```typescript
interface DataExtractor {
  extract(response: HttpResponse, query: string): Promise<ExtractedData>;
  export(data: ExtractedData, format: 'csv' | 'excel' | 'json'): Promise<Blob>;
}

class HTMLDataExtractor implements DataExtractor {
  async extract(response: HttpResponse, query: string): Promise<ExtractedData> {
    const prompt = `从以下 HTML 中提取数据：
查询：${query}

HTML:
${response.body.substring(0, 50000)}`;  // 截断避免超限
    
    const result = await this.llm.call(prompt);
    return this.parseJSON(result);
  }
}
```

### 3. 安全分析器 (SecurityAnalyzer)

```typescript
interface SecurityAnalyzer {
  analyze(request: HttpRequest, response?: HttpResponse): Promise<SecurityReport>;
}

interface SecurityReport {
  findings: Finding[];
  riskScore: number;  // 0-100
  recommendations: string[];
}

interface Finding {
  type: 'http-plaintext' | 'sensitive-exposure' | 'weak-auth' | ...;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  evidence: string;
  recommendation: string;
}
```

### 4. 代码生成器 (CodeGenerator)

```typescript
interface CodeGenerator {
  generate(request: HttpRequest, target: Target): Promise<GeneratedCode>;
}

type Target = 'curl' | 'python' | 'javascript' | 'postman' | 'pytest';

class CodeGeneratorImpl implements CodeGenerator {
  async generate(request: HttpRequest, target: Target): Promise<GeneratedCode> {
    const prompt = `生成 ${target} 代码：
请求:
${formatRequest(request)}

要求:
- 代码可直接运行
- 添加必要注释
- 处理错误情况`;
    
    return await this.llm.call(prompt);
  }
}
```

### 5. LLM 客户端 (LLMClient)

```typescript
interface LLMClient {
  call(prompt: string, options?: CallOptions): Promise<LLMResponse>;
}

interface CallOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  responseFormat?: 'text' | 'json';
  timeout?: number;
}

class MultiProviderLLMClient implements LLMClient {
  private providers: Map<string, Provider>;
  
  async call(prompt: string, options?: CallOptions): Promise<LLMResponse> {
    const provider = this.selectProvider(options?.model);
    
    // 重试逻辑
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        return await provider.call(prompt, options);
      } catch (error) {
        if (this.isRetryable(error)) {
          await this.delay(1000 * Math.pow(2, attempt));
          continue;
        }
        throw error;
      }
    }
  }
  
  private selectProvider(model?: string): Provider {
    // 根据模型名选择提供商
    if (model?.startsWith('gpt-')) return this.providers.get('openai');
    if (model?.startsWith('claude-')) return this.providers.get('anthropic');
    if (model?.startsWith('qwen-')) return this.providers.get('aliyun');
    return this.providers.get('ollama');
  }
}
```

---

## 📊 性能优化

### 1. Prompt 优化

**策略:**
- 精简上下文 (只发送必要数据)
- 使用系统消息预定义行为
- 结构化输出 (JSON Schema)

**示例:**
```javascript
// 差：发送完整请求
const prompt = JSON.stringify(fullRequest);

// 好：只发送关键字段
const prompt = `
Method: ${request.method}
Path: ${request.path}
Headers: ${JSON.stringify(relevantHeaders)}
Body: ${truncate(request.body, 2000)}
`;
```

### 2. 缓存策略

**缓存内容:**
- 相同请求的分析结果
- 常用 Prompt 模板
- 模型响应 (相同输入)

**缓存键:**
```
cacheKey = hash(model + prompt + temperature)
```

### 3. 并发控制

```yaml
concurrency:
  maxConcurrent: 5
  perProvider:
    openai: 3
    anthropic: 2
    ollama: 5
  queue:
    maxSize: 100
    timeout: 30000
```

---

## 🔧 配置管理

### 配置存储

| 配置类型 | 存储位置 | 加密 |
|----------|----------|------|
| API Keys | 系统钥匙串 | ✅ AES-256 |
| 用户偏好 | 配置文件 | ❌ |
| 用量统计 | 本地数据库 | ❌ |
| 缓存数据 | 本地缓存 | ❌ |

### 配置同步

```
本地配置 ←→ 云端同步 (可选)
  ↓
多设备共享配置
  ↓
冲突解决：最新获胜
```

---

## ✅ 验收标准

- [ ] 架构支持 4+ LLM 提供商
- [ ] API Key 加密存储
- [ ] 数据脱敏处理
- [ ] 本地模型支持 (Ollama)
- [ ] 并发控制 + 重试机制
- [ ] 响应时间 < 5s (简单任务)
