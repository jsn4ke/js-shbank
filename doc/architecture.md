# BSH 架构设计文档

## 系统概述

BSH 是一个用于爬取上海银行理财产品数据的 Python 工具/库。系统采用分层架构设计，实现了数据获取、解析、存储的完整流程。

---

## 设计原则

### 1. 分层架构

系统采用清晰的分层结构，各层职责单一：

```
┌─────────────────────────────────────────────┐
│           CLI / Web Interface           │
│      (命令行 / Web 界面)               │
└────────────────┬───────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│           Configuration Layer            │
│      (配置管理: Settings)               │
└────────────────┬───────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│            Business Logic               │
│   (业务逻辑: Client, Parser, Calc)      │
└────────────────┬───────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│             Data Layer                │
│     (数据层: Repository, Model)          │
└─────────────────────────────────────────────┘
```

### 2. 单一职责

每个类/模块只负责一个功能领域：

| 模块 | 职责 |
|------|------|
| `ApiClient` | HTTP 请求与重试 |
| `Parser` | 数据解析与转换 |
| `Repository` | 数据持久化 |
| `Settings` | 配置管理 |

### 3. 开放封闭

对扩展开放，对修改封闭：

- **扩展**：通过继承 `BaseRepository` 添加新的存储方式
- **修改**：不需要修改核心代码即可扩展功能

### 4. 依赖注入

通过构造函数注入依赖，便于测试和替换实现：

```python
class CsvRepository(BaseRepository):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
```

---

## 核心设计模式

### Repository Pattern

**目的**：抽象数据访问逻辑，实现存储方式的可替换性

```python
# 抽象接口
class BaseRepository(ABC):
    @abstractmethod
    def save_batch(self, products) -> None:
        pass

# CSV 实现
class CsvRepository(BaseRepository):
    def save_batch(self, products) -> None:
        # CSV 文件写入逻辑
        pass

# 工厂模式创建实例
class RepositoryFactory:
    @staticmethod
    def create_repository(settings, type, **kwargs):
        if type == "csv":
            return CsvRepository(settings, **kwargs)
```

**优势**：
- 数据访问逻辑集中管理
- 易于切换存储方式（如切换到数据库）
- 便于单元测试（可 Mock Repository）

---

### Factory Pattern

**目的**：根据配置动态创建对象

```python
class RepositoryFactory:
    @staticmethod
    def create_repository(settings, repo_type="csv", **kwargs):
        if repo_type == "csv":
            return CsvRepository(settings, **kwargs)
        # 未来可扩展：
        # elif repo_type == "database":
        #     return DatabaseRepository(settings, **kwargs)
```

---

## 模块架构

### 目录结构

```
src/bsh/
├── config/          # 配置层
│   └── settings.py
├── models/          # 数据模型层
│   └── product.py
├── scraper/         # 数据获取层
│   ├── api_client.py
│   └── parser.py
├── repository/      # 数据访问层
│   ├── base.py
│   ├── csv_repository.py
│   └── factory.py
├── calculator/      # 业务计算层
│   └── yield_calculator.py
├── web/            # Web 界面层
│   └── app.py
├── cli.py          # 命令行层
├── main.py         # 主入口
└── __init__.py     # 包导出
```

### 层次说明

| 层次 | 模块 | 职责 |
|------|------|------|
| **表示层** | `cli.py`, `web/app.py` | 用户交互入口 |
| **配置层** | `config/` | 配置管理 |
| **业务层** | `scraper/`, `calculator/` | 数据获取与处理 |
| **数据层** | `repository/`, `models/` | 数据持久化 |

---

## 数据流程

### 获取数据流程

```
用户运行 shbank-fetch
    │
    ▼
1. CLI 获取配置
   └─> Settings() 读取环境变量/默认值
    │
    ▼
2. 创建 API 客户端
   └─> ApiClient(settings)
    │
    ▼
3. 分页获取数据
   └─> fetch_all_products()
        ├─> 构建请求参数 (FetchParams)
        ├─> 发送 POST 请求
        ├─> 解析响应 (APIResponse)
        └─> 提取 records
    │
    ▼
4. 解析产品数据
   └─> Parser.parse_product(record)
        ├─> 字段名转换 (camelCase → snake_case)
        ├─> 数据映射
        ├─> 生成详情页 URL
        └─> 验证 (ProductModel)
    │
    ▼
5. 保存到 CSV
   └─> CsvRepository.save_batch(products)
        ├─> 打开 CSV 文件
        ├─> 写入表头
        └─> 写入数据行
```

### Web 查看流程

```
用户运行 shbank-web
    │
    ▼
1. Streamlit 启动
   └─> 加载 app.py
    │
    ▼
2. 加载产品数据
   └─> RepositoryFactory.create_repository()
        └─> find_all()
            └─> ProductModel 列表
    │
    ▼
3. 转换为 DataFrame
   └─> pd.DataFrame([p.model_dump() for p in products])
    │
    ▼
4. 应用筛选器
   └─> 按代码、名称、风险等级、币种过滤
    │
    ▼
5. 显示结果
   ├─> 统计图表 (st.bar_chart)
   ├─> 产品列表 (st.dataframe)
   └─> 产品详情 (st.json)
```

---

## 技术选型

| 技术栈 | 选择 | 理由 |
|---------|------|------|
| **语言** | Python 3.13 | 生态丰富，适合爬取和数据处理 |
| **HTTP 客户端** | requests | 简单易用，支持会话管理 |
| **数据验证** | Pydantic | 类型安全，自动验证，文档生成 |
| **Web 框架** | Streamlit | 快速构建数据可视化界面 |
| **数据存储** | CSV | 简单易读，用户友好 |
| **测试框架** | pytest | 功能强大，插件丰富 |
| **代码检查** | ruff | 快速，配置简单 |
| **类型检查** | mypy | 静态类型检查 |

---

## 可扩展性设计

### 新增存储方式

通过继承 `BaseRepository` 实现新的存储方式：

```python
# 新增数据库存储
class DatabaseRepository(BaseRepository):
    def __init__(self, settings) -> None:
        self.db = connect_db()

    def save_batch(self, products) -> None:
        # 数据库写入逻辑
        pass

# 在工厂中注册
class RepositoryFactory:
    @staticmethod
    def create_repository(settings, repo_type):
        if repo_type == "database":
            return DatabaseRepository(settings)
```

### 新增数据源

通过继承 `ApiClient` 或创建新客户端：

```python
# 新增其他银行的数据获取
class OtherBankClient:
    def fetch_products(self) -> list[dict]:
        # 其他银行的 API 调用
        pass
```

### 新增 Web 功能

Streamlit 架构支持轻松添加新功能：

```python
# 添加导出功能
if st.button("导出 Excel"):
    export_to_excel(filtered_df)

# 添加更多图表
col3, col4 = st.columns(2)
with col3:
    st.subheader("收益分布")
    st.line_chart(rate_history)
```

---

## 安全性考虑

| 风险 | 防护措施 |
|------|----------|
| API 认证 | 目前为公开 API，无需认证 |
| 敏感信息泄露 | 不存储任何用户敏感信息 |
| 请求过载 | 内置重试机制和超时设置 |
| 数据注入 | 使用 Pydantic 验证所有输入 |

---

## 性能优化

| 优化项 | 实现 |
|--------|------|
| HTTP 会话复用 | `requests.Session()` |
| 分页批量获取 | 支持自定义 `page_size` |
| Streamlit 缓存 | `@st.cache_data` 装饰器 |
| 异步支持 | 暂未实现（可扩展） |

---

## 相关文档

- [API 参考文档](api.md)
- [README](../README.md)
- [项目进度](../memory/project-progress.md)
