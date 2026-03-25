# Git 分支管理配置

## 分支策略

采用 Git Flow 工作流程：

```
main (生产分支)
 │
 ├─ develop (开发分支)
 │   │
 │   ├─ feature/user-auth (功能分支)
 │   ├─ feature/proxy-engine
 │   └─ bugfix/fix-crash (修复分支)
 │
 ├─ release/v1.0.0 (发布分支)
 │
 └─ hotfix/fix-login (热修分支)
```

## 分支命名规范

| 分支类型 | 前缀 | 示例 | 说明 |
|---------|------|------|------|
| 主分支 | - | `main` | 生产代码，仅接受 merge commit |
| 开发分支 | - | `develop` | 日常开发分支 |
| 功能分支 | `feature/` | `feature/proxy-engine` | 新功能开发 |
| 修复分支 | `bugfix/` | `bugfix/fix-crash` | Bug 修复 |
| 发布分支 | `release/` | `release/v1.0.0` | 发布准备 |
| 热修分支 | `hotfix/` | `hotfix/fix-login` | 紧急修复 |

## Commit 消息规范

采用 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| 类型 | 说明 |
|-----|------|
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具/配置 |

### Scope 范围

| 范围 | 说明 |
|-----|------|
| `proxy` | 代理引擎 |
| `vpn` | VPN 服务 |
| `ssl` | 证书/SSL |
| `ui` | 用户界面 |
| `traffic` | 流量管理 |
| `filter` | 过滤系统 |
| `config` | 配置 |

### 示例

```bash
# 新功能
git commit -m "feat(proxy): 添加 HTTP 代理服务器"

# Bug 修复
git commit -m "fix(vpn): 修复 VPN 连接崩溃问题"

# 文档更新
git commit -m "docs: 更新技术架构文档"

# 重构
git commit -m "refactor(traffic): 优化流量存储逻辑"
```

## 提交流程

### 功能开发流程

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/proxy-engine

# 2. 开发并提交
git add .
git commit -m "feat(proxy): 实现 HTTP 代理"
git commit -m "feat(proxy): 实现 HTTPS 代理"

# 3. 推送到远程
git push -u origin feature/proxy-engine

# 4. 创建 Pull Request
# 在 GitHub 上创建 PR: feature/proxy-engine -> develop

# 5. Code Review 通过后合并
# 由维护者合并到 develop

# 6. 删除分支
git branch -d feature/proxy-engine
git push origin --delete feature/proxy-engine
```

### 发布流程

```bash
# 1. 从 develop 创建发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. 版本号和最终测试
# 更新 pubspec.yaml version: 1.0.0+1
git commit -m "chore: bump version to 1.0.0"

# 3. 创建 Pull Request
# PR: release/v1.0.0 -> main

# 4. 合并到 main 并打 tag
git checkout main
git pull origin main
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags

# 5. 合并回 develop
git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# 6. 删除发布分支
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### 热修流程

```bash
# 1. 从 main 创建热修分支
git checkout main
git pull origin main
git checkout -b hotfix/fix-crash

# 2. 修复并提交
git add .
git commit -m "fix(vpn): 修复紧急崩溃问题"

# 3. 创建 Pull Request
# PR: hotfix/fix-crash -> main

# 4. 合并并打 tag
git checkout main
git merge --no-ff hotfix/fix-crash
git tag -a v1.0.1 -m "Hotfix for crash issue"
git push origin main --tags

# 5. 合并回 develop
git checkout develop
git merge --no-ff hotfix/fix-crash
git push origin develop

# 6. 删除热修分支
git branch -d hotfix/fix-crash
git push origin --delete hotfix/fix-crash
```

## 保护规则

### main 分支保护

- ✅ 需要 Pull Request
- ✅ 至少 1 个 reviewer
- ✅ CI 检查必须通过
- ✅ 禁止 force push
- ✅ 需要签名 commit（可选）

### develop 分支保护

- ✅ 需要 Pull Request
- ✅ CI 检查必须通过
- ✅ 禁止 force push

## 版本号规范

采用 SemVer 2.0.0 规范：`MAJOR.MINOR.PATCH`

| 版本类型 | 说明 | 示例 |
|---------|------|------|
| MAJOR | 不兼容的 API 变更 | 1.0.0 → 2.0.0 |
| MINOR | 向后兼容的功能 | 1.0.0 → 1.1.0 |
| PATCH | 向后兼容的 Bug 修复 | 1.0.0 → 1.0.1 |

**pubspec.yaml 格式:**
```yaml
version: 1.0.0+1
#       ─────┬─┬
#      MAJOR  │ │
#       ────┬─┘ │
#           │   │
#        MINOR  │
#           ───┬┘
#              │
#           PATCH (build number)
```

## 标签规范

```bash
# 正式版本
git tag -a v1.0.0 -m "Release version 1.0.0"
git tag -a v1.1.0 -m "Release version 1.1.0"

# 预发布版本
git tag -a v1.0.0-alpha.1 -m "Alpha 1"
git tag -a v1.0.0-beta.1 -m "Beta 1"
git tag -a v1.0.0-rc.1 -m "Release Candidate 1"
```

## 分支清理

定期清理已合并的分支：

```bash
# 删除本地已合并分支
git branch --merged main | grep -v "^\*\|main\|develop" | xargs -n 1 git branch -d

# 删除远程已合并分支（谨慎使用）
git fetch -p
git branch -r --merged | grep -v "main\|develop" | sed 's/origin\///' | xargs -n 1 git push origin --delete
```

---

**文档版本:** 1.0
**更新日期:** 2026-03-25
