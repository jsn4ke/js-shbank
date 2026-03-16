# BSH 项目开发进度追踪

## 版本: v0.0.1

> 目标: 爬取完整的上海银行理财数据并存储为 CSV

---

## 任务清单 (按开发顺序)

| ID | 任务名称 | 分支名 | 状态 | 说明 |
|----|----------|--------|------|------|
| 1 | 项目初始化 | feat/init-project | ✅ 完成 | 目录结构、配置文件创建 |
| 2 | 配置管理模块 | feat/config-module | ✅ 完成 | Settings 类实现 |
| 3 | 数据模型定义 | feat/data-models | ✅ 完成 | ProductModel 和 APIResponse |
| 4 | API 客户端 | feat/api-client | ⏳ 待开发 | ApiClient 类，请求参数构建 |
| 5 | 数据解析器 | feat/data-parser | ⏳ 待开发 | Parser 类，字段映射 |
| 6 | 年化计算器 | feat/yield-calculator | ⏳ 待开发 | YieldCalculator 类 |
| 7 | Repository 接口设计 | feat/repository-interface | ⏳ 待开发 | BaseRepository, RepositoryFactory |
| 8 | CSV Repository 实现 | feat/csv-repository | ⏳ 待开发 | CsvRepository 类 |
| 9 | 主流程集成 | feat/main-integration | ⏳ 待开发 | main.py 主入口 |
| 10 | 完整测试 | test/integration-tests | ⏳ 待开发 | 单元测试 + 集成测试 |
| 11 | 文档完善 | docs/project-docs | ⏳ 待开发 | README, 代码注释 |

---

## 开发流程规范 (CRITICAL)

```
每个功能点必须严格遵循以下流程:

1. [Planning]  制定小功能点实现计划
2. [Branch]    创建新分支 (从 main 拉出)
3. [TDD]       写测试 → 实现代码 → 验证通过
4. [Commit]    提交到本地分支
5. [Push]      推送到远程分支
6. [Test]      严格测试（单元/集成）
7. [Merge]     合并到 main
8. [Push]      推送 main 到远程
```

### 关键约束

| 阶段 | 要求 |
|------|------|
| Python 操作 | **所有 Python 相关操作必须在 venv 虚拟环境下执行** |
| 开发前 | 制定计划，明确小功能点 |
| 开发中 | TDD：先写测试，再写代码 |
| 提交前 | 测试必须通过，覆盖率 ≥80% |
| 合并前 | 所有测试通过 |
| 合并后 | 立即推送 main |

### 虚拟环境激活

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

## 测试要求

- **覆盖率**: ≥ 80%
- **测试类型**: 单元测试 + 集成测试
- **测试框架**: pytest
- **测试顺序**: TDD - RED → GREEN → IMPROVE

---

## Git 提交规范

```
<type>: <description>

类型: feat, fix, refactor, docs, test, chore

示例:
feat: 添加 API 客户端
fix: 修复分页逻辑错误
test: 添加 repository 测试
```

---

## 分支命名规范

- `feat/xxx`: 新功能
- `fix/xxx`: Bug 修复
- `refactor/xxx`: 重构
- `test/xxx`: 测试相关

---

## 架构约束

1. **Repository Pattern**: 数据存储必须通过抽象层实现
2. **不可变性**: 优先创建新对象，避免原地修改
3. **错误处理**: 完整的错误捕获和用户友好提示
4. **文件组织**: 高内聚低耦合，文件 ≤ 800 行

---

## 工具配置

| 工具 | 用途 |
|------|------|
| uv/pip | 包管理 |
| ruff | 代码格式化 |
| mypy | 类型检查 |
| pytest | 测试 |
| pydantic | 数据模型 |

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-03-16 | 创建项目进度追踪文件，记录当前状态 |
