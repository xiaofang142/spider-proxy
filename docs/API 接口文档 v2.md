# Spider Proxy API 接口文档

**版本**: 2.0
**日期**: 2026-03-25
**项目名称**: Spider Proxy

---

## 一、接口概述

### 1.1 接口分类

| 接口类型 | 说明 | 调用方式 |
|---------|------|---------|
| Platform Channel | Flutter ↔ Android 原生通信 | MethodChannel + EventChannel |
| 内部服务接口 | Dart 服务层接口 | 类方法调用 |
| 数据存储接口 | SQLite 数据库操作 | Repository 模式 |

### 1.2 命名规范

- **MethodChannel**: `spider_proxy/<module>`
- **EventChannel**: `spider_proxy/<module>_events`
- **方法名**: camelCase 动词 + 名词 (如 `startVpn`, `installCertificate`)
- **参数**: Map 格式，键名 camelCase

---

## 二、Platform Channel 接口

### 2.1 VPN 服务接口

**Channel**: `spider_proxy/vpn`

#### 2.1.1 startVpn

启动 VPN 服务和代理服务器。

```dart
// Flutter 调用
final result = await MethodChannel('spider_proxy/vpn')
    .invokeMethod('startVpn', {
  'port': 8888,
  'proxyHost': '127.0.0.1',
  'enableHttpsDecrypt': true,
  'bypassDomains': ['google.com', 'apple.com'],
});

// Android 处理
@MethodChannel
fun startVpn(args: Map<*, *>, result: MethodChannel.Result) {
    val port = args["port"] as Int
    val enableHttps = args["enableHttpsDecrypt"] as Boolean

    // 1. 创建 VPN 服务
    // 2. 配置 TUN 设备
    // 3. 启动代理服务器
    // 4. 返回结果

    result.success(true)
}
```

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| port | int | 是 | 代理服务器监听端口 |
| proxyHost | String | 否 | 代理服务器地址 (默认 127.0.0.1) |
| enableHttpsDecrypt | bool | 否 | 是否启用 HTTPS 解密 |
| bypassDomains | List<String> | 否 | 不走代理的域名列表 |

**返回**: `bool` - 启动是否成功

---

#### 2.1.2 stopVpn

停止 VPN 服务和代理服务器。

```dart
// Flutter 调用
await MethodChannel('spider_proxy/vpn')
    .invokeMethod('stopVpn');

// Android 处理
@MethodChannel
fun stopVpn(result: MethodChannel.Result) {
    // 1. 停止代理服务器
    // 2. 关闭 TUN 设备
    // 3. 停止 VPN 服务

    result.success(null)
}
```

**参数**: 无

**返回**: `null`

---

#### 2.1.3 getVpnStatus

获取 VPN 当前运行状态。

```dart
// Flutter 调用
final status = await MethodChannel('spider_proxy/vpn')
    .invokeMethod('getVpnStatus');

// 返回值：'running' | 'stopped' | 'error'
```

**参数**: 无

**返回**: `String` - 状态枚举值

---

#### 2.1.4 getTrafficStats

获取实时流量统计。

```dart
// Flutter 调用
final stats = await MethodChannel('spider_proxy/vpn')
    .invokeMethod('getTrafficStats');

// 返回格式
{
  "uploadSpeed": 1024,      // 上传速度 (字节/秒)
  "downloadSpeed": 2048,    // 下载速度 (字节/秒)
  "totalUpload": 1048576,   // 总上传 (字节)
  "totalDownload": 2097152, // 总下载 (字节)
  "activeConnections": 15,  // 活跃连接数
  "totalRequests": 150      // 总请求数
}
```

**参数**: 无

**返回**: `Map<String, dynamic>`

---

### 2.2 证书管理接口

**Channel**: `spider_proxy/cert`

#### 2.2.1 installCertificate

安装 CA 证书到系统信任存储。

```dart
// Flutter 调用
final installed = await MethodChannel('spider_proxy/cert')
    .invokeMethod('installCertificate');

// Android 处理
@MethodChannel
fun installCertificate(result: MethodChannel.Result) {
    val intent = Intent("android.settings.CREDENTIAL_INSTALL")
    intent.putExtra("CERTIFICATE", getCACertificateBytes())
    intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    context.startActivity(intent)

    result.success(true)
}
```

**参数**: 无

**返回**: `bool` - 是否成功触发安装

---

#### 2.2.2 uninstallCertificate

卸载已安装的 CA 证书。

```dart
// Flutter 调用
final uninstalled = await MethodChannel('spider_proxy/cert')
    .invokeMethod('uninstallCertificate');

// Android 处理
@MethodChannel
fun uninstallCertificate(result: MethodChannel.Result) {
    // 1. 从 KeyStore 删除 CA 密钥
    // 2. 删除证书文件
    // 3. 提示用户到系统设置移除

    result.success(true)
}
```

**参数**: 无

**返回**: `bool` - 是否成功卸载

---

#### 2.2.3 isCertificateInstalled

检查证书是否已安装。

```dart
// Flutter 调用
final isInstalled = await MethodChannel('spider_proxy/cert')
    .invokeMethod('isCertificateInstalled');

// Android 处理
@MethodChannel
fun isCertificateInstalled(result: MethodChannel.Result) {
    // 1. 检查 KeyStore 中是否存在 CA 密钥
    // 2. 检查证书文件是否存在
    // 3. 检查证书是否在系统信任存储中

    result.success(isInstalled)
}
```

**参数**: 无

**返回**: `bool`

---

#### 2.2.4 getCertificateInfo

获取证书详细信息。

```dart
// Flutter 调用
final info = await MethodChannel('spider_proxy/cert')
    .invokeMethod('getCertificateInfo');

// 返回格式
{
  "subject": "CN=Spider Proxy CA",
  "issuer": "CN=Spider Proxy CA",
  "validFrom": "2026-03-25T00:00:00Z",
  "validTo": "2026-03-26T00:00:00Z",  // 24 小时后过期
  "serialNumber": "1234567890ABCDEF",
  "fingerprint": "SHA256:..."
}
```

**参数**: 无

**返回**: `Map<String, dynamic>`

---

### 2.3 流量记录接口

**Channel**: `spider_proxy/traffic`

#### 2.3.1 recordRequest

记录 HTTP 请求数据。

```dart
// Native → Flutter 事件推送
final channel = EventChannel('spider_proxy/traffic_events');

// Android 推送
val eventData = mapOf(
  "id" to recordId,
  "timestamp" to System.currentTimeMillis(),
  "method" to "GET",
  "url" to "https://api.example.com/data",
  "host" to "api.example.com",
  "path" to "/data",
  "statusCode" to 200,
  "requestSize" to 256,
  "responseSize" to 1024,
  "durationMs" to 120,
  "requestType" to "application/json",
  "responseType" to "application/json",
  "isHttps" to true
)

eventChannel.success(eventData)
```

**事件数据**:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 唯一标识 |
| timestamp | int | 时间戳 (毫秒) |
| method | String | HTTP 方法 |
| url | String | 完整 URL |
| host | String | 主机名 |
| path | String | 路径 |
| statusCode | int | 状态码 |
| requestSize | int | 请求大小 (字节) |
| responseSize | int | 响应大小 (字节) |
| durationMs | int | 耗时 (毫秒) |
| requestType | String? | 请求 Content-Type |
| responseType | String? | 响应 Content-Type |
| isHttps | bool | 是否 HTTPS |

---

#### 2.3.2 recordRequestBody

记录请求体数据。

```dart
// Android 推送
val eventData = mapOf(
  "recordId" to recordId,
  "body" to requestBodyString,
  "isBase64" to !isValidUtf8(requestBodyBytes)
)

eventChannel.success(eventData)
```

**参数**:
| 字段 | 类型 | 说明 |
|------|------|------|
| recordId | String | 关联的记录 ID |
| body | String | 请求体内容 |
| isBase64 | bool | 是否 Base64 编码 |

---

#### 2.3.3 recordResponseBody

记录响应体数据。

```dart
// Android 推送
val eventData = mapOf(
  "recordId" to recordId,
  "body" to responseBodyString,
  "isBase64" to !isValidUtf8(responseBodyBytes)
)

eventChannel.success(eventData)
```

---

### 2.4 设置接口

**Channel**: `spider_proxy/settings`

#### 2.4.1 getSettings

获取所有设置项。

```dart
// Flutter 调用
final settings = await MethodChannel('spider_proxy/settings')
    .invokeMethod('getSettings');

// 返回格式
{
  "proxyPort": 8888,
  "autoStart": false,
  "enableHttpsDecrypt": true,
  "bypassDomains": ["google.com", "apple.com"],
  "maxRecords": 1000,
  "theme": "system"
}
```

---

#### 2.4.2 updateSettings

更新设置项。

```dart
// Flutter 调用
await MethodChannel('spider_proxy/settings')
    .invokeMethod('updateSettings', {
  'proxyPort': 9999,
  'enableHttpsDecrypt': true,
});
```

**参数**:
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| proxyPort | int | 否 | 代理端口 |
| autoStart | bool | 否 | 是否自动启动 |
| enableHttpsDecrypt | bool | 否 | 是否启用 HTTPS 解密 |
| bypassDomains | List<String> | 否 | 绕过域名列表 |
| maxRecords | int | 否 | 最大记录数 |
| theme | String | 否 | 主题 (light/dark/system) |

**返回**: `bool` - 是否成功

---

## 三、Flutter 服务层接口

### 3.1 ProxyService

```dart
// 代理服务管理类
class ProxyService {
  // 单例
  static final ProxyService instance = ProxyService._internal();

  // ========== 生命周期管理 ==========

  /// 启动代理
  /// [port] 代理端口
  /// [enableHttps] 是否启用 HTTPS 解密
  Future<void> startProxy({
    int port = 8888,
    bool enableHttps = true,
  });

  /// 停止代理
  Future<void> stopProxy();

  /// 检查代理是否运行中
  Future<bool> isProxyRunning();

  // ========== 证书管理 ==========

  /// 安装证书
  Future<bool> installCertificate();

  /// 卸载证书
  Future<bool> uninstallCertificate();

  /// 检查证书是否已安装
  Future<bool> isCertificateInstalled();

  /// 获取证书信息
  Future<CertificateInfo?> getCertificateInfo();

  // ========== 数据流 ==========

  /// 流量记录流
  Stream<TrafficRecord> get trafficStream;

  /// 代理状态流
  Stream<ProxyStatus> get statusStream;

  /// 流量统计流
  Stream<TrafficStats> get statsStream;

  // ========== 数据操作 ==========

  /// 获取流量记录列表
  Future<List<TrafficRecord>> getRecords({
    DateTime? startTime,
    DateTime? endTime,
    String? domain,
    int? statusCode,
    String? method,
    int limit = 100,
  });

  /// 清空所有记录
  Future<void> clearAllRecords();

  /// 删除单条记录
  Future<void> deleteRecord(String recordId);
}
```

---

### 3.2 CertificateManager

```dart
// 证书管理类
class CertificateManager {
  static const MethodChannel _channel = MethodChannel('spider_proxy/cert');

  /// 安装证书到系统
  Future<bool> install() async {
    try {
      final result = await _channel.invokeMethod<bool>('installCertificate');
      return result ?? false;
    } catch (e) {
      return false;
    }
  }

  /// 从系统卸载证书
  Future<bool> uninstall() async {
    try {
      final result = await _channel.invokeMethod<bool>('uninstallCertificate');
      return result ?? false;
    } catch (e) {
      return false;
    }
  }

  /// 检查证书安装状态
  Future<bool> isInstalled() async {
    try {
      final result = await _channel.invokeMethod<bool>('isCertificateInstalled');
      return result ?? false;
    } catch (e) {
      return false;
    }
  }

  /// 获取证书详细信息
  Future<CertificateInfo?> getInfo() async {
    try {
      final result = await _channel.invokeMethod<Map>('getCertificateInfo');
      if (result == null) return null;
      return CertificateInfo.fromMap(result);
    } catch (e) {
      return null;
    }
  }

  /// 检查证书是否过期
  Future<bool> isCertificateExpired() async {
    final info = await getInfo();
    if (info == null) return true;

    return DateTime.now().isAfter(info.validTo);
  }
}

// 证书信息数据类
class CertificateInfo {
  final String subject;
  final String issuer;
  final DateTime validFrom;
  final DateTime validTo;
  final String serialNumber;
  final String fingerprint;

  CertificateInfo({
    required this.subject,
    required this.issuer,
    required this.validFrom,
    required this.validTo,
    required this.serialNumber,
    required this.fingerprint,
  });

  factory CertificateInfo.fromMap(Map map) {
    return CertificateInfo(
      subject: map['subject'] as String,
      issuer: map['issuer'] as String,
      validFrom: DateTime.parse(map['validFrom'] as String),
      validTo: DateTime.parse(map['validTo'] as String),
      serialNumber: map['serialNumber'] as String,
      fingerprint: map['fingerprint'] as String,
    );
  }

  bool get isExpired => DateTime.now().isAfter(validTo);
}
```

---

### 3.3 TrafficRepository

```dart
// 流量数据仓库
class TrafficRepository {
  static const String _tableName = 'traffic_records';
  Database? _database;

  /// 初始化数据库
  Future<void> init() async {
    final databasesPath = await getDatabasesPath();
    _database = await openDatabase(
      join(databasesPath, 'spider_proxy.db'),
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE $_tableName (
        id TEXT PRIMARY KEY,
        timestamp INTEGER NOT NULL,
        method TEXT NOT NULL,
        url TEXT NOT NULL,
        host TEXT NOT NULL,
        path TEXT NOT NULL,
        statusCode INTEGER NOT NULL,
        requestSize INTEGER NOT NULL,
        responseSize INTEGER NOT NULL,
        durationMs INTEGER NOT NULL,
        requestType TEXT,
        responseType TEXT,
        isHttps INTEGER NOT NULL,
        requestBody TEXT,
        responseBody TEXT,
        requestHeaders TEXT,
        responseHeaders TEXT
      )
    ''');

    // 创建索引
    await db.execute('CREATE INDEX idx_timestamp ON $_tableName(timestamp)');
    await db.execute('CREATE INDEX idx_host ON $_tableName(host)');
    await db.execute('CREATE INDEX idx_status_code ON $_tableName(statusCode)');
  }

  /// 插入记录
  Future<void> insert(TrafficRecord record) async {
    await _database?.insert(
      _tableName,
      record.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  /// 查询记录
  Future<List<TrafficRecord>> query({
    DateTime? startTime,
    DateTime? endTime,
    String? domain,
    int? statusCode,
    String? method,
    int limit = 100,
    int offset = 0,
  }) async {
    final whereClauses = <String>[];
    final whereArgs = <dynamic>[];

    if (startTime != null) {
      whereClauses.add('timestamp >= ?');
      whereArgs.add(startTime.millisecondsSinceEpoch);
    }

    if (endTime != null) {
      whereClauses.add('timestamp <= ?');
      whereArgs.add(endTime.millisecondsSinceEpoch);
    }

    if (domain != null) {
      whereClauses.add('host LIKE ?');
      whereArgs.add('%$domain%');
    }

    if (statusCode != null) {
      whereClauses.add('statusCode = ?');
      whereArgs.add(statusCode);
    }

    if (method != null) {
      whereClauses.add('method = ?');
      whereArgs.add(method);
    }

    final where = whereClauses.isNotEmpty ? whereClauses.join(' AND ') : null;

    final List<Map<String, dynamic>> maps = await _database?.query(
      _tableName,
      where: where,
      whereArgs: whereArgs,
      orderBy: 'timestamp DESC',
      limit: limit,
      offset: offset,
    ) ?? [];

    return List.generate(maps.length, (i) {
      return TrafficRecord.fromMap(maps[i]);
    });
  }

  /// 删除记录
  Future<void> delete(String id) async {
    await _database?.delete(
      _tableName,
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  /// 清空所有记录
  Future<void> clearAll() async {
    await _database?.delete(_tableName);
  }

  /// 获取统计信息
  Future<TrafficStats> getStats({DateTime? date}) async {
    // 实现统计查询
  }

  /// 获取记录总数
  Future<int> getCount() async {
    final result = await _database?.rawQuery('SELECT COUNT(*) FROM $_tableName');
    return result?.first.values.first as int? ?? 0;
  }
}

// 流量记录数据类
class TrafficRecord {
  final String id;
  final DateTime timestamp;
  final String method;
  final String url;
  final String host;
  final String path;
  final int statusCode;
  final int requestSize;
  final int responseSize;
  final int durationMs;
  final String? requestType;
  final String? responseType;
  final bool isHttps;
  final String? requestBody;
  final String? responseBody;
  final Map<String, String>? requestHeaders;
  final Map<String, String>? responseHeaders;

  TrafficRecord({
    required this.id,
    required this.timestamp,
    required this.method,
    required this.url,
    required this.host,
    required this.path,
    required this.statusCode,
    required this.requestSize,
    required this.responseSize,
    required this.durationMs,
    this.requestType,
    this.responseType,
    this.isHttps = false,
    this.requestBody,
    this.responseBody,
    this.requestHeaders,
    this.responseHeaders,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'timestamp': timestamp.millisecondsSinceEpoch,
      'method': method,
      'url': url,
      'host': host,
      'path': path,
      'statusCode': statusCode,
      'requestSize': requestSize,
      'responseSize': responseSize,
      'durationMs': durationMs,
      'requestType': requestType,
      'responseType': responseType,
      'isHttps': isHttps ? 1 : 0,
      'requestBody': requestBody,
      'responseBody': responseBody,
      'requestHeaders': jsonEncode(requestHeaders),
      'responseHeaders': jsonEncode(responseHeaders),
    };
  }

  factory TrafficRecord.fromMap(Map map) {
    return TrafficRecord(
      id: map['id'] as String,
      timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] as int),
      method: map['method'] as String,
      url: map['url'] as String,
      host: map['host'] as String,
      path: map['path'] as String,
      statusCode: map['statusCode'] as int,
      requestSize: map['requestSize'] as int,
      responseSize: map['responseSize'] as int,
      durationMs: map['durationMs'] as int,
      requestType: map['requestType'] as String?,
      responseType: map['responseType'] as String?,
      isHttps: (map['isHttps'] as int) == 1,
      requestBody: map['requestBody'] as String?,
      responseBody: map['responseBody'] as String?,
      requestHeaders: map['requestHeaders'] != null
          ? jsonDecode(map['requestHeaders'] as String) as Map<String, String>
          : null,
      responseHeaders: map['responseHeaders'] != null
          ? jsonDecode(map['responseHeaders'] as String) as Map<String, String>
          : null,
    );
  }
}
```

---

## 四、数据模型

### 4.1 核心模型

```dart
// 代理状态枚举
enum ProxyStatus {
  stopped,      // 已停止
  starting,     // 启动中
  running,      // 运行中
  stopping,     // 停止中
  error,        // 错误
}

// 流量统计
class TrafficStats {
  final int uploadSpeed;      // 上传速度 (字节/秒)
  final int downloadSpeed;    // 下载速度 (字节/秒)
  final int totalUpload;      // 总上传 (字节)
  final int totalDownload;    // 总下载 (字节)
  final int activeConnections;// 活跃连接数
  final int totalRequests;    // 总请求数

  TrafficStats({
    required this.uploadSpeed,
    required this.downloadSpeed,
    required this.totalUpload,
    required this.totalDownload,
    required this.activeConnections,
    required this.totalRequests,
  });
}

// 过滤设置
class FilterSettings {
  final String? domain;       // 域名过滤
  final String? method;       // 方法过滤
  final List<int>? statusCodes;// 状态码过滤
  final String? keyword;      // 关键词搜索
  final DateTime? startTime;  // 开始时间
  final DateTime? endTime;    // 结束时间

  FilterSettings({
    this.domain,
    this.method,
    this.statusCodes,
    this.keyword,
    this.startTime,
    this.endTime,
  });

  bool get isActive => domain != null || method != null ||
                       statusCodes != null || keyword != null;
}

// 主题设置
class ThemeSettings {
  final ThemeMode mode;       // light/dark/system

  ThemeSettings({required this.mode});
}

// 订阅状态
class SubscriptionStatus {
  final bool isPremium;       // 是否高级版
  final DateTime? expiryDate; // 过期日期
  final String? planId;       // 套餐 ID

  SubscriptionStatus({
    this.isPremium = false,
    this.expiryDate,
    this.planId,
  });
}
```

---

## 五、错误码定义

### 5.1 Platform Channel 错误

| 错误码 | 错误名 | 说明 |
|-------|--------|------|
| 1001 | VPN_START_FAILED | VPN 服务启动失败 |
| 1002 | VPN_STOP_FAILED | VPN 服务停止失败 |
| 1003 | PERMISSION_DENIED | 权限被拒绝 |
| 2001 | CERT_INSTALL_FAILED | 证书安装失败 |
| 2002 | CERT_UNINSTALL_FAILED | 证书卸载失败 |
| 2003 | CERT_NOT_FOUND | 证书不存在 |
| 2004 | CERT_EXPIRED | 证书已过期 |
| 3001 | PROXY_START_FAILED | 代理服务启动失败 |
| 3002 | PROXY_STOP_FAILED | 代理服务停止失败 |
| 3003 | PORT_IN_USE | 端口已被占用 |

### 5.2 Flutter 端错误处理

```dart
// 统一错误处理
class SpiderProxyException implements Exception {
  final int code;
  final String message;

  SpiderProxyException(this.code, this.message);

  @override
  String toString() => 'SpiderProxyException($code): $message';
}

// 错误码常量
class ErrorCode {
  static const int VPN_START_FAILED = 1001;
  static const int VPN_STOP_FAILED = 1002;
  static const int PERMISSION_DENIED = 1003;
  static const int CERT_INSTALL_FAILED = 2001;
  static const int CERT_UNINSTALL_FAILED = 2002;
  static const int CERT_NOT_FOUND = 2003;
  static const int CERT_EXPIRED = 2004;
  static const int PROXY_START_FAILED = 3001;
  static const int PROXY_STOP_FAILED = 3002;
  static const int PORT_IN_USE = 3003;
}

// 使用示例
try {
  await ProxyService.instance.startProxy();
} on PlatformException catch (e) {
  throw SpiderProxyException(
    e.code as int? ?? ErrorCode.PROXY_START_FAILED,
    e.message ?? 'Unknown error',
  );
}
```

---

**文档版本**: 2.0
**最后更新**: 2026-03-25
**审批状态**: 待审议
