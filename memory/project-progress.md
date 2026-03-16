# BSH 项目开发进度追踪

---

## 版本: v0.0.3

> 目标: 文档完善
> 状态: ✅ 已完成 (2026-03-16)

---

## v0.0.3 任务清单 (按开发顺序)

### 阶段一：修复 README.md (Tasks 1-5)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 1.1 | 更新版本号到 0.0.2 | README.md | ✅ 完成 |
| 1.2 | 修复库使用代码示例 | README.md | ✅ 完成 |
| 1.3 | 移除过时的字段说明 | README.md | ✅ 完成 |
| 1.4 | 修复 API URL | README.md | ✅ 完成 |
| 1.5 | 更新项目结构 | README.md | ✅ 完成 |

---

### 阶段二：创建 API 文档 (Tasks 6-8)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 2.1 | 创建 API 文档结构 | doc/api.md | ✅ 完成 |
| 2.2 | 添加 API 端点说明 | doc/api.md | ✅ 完成 |
| 2.3 | 添加数据模型说明 | doc/api.md | ✅ 完成 |

---

### 阶段三：创建架构文档 (Tasks 9-11)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 3.1 | 创建架构文档结构 | doc/architecture.md | ✅ 完成 |
| 3.2 | 添加系统架构说明 | doc/architecture.md | ✅ 完成 |
| 3.3 | 添加技术选型说明 | doc/architecture.md | ✅ 完成 |

---

### 阶段四：创建贡献指南 (Tasks 12-14)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 4.1 | 创建贡献指南 | CONTRIBUTING.md | ✅ 完成 |
| 4.2 | 添加环境搭建说明 | CONTRIBUTING.md | ✅ 完成 |
| 4.3 | 添加测试说明 | CONTRIBUTING.md | ✅ 完成 |

---

### 阶段五：创建变更日志 (Tasks 15-16)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 5.1 | 创建变更日志框架 | CHANGELOG.md | ✅ 完成 |
| 5.2 | 添加版本历史 | CHANGELOG.md | ✅ 完成 |

---

## 版本: v0.0.1

> 目标: 爬取完整的上海银行理财数据并存储为 CSV

---

## 任务清单 (按开发顺序)

| ID | 任务名称 | 分支名 | 状态 | 说明 |
|----|----------|--------|------|------|
| 1 | 项目初始化 | feat/init-project | ✅ 完成 | 目录结构、配置文件创建 |
| 2 | 配置管理模块 | feat/config-module | ✅ 完成 | Settings 类实现 |
| 3 | 数据模型定义 | feat/data-models | ✅ 完成 | ProductModel 和 APIResponse |
| 4 | API 客户端 | feat/api-client | ✅ 完成 | ApiClient 类，请求参数构建 |
| 5 | 数据解析器 | feat/data-parser | ✅ 完成 | Parser 类，字段映射 |
| 6 | 年化计算器 | feat/yield-calculator | ✅ 完成 | YieldCalculator 类 |
| 7 | Repository 接口设计 | feat/repository-interface | ✅ 完成 | BaseRepository, RepositoryFactory |
| 8 | CSV Repository 实现 | feat/csv-repository | ✅ 完成 | CsvRepository 类 |
| 9 | 主流程集成 | feat/main-integration | ✅ 完成 | main.py 主入口 |
| 10 | 完整测试 | test/integration-tests | ✅ 完成 | 103 个测试，95% 覆盖率 |
| 11 | 文档完善 | docs/project-docs | ✅ 完成 | README 更新，代码注释完善 |

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

---

## 版本: v0.0.2

> 目标: 库化、Web 查看、产品 URL 定位
> 状态: ✅ 已完成 (2026-03-16)

---

## v0.0.2 任务清单 (按开发顺序)

### 阶段一：库化基础设施 (Tasks 1-13)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 1.1 | 更新 src/__init__.py 导出 | src/__init__.py | ✅ 完成 |
| 1.2 | 更新 src/models/__init__.py 导出 | src/models/__init__.py | ✅ 完成 |
| 1.3 | 更新 src/config/__init__.py 导出 | src/config/__init__.py | ✅ 完成 |
| 1.4 | 更新 src/scraper/__init__.py 导出 | src/scraper/__init__.py | ✅ 完成 |
| 1.5 | 更新 src/repository/__init__.py 导出 | src/repository/__init__.py | ✅ 完成 |
| 1.6 | 更新 src/calculator/__init__.py 导出 | src/calculator/__init__.py | ✅ 完成 |
| 1.7 | 测试模块导出 | tests/test_exports.py | ✅ 完成 |
| 2.1 | 创建 src/cli.py 基础结构 | src/cli.py | ✅ 完成 |
| 2.2 | 实现 fetch_command 函数 | src/cli.py | ✅ 完成 |
| 2.3 | 实现 web_command 函数 | src/cli.py | ✅ 完成 |
| 2.4 | 添加 pyproject.toml 入口点配置 | pyproject.toml | ✅ 完成 |
| 2.5 | 测试 CLI 命令 | tests/test_cli.py | ✅ 完成 |
| 3.1 | 更新 pyproject.toml 版本号 | pyproject.toml | ✅ 完成 |
| 3.2 | 更新 src/__init__.py 版本号 | src/__init__.py | ✅ 完成 |

---

### 阶段二：产品 URL 定位 (Tasks 14-19)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 4.1 | 研究 URL 生成规则 | doc/url-research.md | ✅ 完成 |
| 4.2 | 确定 URL 模式并验证 | doc/url-research.md | ✅ 完成 |
| 5.1 | ProductModel 添加 prd_id 字段 | src/models/product.py | ✅ 完成 |
| 5.2 | ProductModel 添加 prd_category 字段 | src/models/product.py | ✅ 完成 |
| 5.3 | ProductModel 添加 detail_page_url 字段 | src/models/product.py | ✅ 完成 |
| 5.4 | Parser 添加 build_detail_url 方法 | src/scraper/parser.py | ✅ 完成 |
| 5.5 | 更新 CSV 表头 | src/repository/csv_repository.py | ✅ 完成 |
| 5.6 | 添加 URL 字段测试 | tests/test_product.py | ✅ 完成 |

---

### 阶段三：Web 查看功能 (Tasks 20-30)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 6.1 | pyproject.toml 添加 streamlit 依赖 | pyproject.toml | ✅ 完成 |
| 6.2 | 创建 src/web/__init__.py | src/web/__init__.py | ✅ 完成 |
| 6.3 | 创建 src/web/app.py 基础结构 | src/web/app.py | ✅ 完成 |
| 6.4 | 实现 load_products 函数 | src/web/app.py | ✅ 完成 |
| 6.5 | 实现产品列表展示 | src/web/app.py | ✅ 完成 |
| 6.6 | 实现侧边栏筛选器 | src/web/app.py | ✅ 完成 |
| 7.1 | 添加数据统计面板 | src/web/app.py | ✅ 完成 |
| 7.2 | 添加产品详情视图 | src/web/app.py | ✅ 完成 |
| 7.3 | 添加搜索功能 | src/web/app.py | ✅ 完成 |
| 8.1 | 创建 tests/test_web.py | tests/test_web.py | ✅ 完成 |
| 8.2 | 实现 Web 模块单元测试 | tests/test_web.py | ✅ 完成 |

---

### 阶段四：文档与发布 (Tasks 31-34)

| ID | 任务名称 | 文件 | 状态 |
|----|----------|------|------|
| 9.1 | 更新 README.md 添加库使用说明 | README.md | ✅ 完成 |
| 9.2 | 更新 README.md 添加 Web 查看说明 | README.md | ✅ 完成 |
| 9.3 | 创建 MANIFEST.in | MANIFEST.in | ✅ 完成 |
| 9.4 | 验证 LICENSE 文件 | LICENSE | ✅ 完成 |

---

## v0.0.2 详细任务描述

### Task 1.1: 更新 src/__init__.py 导出
**文件**: `src/__init__.py`
**内容**: 添加 `__version__` 和 `__all__` 导出列表
**验收**: 可以 `import bsh; bsh.__version__` 获取版本号

### Task 1.2: 更新 src/models/__init__.py 导出
**文件**: `src/models/__init__.py`
**内容**: 添加 `__all__ = ["ProductModel"]`
**验收**: `from bsh.models import ProductModel` 成功

### Task 1.3: 更新 src/config/__init__.py 导出
**文件**: `src/config/__init__.py`
**内容**: 添加 `__all__ = ["Settings"]`
**验收**: `from bsh.config import Settings` 成功

### Task 1.4: 更新 src/scraper/__init__.py 导出
**文件**: `src/scraper/__init__.py`
**内容**: 添加 `__all__ = ["ApiClient", "Parser"]`
**验收**: `from bsh.scraper import ApiClient, Parser` 成功

### Task 1.5: 更新 src/repository/__init__.py 导出
**文件**: `src/repository/__init__.py`
**内容**: 添加 `__all__ = ["BaseRepository", "CsvRepository", "RepositoryFactory"]`
**验收**: `from bsh.repository import CsvRepository, RepositoryFactory` 成功

### Task 1.6: 更新 src/calculator/__init__.py 导出
**文件**: `src/calculator/__init__.py`
**内容**: 添加 `__all__ = ["YieldCalculator"]`
**验收**: `from bsh.calculator import YieldCalculator` 成功

### Task 1.7: 测试模块导出
**文件**: `tests/test_exports.py` (新建)
**内容**: 测试所有模块可以正确导入
**验收**: 所有测试通过

### Task 2.1: 创建 src/cli.py 基础结构
**文件**: `src/cli.py` (新建)
**内容**: 创建 CLI 模块基础结构，添加 docstring
**验收**: 文件创建成功

### Task 2.2: 实现 fetch_command 函数
**文件**: `src/cli.py`
**内容**: 实现 `fetch_command()` 函数，支持 --output 和 --page-size 参数
**验收**: 可以运行 `bsh-fetch --help`

### Task 2.3: 实现 web_command 函数
**文件**: `src/cli.py`
**内容**: 实现 `web_command()` 函数，启动 Streamlit 应用
**验收**: 可以运行 `bsh-web`

### Task 2.4: 添加 pyproject.toml 入口点配置
**文件**: `pyproject.toml`
**内容**: 添加 `[project.scripts]` 配置
**验收**: 配置格式正确

### Task 2.5: 测试 CLI 命令
**文件**: `tests/test_cli.py` (新建)
**内容**: 测试 fetch_command 和 web_command
**验收**: 所有测试通过

### Task 3.1: 更新 pyproject.toml 版本号
**文件**: `pyproject.toml`
**内容**: 将版本号从 0.0.1 更新为 0.0.2
**验收**: 版本号正确更新

### Task 3.2: 更新 src/__init__.py 版本号
**文件**: `src/__init__.py`
**内容**: 将 `__version__` 设置为 "0.0.2"
**验收**: `import bsh; print(bsh.__version__)` 输出 0.0.2

### Task 4.1: 研究 URL 生成规则
**文件**: `doc/url-research.md` (新建)
**内容**: 研究上海银行产品详情页 URL 模式
**验收**: 记录研究过程和发现

### Task 4.2: 确定 URL 模式并验证
**文件**: `doc/url-research.md`
**内容**: 确定最终的 URL 生成规则，验证 URL 有效性
**验收**: URL 规则确定且可验证

### Task 5.1: ProductModel 添加 prd_id 字段
**文件**: `src/models/product.py`
**内容**: 添加 `prd_id: str | None = None` 字段
**验收**: ProductModel 可以创建包含 prd_id 的实例

### Task 5.2: ProductModel 添加 prd_category 字段
**文件**: `src/models/product.py`
**内容**: 添加 `prd_category: str | None = None` 字段
**验收**: ProductModel 可以创建包含 prd_category 的实例

### Task 5.3: ProductModel 添加 detail_page_url 字段
**文件**: `src/models/product.py`
**内容**: 添加 `detail_page_url: str | None = Field(default=None, description="产品详情页 URL")`
**验收**: ProductModel 可以创建包含 detail_page_url 的实例

### Task 5.4: Parser 添加 build_detail_url 方法
**文件**: `src/scraper/parser.py`
**内容**: 添加 `@staticmethod def build_detail_url(prd_id, prd_category)` 方法
**验收**: URL 生成正确

### Task 5.5: 更新 CSV 表头
**文件**: `src/repository/csv_repository.py`
**内容**: 更新 `CSV_HEADER` 添加新字段
**验收**: CSV 包含新字段

### Task 5.6: 添加 URL 字段测试
**文件**: `tests/test_product.py`
**内容**: 测试新字段的创建和使用
**验收**: 所有测试通过

### Task 6.1: pyproject.toml 添加 streamlit 依赖
**文件**: `pyproject.toml`
**内容**: 添加 `streamlit>=1.29.0` 到 dependencies
**验收**: 依赖配置正确

### Task 6.2: 创建 src/web/__init__.py
**文件**: `src/web/__init__.py` (新建)
**内容**: 导出 main 函数
**验收**: `from bsh.web import main` 成功

### Task 6.3: 创建 src/web/app.py 基础结构
**文件**: `src/web/app.py` (新建)
**内容**: 创建 Streamlit 应用基础结构，设置页面配置
**验收**: Streamlit 可以启动

### Task 6.4: 实现 load_products 函数
**文件**: `src/web/app.py`
**内容**: 实现 `@st.cache_data def load_products()` 函数
**验收**: 数据正确加载

### Task 6.5: 实现产品列表展示
**文件**: `src/web/app.py`
**内容**: 使用 st.dataframe 展示产品列表
**验收**: 产品列表正确显示

### Task 6.6: 实现侧边栏筛选器
**文件**: `src/web/app.py`
**内容**: 实现代码、名称、风险等级、币种筛选器
**验收**: 筛选功能正常

### Task 7.1: 添加数据统计面板
**文件**: `src/web/app.py`
**内容**: 添加风险等级分布和币种统计图表
**验收**: 图表正确显示

### Task 7.2: 添加产品详情视图
**文件**: `src/web/app.py`
**内容**: 实现选择产品查看详情的功能
**验收**: 详情视图正常

### Task 7.3: 添加搜索功能
**文件**: `src/web/app.py`
**内容**: 添加全局搜索框
**验收**: 搜索功能正常

### Task 8.1: 创建 tests/test_web.py
**文件**: `tests/test_web.py` (新建)
**内容**: 创建测试文件基础结构
**验收**: 文件创建成功

### Task 8.2: 实现 Web 模块单元测试
**文件**: `tests/test_web.py`
**内容**: 实现加载、筛选、组合筛选、边界情况测试
**验收**: 所有测试通过

### Task 9.1: 更新 README.md 添加库使用说明
**文件**: `README.md`
**内容**: 添加"作为库使用"章节
**验收**: 文档完整准确

### Task 9.2: 更新 README.md 添加 Web 查看说明
**文件**: `README.md`
**内容**: 添加"Web 查看界面"章节
**验收**: 文档完整准确

### Task 9.3: 创建 MANIFEST.in
**文件**: `MANIFEST.in` (新建)
**内容**: 指定打包包含的文件
**验收**: 文件格式正确

### Task 9.4: 验证 LICENSE 文件
**文件**: `LICENSE`
**内容**: 确认 MIT 许可证存在
**验收**: 许可证文件完整

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-03-16 | 创建项目进度追踪文件，记录当前状态 |
| 2026-03-16 | 完成 v0.0.1 所有任务 - 11 个任务全部完成 |
| 2026-03-16 | 成功实现真实数据抓取 - 从上海银行 API 获取 260 个理财产品 |
| 2026-03-16 | 测试覆盖率达到 95% (103 个测试全部通过) |
| 2026-03-16 | 完成 v0.0.2 开发 - 34 个任务全部完成 |
| 2026-03-16 | v0.0.2 新增功能：第三方库化、CLI 命令、Web 查看界面、产品详情页 URL |
| 2026-03-16 | 修复 Web 启动问题和 URL 生成问题 |
| 2026-03-16 | 测试覆盖率 79% (130 个测试全部通过) |
| 2026-03-16 | 完成 v0.0.3 文档完善 - 16 个任务全部完成 |
| 2026-03-16 | 新增文档：API 参考文档 (doc/api.md)、架构文档 (doc/architecture.md)、贡献指南 (CONTRIBUTING.md)、变更日志 (CHANGELOG.md) |
