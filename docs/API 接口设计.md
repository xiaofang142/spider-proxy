# API 接口设计

**版本:** 2.0  
**日期:** 2026-03-24  
**任务 ID:** JJC-20260324-002  
**项目名称:** Spider Proxy

---

## 一、文档概述

本文档定义 Spider Proxy 内部数据接口和组件间通信协议。

---

## 二、架构分层

```
┌─────────────────────────────────────────┐
│              UI Layer                    │
│  (Activity/Fragment/Compose)             │
├─────────────────────────────────────────┤
│            ViewModel Layer               │
│  (StateFlow, LiveData)                   │
├─────────────────────────────────────────┤
│           Domain Layer                   │
│  (Use Cases, Repository Interfaces)      │
├─────────────────────────────────────────┤
│            Data Layer                    │
│  (Repository Implementations, DTOs)      │
├─────────────────────────────────────────┤
│          Network Core                    │
│  (VPN Service, MITM Proxy)               │
└─────────────────────────────────────────┘
```

---

## 三、核心数据模型

### 3.1 流量记录 (TrafficRecord)

```kotlin
data class TrafficRecord(
    val id: Long,                    // 唯一标识
    val timestamp: Long,             // 时间戳 (ms)
    val method: String,              // HTTP 方法
    val url: String,                 // 完整 URL
    val host: String,                // 域名
    val path: String,                // 路径
    val statusCode: Int,             // 状态码
    val requestSize: Long,           // 请求大小 (bytes)
    val responseSize: Long,          // 响应大小 (bytes)
    val duration: Long,              // 耗时 (ms)
    val protocol: String,            // 协议 (HTTP/1.1, HTTP/2)
    val remoteAddress: String,       // 远程地址
    val remotePort: Int,             // 远程端口
    val mimeType: String?,           // 内容类型
    val isHttps: Boolean,            // 是否 HTTPS
    val isWebSocket: Boolean,        // 是否 WebSocket
    val tags: List<String>,          // 标签
    val note: String?,               // 用户备注
    val isFavorite: Boolean,         // 是否收藏
    val createdAt: Long,             // 创建时间
    val updatedAt: Long              // 更新时间
)
```

### 3.2 请求详情 (RequestDetail)

```kotlin
data class RequestDetail(
    val recordId: Long,
    val method: String,
    val url: String,
    val headers: Map<String, String>,
    val queryParams: Map<String, String>,
    val cookies: Map<String, String>,
    val body: ByteArray?,
    val bodyText: String?,
    val bodyMimeType: String?,
    val timestamp: Long
)
```

### 3.3 响应详情 (ResponseDetail)

```kotlin
data class ResponseDetail(
    val recordId: Long,
    val statusCode: Int,
    val statusMessage: String,
    val headers: Map<String, String>,
    val cookies: Map<String, String>,
    val body: ByteArray?,
    val bodyText: String?,
    val bodyMimeType: String?,
    val duration: Long,
    val timeline: RequestTimeline
)
```

### 3.4 请求时间线 (RequestTimeline)

```kotlin
data class RequestTimeline(
    val dnsStart: Long,
    val dnsEnd: Long,
    val connectStart: Long,
    val connectEnd: Long,
    val sslStart: Long,
    val sslEnd: Long,
    val requestStart: Long,
    val requestEnd: Long,
    val responseStart: Long,
    val responseEnd: Long
) {
    val dnsDuration: Long get() = dnsEnd - dnsStart
    val connectDuration: Long get() = connectEnd - connectStart
    val sslDuration: Long get() = sslEnd - sslStart
    val sendDuration: Long get() = requestEnd - requestStart
    val waitDuration: Long get() = responseStart - requestEnd
    val downloadDuration: Long get() = responseEnd - responseStart
    val totalDuration: Long get() = responseEnd - dnsStart
}
```

### 3.5 过滤器 (TrafficFilter)

```kotlin
data class TrafficFilter(
    val id: String,
    val name: String,
    val conditions: List<FilterCondition>,
    val logic: FilterLogic,  // AND / OR
    val isDefault: Boolean,
    val createdAt: Long
)

data class FilterCondition(
    val field: FilterField,
    val operator: FilterOperator,
    val value: String
)

enum class FilterField {
    URL, HOST, METHOD, STATUS_CODE, 
    MIME_TYPE, REQUEST_SIZE, RESPONSE_SIZE,
    DURATION, IP_ADDRESS, PROTOCOL
}

enum class FilterOperator {
    EQUALS, CONTAINS, STARTS_WITH, ENDS_WITH,
    REGEX, GREATER_THAN, LESS_THAN, BETWEEN,
    IN_RANGE
}

enum class FilterLogic { AND, OR }
```

### 3.6 脚本 (Script)

```kotlin
data class Script(
    val id: String,
    val name: String,
    val description: String?,
    val language: ScriptLanguage,
    val content: String,
    val isEnabled: Boolean,
    val triggers: List<ScriptTrigger>,
    val author: String?,
    val version: String,
    val createdAt: Long,
    val updatedAt: Long
)

enum class ScriptLanguage { JAVASCRIPT, PYTHON }

data class ScriptTrigger(
    val type: TriggerType,
    val pattern: String?  // URL 匹配模式
)

enum class TriggerType {
    ON_REQUEST, ON_RESPONSE, ON_CONNECT
}
```

---

## 四、Repository 接口

### 4.1 TrafficRepository

```kotlin
interface TrafficRepository {
    // 流量记录
    suspend fun insertRecord(record: TrafficRecord): Long
    suspend fun updateRecord(record: TrafficRecord)
    suspend fun deleteRecord(id: Long)
    suspend fun getRecord(id: Long): TrafficRecord?
    suspend fun getAllRecords(
        filter: TrafficFilter?,
        sortBy: SortField,
        sortOrder: SortOrder,
        limit: Int,
        offset: Int
    ): List<TrafficRecord>
    suspend fun getCount(filter: TrafficFilter?): Int
    suspend fun clearAll()
    
    // 请求/响应详情
    suspend fun saveRequestDetail(detail: RequestDetail)
    suspend fun saveResponseDetail(detail: ResponseDetail)
    suspend fun getRequestDetail(recordId: Long): RequestDetail?
    suspend fun getResponseDetail(recordId: Long): ResponseDetail?
    
    // 统计
    suspend fun getStatistics(timeRange: TimeRange): TrafficStatistics
    suspend fun getTopHosts(limit: Int): List<HostStats>
    suspend fun getStatusCodeDistribution(): Map<Int, Int>
}

data class TrafficStatistics(
    val totalRequests: Int,
    val totalRequestSize: Long,
    val totalResponseSize: Long,
    val avgDuration: Long,
    val requestsPerSecond: Double,
    val errorRate: Double
)

data class HostStats(
    val host: String,
    val count: Int,
    val totalSize: Long
)
```

### 4.2 FilterRepository

```kotlin
interface FilterRepository {
    suspend fun insertFilter(filter: TrafficFilter): String
    suspend fun updateFilter(filter: TrafficFilter)
    suspend fun deleteFilter(id: String)
    suspend fun getFilter(id: String): TrafficFilter?
    suspend fun getAllFilters(): List<TrafficFilter>
    suspend fun getDefaultFilter(): TrafficFilter?
    suspend fun setDefaultFilter(id: String)
}
```

### 4.3 ScriptRepository

```kotlin
interface ScriptRepository {
    suspend fun insertScript(script: Script): String
    suspend fun updateScript(script: Script)
    suspend fun deleteScript(id: String)
    suspend fun getScript(id: String): Script?
    suspend fun getAllScripts(): List<Script>
    suspend fun getEnabledScripts(): List<Script>
    suspend fun toggleScript(id: String, enabled: Boolean)
    suspend fun importScript(content: String): Script
    suspend fun exportScript(id: String): String
}
```

### 4.4 SettingsRepository

```kotlin
interface SettingsRepository {
    // 代理设置
    var proxyPort: Int
    var autoStart: Boolean
    var runInBackground: Boolean
    var ignoreSystemTraffic: Boolean
    
    // 证书设置
    var certificateInstalled: Boolean
    var certificateExpiryDate: Long?
    
    // 显示设置
    var theme: Theme
    var fontSize: FontSize
    var showTimestamp: Boolean
    
    // 存储设置
    var storageLocation: String
    var autoCleanDays: Int
    
    // 统计
    var totalCapturedRequests: Long
    var totalStoredBytes: Long
}

enum class Theme { LIGHT, DARK, SYSTEM }
enum class FontSize { SMALL, MEDIUM, LARGE }
```

---

## 五、ViewModel 接口

### 5.1 CaptureViewModel

```kotlin
class CaptureViewModel @Inject constructor(
    private val trafficRepository: TrafficRepository,
    private val captureService: CaptureService
) : ViewModel() {
    
    // 状态
    val captureState: StateFlow<CaptureState>
    val trafficRecords: StateFlow<List<TrafficRecord>>
    val statistics: StateFlow<TrafficStatistics>
    
    // 操作
    fun startCapture()
    fun stopCapture()
    fun pauseCapture()
    fun resumeCapture()
    
    fun applyFilter(filter: TrafficFilter?)
    fun clearRecords()
    fun deleteRecord(id: Long)
    fun toggleFavorite(id: Long)
}

data class CaptureState(
    val status: CaptureStatus,
    val isCapturing: Boolean,
    val recordCount: Int,
    val startTime: Long?,
    val errorMessage: String?
)

enum class CaptureStatus {
    IDLE, STARTING, CAPTURING, PAUSED, STOPPING, ERROR
}
```

### 5.2 RequestDetailViewModel

```kotlin
class RequestDetailViewModel @Inject constructor(
    private val trafficRepository: TrafficRepository
) : ViewModel() {
    
    // 状态
    val requestDetail: StateFlow<RequestDetail?>
    val responseDetail: StateFlow<ResponseDetail?>
    val isLoading: StateFlow<Boolean>
    
    // 操作
    fun loadRecord(id: Long)
    fun replayRequest(): Result<Unit>
    fun copyAsCurl(): String
    fun exportAsHAR(): File
    fun exportAsPCAP(): File
}
```

### 5.3 FilterViewModel

```kotlin
class FilterViewModel @Inject constructor(
    private val filterRepository: FilterRepository
) : ViewModel() {
    
    // 状态
    val filters: StateFlow<List<TrafficFilter>>
    val currentFilter: StateFlow<TrafficFilter?>
    
    // 操作
    fun createFilter(name: String, conditions: List<FilterCondition>)
    fun updateFilter(filter: TrafficFilter)
    fun deleteFilter(id: String)
    fun applyFilter(filter: TrafficFilter?)
    fun setAsDefault(id: String)
    fun testRegex(regex: String, testString: String): Boolean
}
```

### 5.4 ScriptViewModel

```kotlin
class ScriptViewModel @Inject constructor(
    private val scriptRepository: ScriptRepository,
    private val scriptEngine: ScriptEngine
) : ViewModel() {
    
    // 状态
    val scripts: StateFlow<List<Script>>
    val consoleOutput: StateFlow<List<ConsoleMessage>>
    val isRunning: StateFlow<Boolean>
    
    // 操作
    fun createScript(name: String, language: ScriptLanguage, template: String?)
    fun updateScript(script: Script)
    fun deleteScript(id: String)
    fun toggleScript(id: String, enabled: Boolean)
    fun runScript(id: String)
    fun stopScript()
    fun importScript(content: String)
    fun exportScript(id: String): String
}

data class ConsoleMessage(
    val level: LogLevel,
    val message: String,
    val timestamp: Long
)

enum class LogLevel { DEBUG, INFO, WARN, ERROR }
```

---

## 六、Service 接口

### 6.1 CaptureService

```kotlin
interface CaptureService {
    // 生命周期
    fun start(): Result<Unit>
    fun stop()
    fun pause()
    fun resume()
    
    // 状态
    val isRunning: Boolean
    val isPaused: Boolean
    val currentPort: Int
    
    // 回调
    fun setOnTrafficCapturedListener(listener: (TrafficRecord) -> Unit)
    fun setOnErrorListener(listener: (Throwable) -> Unit)
    
    // 配置
    fun configure(config: CaptureConfig)
}

data class CaptureConfig(
    val port: Int,
    val sslEnabled: Boolean,
    val mitmEnabled: Boolean,
    val interceptors: List<Interceptor>
)
```

### 6.2 ScriptEngine

```kotlin
interface ScriptEngine {
    // 生命周期
    fun load(script: Script)
    fun unload(scriptId: String)
    fun reload(script: Script)
    
    // 执行
    fun onRequest(request: MutableRequest): MutableRequest
    fun onResponse(response: MutableResponse): MutableResponse
    fun onConnect(connection: ConnectionInfo)
    
    // 调试
    fun setDebugMode(enabled: Boolean)
    fun setConsoleListener(listener: (ConsoleMessage) -> Unit)
    
    // 清理
    fun shutdown()
}

interface MutableRequest {
    val method: String
    val url: HttpUrl
    val headers: MutableMap<String, String>
    val body: ByteArray?
    
    fun setMethod(method: String)
    fun setUrl(url: HttpUrl)
    fun setHeader(name: String, value: String)
    fun removeHeader(name: String)
    fun setBody(body: ByteArray)
}

interface MutableResponse {
    val statusCode: Int
    val headers: MutableMap<String, String>
    val body: ByteArray?
    
    fun setStatusCode(code: Int)
    fun setHeader(name: String, value: String)
    fun removeHeader(name: String)
    fun setBody(body: ByteArray)
}
```

---

## 七、导出接口

### 7.1 ExportManager

```kotlin
interface ExportManager {
    // 单个导出
    suspend fun exportAsPCAP(record: TrafficRecord): File
    suspend fun exportAsHAR(record: TrafficRecord): File
    suspend fun exportAsCurl(record: TrafficRecord): String
    suspend fun exportAsMarkdown(record: TrafficRecord): String
    
    // 批量导出
    suspend fun exportBatchAsPCAP(records: List<TrafficRecord>): File
    suspend fun exportBatchAsHAR(records: List<TrafficRecord>): File
    suspend fun exportBatchAsMarkdown(records: List<TrafficRecord>): File
    
    // 分享
    suspend fun shareRecord(record: TrafficRecord): ShareLink
    suspend fun createShareSession(records: List<TrafficRecord>): ShareSession
}

data class ShareLink(
    val url: String,
    val expiryDate: Long,
    val password: String?,
    val viewCount: Int,
    val maxViews: Int?
)

data class ShareSession(
    val id: String,
    val name: String,
    val records: List<TrafficRecord>,
    val createdAt: Long,
    val isPublic: Boolean
)
```

---

## 八、事件总线

### 8.1 应用事件

```kotlin
sealed class AppEvent {
    // 抓包事件
    data class CaptureStarted(val port: Int) : AppEvent()
    data class CaptureStopped(val reason: String?) : AppEvent()
    data class CapturePaused(val isPaused: Boolean) : AppEvent()
    data class TrafficCaptured(val record: TrafficRecord) : AppEvent()
    
    // 证书事件
    object CertificateInstalled : AppEvent()
    object CertificateRemoved : AppEvent()
    data class CertificateError(val message: String) : AppEvent()
    
    // 脚本事件
    data class ScriptLoaded(val scriptId: String) : AppEvent()
    data class ScriptError(val scriptId: String, val error: String) : AppEvent()
    data class ScriptLog(val scriptId: String, val message: ConsoleMessage) : AppEvent()
    
    // 设置事件
    data class SettingsChanged(val key: String, val value: Any) : AppEvent()
    
    // 存储事件
    data class StorageCleared(val freedBytes: Long) : AppEvent()
    data class StorageWarning(val usedPercent: Double) : AppEvent()
}
```

### 8.2 事件总线接口

```kotlin
interface EventBus {
    fun subscribe(events: Set<KClass<out AppEvent>>, listener: (AppEvent) -> Unit)
    fun unsubscribe(listener: (AppEvent) -> Unit)
    fun publish(event: AppEvent)
}
```

---

## 九、数据库设计

### 9.1 表结构

```sql
-- 流量记录表
CREATE TABLE traffic_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    method TEXT NOT NULL,
    url TEXT NOT NULL,
    host TEXT NOT NULL,
    path TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    request_size INTEGER NOT NULL,
    response_size INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    protocol TEXT NOT NULL,
    remote_address TEXT,
    remote_port INTEGER,
    mime_type TEXT,
    is_https INTEGER NOT NULL DEFAULT 0,
    is_websocket INTEGER NOT NULL DEFAULT 0,
    tags TEXT,  -- JSON array
    note TEXT,
    is_favorite INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- 请求详情表
CREATE TABLE request_details (
    record_id INTEGER PRIMARY KEY,
    headers TEXT NOT NULL,  -- JSON object
    query_params TEXT NOT NULL,  -- JSON object
    cookies TEXT,  -- JSON object
    body BLOB,
    body_text TEXT,
    body_mime_type TEXT,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (record_id) REFERENCES traffic_records(id) ON DELETE CASCADE
);

-- 响应详情表
CREATE TABLE response_details (
    record_id INTEGER PRIMARY KEY,
    status_code INTEGER NOT NULL,
    status_message TEXT NOT NULL,
    headers TEXT NOT NULL,  -- JSON object
    cookies TEXT,  -- JSON object
    body BLOB,
    body_text TEXT,
    body_mime_type TEXT,
    duration INTEGER NOT NULL,
    timeline TEXT NOT NULL,  -- JSON object
    FOREIGN KEY (record_id) REFERENCES traffic_records(id) ON DELETE CASCADE
);

-- 过滤器表
CREATE TABLE filters (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    conditions TEXT NOT NULL,  -- JSON array
    logic TEXT NOT NULL,  -- AND/OR
    is_default INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL
);

-- 脚本表
CREATE TABLE scripts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    language TEXT NOT NULL,
    content TEXT NOT NULL,
    is_enabled INTEGER NOT NULL DEFAULT 0,
    triggers TEXT,  -- JSON array
    author TEXT,
    version TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

-- 索引
CREATE INDEX idx_records_timestamp ON traffic_records(timestamp DESC);
CREATE INDEX idx_records_host ON traffic_records(host);
CREATE INDEX idx_records_status ON traffic_records(status_code);
CREATE INDEX idx_records_favorite ON traffic_records(is_favorite);
```

---

## 十、组件通信

### 10.1 依赖注入

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "spider_proxy.db"
        ).build()
    }
    
    @Provides
    @Singleton
    fun provideTrafficRepository(db: AppDatabase): TrafficRepository {
        return TrafficRepositoryImpl(db.trafficDao())
    }
    
    @Provides
    @Singleton
    fun provideCaptureService(): CaptureService {
        return CaptureServiceImpl()
    }
}
```

### 10.2 数据流

```
┌─────────────┐
│  UI 组件     │
│  (Compose)  │
└──────┬──────┘
       │ 观察 StateFlow
       │ 调用方法
       ▼
┌─────────────┐
│  ViewModel  │
│  (业务逻辑) │
└──────┬──────┘
       │ 调用
       │ 返回数据
       ▼
┌─────────────┐
│ Repository  │
│  (数据访问) │
└──────┬──────┘
       │ CRUD
       │ 返回实体
       ▼
┌─────────────┐
│   DAO       │
│  (Room)     │
└──────┬──────┘
       │ SQL
       ▼
┌─────────────┐
│  Database   │
│  (SQLite)   │
└─────────────┘
```

---

**文档版本:** 2.0  
**最后更新:** 2026-03-24
