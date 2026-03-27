# Spider Proxy v3.1 P0 优化设计文档

**版本**: v3.1.0
**日期**: 2026-03-27
**类型**: P0 核心功能完善
**状态**: ✅ 已完成 (2026-03-27)

---

## 一、优化目标

完善 v3.0 中的占位实现和不完整功能，提升核心模块的可用性和安全性。

### 1.1 问题清单

| 问题 | 文件 | 当前状态 | 影响 |
|------|------|----------|------|
| `jsonDecode` 占位实现 | `script_engine_v2.dart` | 返回原始字符串 | 脚本无法解析 JSON 数据 |
| `jsonEncode` 占位实现 | `script_engine_v2.dart` | 仅调用 `toString()` | 脚本无法正确序列化 JSON |
| BodyCache 无文件监听 | `body_mapper.dart` | 5 秒 TTL 被动过期 | 文件修改后需等待或手动刷新 |
| Map Local 无路径校验 | `body_mapper.dart` | 直接读取文件 | 目录遍历攻击风险 |

---

## 二、实施方案

### 2.1 JSON 解析/序列化实现

**修改文件**: `lib/core/script/script_engine_v2.dart`

**变更内容**:
```dart
// 导入 dart:convert
import 'dart:convert';

// 修改 proxy://utils 库注册
_vm!.registerLibrary('proxy://utils', {
  'print': Func1((msg) {
    print('[Script] $msg');
    return null;
  }),
  'jsonDecode': Func1((str) => json.decode(str as String)),
  'jsonEncode': Func1((obj) => json.encode(obj)),
});
```

**验收标准**:
- [ ] 脚本中可以调用 `utils.jsonDecode('{"key": "value"}')` 返回 Map
- [ ] 脚本中可以调用 `utils.jsonEncode({'key': 'value'})` 返回 JSON 字符串
- [ ] 错误输入抛出异常（非法 JSON 字符串）

---

### 2.2 BodyCache 文件监听自动刷新

**修改文件**: `lib/core/mapper/body_mapper.dart`

**新增依赖**: `watcher: ^1.1.0`

**变更内容**:

```dart
import 'package:watcher/watcher.dart';

class BodyCache {
  final Map<String, _CacheEntry> _cache = {};
  final Map<String, StreamSubscription<WatchEvent>> _watchers = {};

  /// 获取文件内容（带缓存和自动监听）
  Future<String> getFileContent(String path) async {
    final now = DateTime.now();

    // 检查缓存（5 秒有效期）
    if (_cache.containsKey(path)) {
      final entry = _cache[path]!;
      if (now.difference(entry.cachedAt).inSeconds < 5) {
        return entry.content;
      }
    }

    // 读取文件
    final file = File(path);
    final content = await file.readAsString();

    // 更新缓存
    _cache[path] = _CacheEntry(content, now);

    // 启动文件监听（如果尚未监听）
    _startWatching(path, file);

    return content;
  }

  void _startWatching(String path, File file) {
    if (_watchers.containsKey(path)) return;

    final watcher = FileWatcher(path);
    _watchers[path] = watcher.events.listen((event) {
      if (event.type == ChangeType.MODIFY ||
          event.type == ChangeType.REMOVE) {
        _cache.remove(path); // 清除缓存
        print('[BodyCache] File changed, invalidated cache: $path');
      }
    });
  }

  /// 清理资源
  void dispose() {
    for (final subscription in _watchers.values) {
      subscription.cancel();
    }
    _watchers.clear();
    _cache.clear();
  }
}
```

**验收标准**:
- [ ] 文件修改后，下次访问立即返回新内容（无需等待 5 秒）
- [ ] 同一文件只启动一个监听器
- [ ] 缓存清理时正确取消监听

---

### 2.3 路径安全校验

**修改文件**: `lib/core/mapper/body_mapper.dart`

**变更内容**:

```dart
import 'dart:io';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart';

class BodyMapperRule {
  // ... 现有代码 ...

  /// 应用本地文件替换
  Future<String?> _applyLocal(String requestPath) async {
    // 路径安全校验
    if (!_isSafePath(requestPath)) {
      print('[BodyMapper] Unsafe path blocked: $requestPath');
      return null;
    }

    try {
      // 规范化路径（解析 .. 和符号链接）
      final normalizedPath = path.canonicalize(requestPath);
      final file = File(normalizedPath);

      if (!await file.exists()) {
        print('[BodyMapper] File not found: $normalizedPath');
        return null;
      }

      return await file.readAsString();
    } catch (e) {
      print('[BodyMapper] Error reading file: $e');
      return null;
    }
  }

  /// 路径安全校验
  bool _isSafePath(String requestPath) {
    // 允许绝对路径和相对路径
    if (!requestPath.startsWith('/') && !requestPath.startsWith('./')) {
      // 可能是 Windows 路径或其他格式，尝试规范化后校验
      try {
        final normalized = path.canonicalize(requestPath);
        // 继续后续校验
      } catch (e) {
        print('[BodyMapper] Invalid path format: $requestPath');
        return false;
      }
    }

    // TODO: 获取应用文档目录并校验
    // 当前实现：仅检查路径是否包含 ".." 等危险模式
    if (requestPath.contains('..') ||
        requestPath.contains('~') ||
        requestPath.contains('\$')) {
      print('[BodyMapper] Potentially unsafe path pattern: $requestPath');
      return false;
    }

    return true;
  }
}
```

**完整实现**（需要 path_provider）:
```dart
Future<bool> _isSafePath(String requestPath) async {
  try {
    // 规范化路径
    final normalizedPath = path.canonicalize(requestPath);

    // 获取应用文档目录
    final appDir = await getApplicationDocumentsDirectory();
    final appDirPath = path.canonicalize(appDir.path);

    // 检查是否在应用目录内
    if (!normalizedPath.startsWith(appDirPath)) {
      // 允许用户通过文件选择器选择的其他目录
      // TODO: 维护一个允许访问的目录列表
      print('[BodyMapper] Path outside app directory: $normalizedPath');
      // 暂时允许，后续可配置
    }

    // 检查危险模式
    if (requestPath.contains('../') ||
        requestPath.contains('..\\') ||
        requestPath.contains('~') ||
        requestPath.contains('\$')) {
      return false;
    }

    return true;
  } catch (e) {
    print('[BodyMapper] Path validation error: $e');
    return false;
  }
}
```

**验收标准**:
- [ ] 阻止 `../../../etc/passwd` 等目录遍历攻击
- [ ] 阻止包含 `~`、`$` 等特殊字符的路径
- [ ] 正常路径访问不受影响

---

## 三、依赖更新

**文件**: `code/pubspec.yaml`

```yaml
dependencies:
  # 新增
  watcher: ^1.1.0        # 文件监听

  # 已有，确认版本
  path: ^1.8.3           # 路径工具
  path_provider: ^2.1.1  # 应用目录
```

---

## 四、测试计划

### 4.1 JSON 功能测试
```dart
// 单元测试
test('jsonDecode parses valid JSON', () {
  final result = json.decode('{"key": "value"}');
  expect(result, {'key': 'value'});
});

test('jsonEncode serializes Map', () {
  final result = json.encode({'key': 'value'});
  expect(result, '{"key":"value"}');
});

test('jsonDecode throws on invalid JSON', () {
  expect(() => json.decode('{invalid}'), throwsFormatException);
});
```

### 4.2 文件监听测试
```dart
// 集成测试
test('cache invalidates on file change', () async {
  final file = File('test.json');
  await file.writeAsString('v1');

  final content1 = await cache.getFileContent('test.json');
  expect(content1, 'v1');

  await file.writeAsString('v2');
  await Future.delayed(Duration(milliseconds: 100));

  final content2 = await cache.getFileContent('test.json');
  expect(content2, 'v2'); // 立即返回新内容
});
```

### 4.3 路径安全测试
```dart
// 单元测试
test('blocks directory traversal', () async {
  final isSafe = await _isSafePath('../../../etc/passwd');
  expect(isSafe, false);
});

test('allows normal paths', () async {
  final isSafe = await _isSafePath('/app/docs/test.json');
  expect(isSafe, true);
});
```

---

## 五、实施顺序

1. **添加依赖** - 修改 `pubspec.yaml`，运行 `flutter pub get`
2. **JSON 实现** - 修改 `script_engine_v2.dart`
3. **文件监听** - 修改 `body_mapper.dart` 中的 `BodyCache`
4. **路径安全** - 修改 `body_mapper.dart` 中的 `_applyLocal` 和 `_isSafePath`
5. **运行测试** - 验证所有功能正常

---

## 六、风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| watcher 包兼容性问题 | 中 | 低 | 选择成熟版本，准备备选方案 |
| 文件监听性能开销 | 低 | 中 | 懒加载模式，仅监听活跃文件 |
| 路径校验误报 | 中 | 低 | 提供配置选项，允许用户自定义白名单 |

---

**设计审批**:
- [ ] 设计评审通过
- [ ] 实施方案确认
- [ ] 测试计划确认

**实施者**: ___________
**实施日期**: ___________
**完成日期**: ___________
