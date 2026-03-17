# BSH - 上海银行理财数据爬取

爬取上海银行理财产品数据，提取产品信息并存储为 CSV 文件。

## 功能特性

- 从上海银行 API 获取真实理财产品数据
- 提取产品基本信息（名称、收益率、风险等级、起售金额等）
- 支持分页获取全部产品
- 数据存储为 CSV 格式（基于 Repository Pattern，可扩展其他存储方式）
- 完整的单元测试和集成测试（95% 测试覆盖率）

## 版本

**当前版本**: 0.0.2

详见 [doc/v0.0.2-plan.md](doc/v0.0.2-plan.md) 和 [doc/v0.0.3-plan.md](doc/v0.0.3-plan.md)

---

## 作为库使用

BSH 可以作为一个 Python 库被其他项目引用。

### 安装

```bash
pip install js-shbank
```

### 基本使用

```python
from js_shbank import ApiClient, Parser, CsvRepository, ProductModel, Settings
from js_shbank.config import Settings

# 创建配置
settings = get_settings()

# 获取产品数据
client = ApiClient(settings)

# fetch_all_products 返回所有产品记录
all_records = client.fetch_all_products()

# 解析每条产品记录
products = [Parser.parse_product(record) for record in all_records]

# 保存到 CSV
repository = CsvRepository(settings)
repository.save_batch(products)
```

### 使用数据模型

```python
from js_shbank.models import ProductModel

# 创建产品
product = ProductModel(
    prd_code="B001",
    prd_name="示例产品",
    rate="3.5",
    risk_level=2,
    curr_type="USD",
)

# 访问字段
print(product.prd_name)
print(product.rate)
print(product.detail_page_url)
```

---

## Web 查看界面

BSH 提供基于 Streamlit 的 Web 查看界面。

### 启动方式

#### 方法一：使用命令行工具

```bash
# 确保在虚拟环境中
venv\Scripts\activate  # Windows
# 或
source venv/bin/activate  # Linux/Mac

# 启动 Web 界面
shbank-web
```

#### 方法二：直接运行 Streamlit

```bash
# 确保在虚拟环境中
venv\Scripts\activate

# 启动 Web 界面
streamlit run bsh.web.app
```

### 功能说明

启动后，Streamlit 会自动打开浏览器（通常是 http://localhost:8501）。

| 功能 | 描述 |
|------|------|
| 📊 数据统计 | 显示风险等级分布柱状图和币种统计 |
| 🔍 筛选器 | 左侧边栏支持按代码、名称、风险等级、币种筛选 |
| 📋 产品列表 | 显示所有匹配的产品列表 |
| 📋 产品详情 | 从下拉框选择产品，显示完整 JSON 信息 |
| 🔗 详情链接 | 产品列表中的 `detail_page_url` 可点击跳转上海银行官网 |

### 前提条件

需要先获取产品数据：

```bash
shbank-fetch
```

这会创建 `data/products.csv` 文件，Streamlit Web 界面会自动读取该文件。

### 故障排查

#### 问题：启动后报错或显示"没有产品数据"

**原因**：CSV 文件不存在或为空

**解决方法**：

```bash
# 方式 1：指定输出路径获取数据
shbank-fetch -o data/products.csv

# 方式 2：检查默认输出目录
ls data/products.csv
```

#### 问题：Streamlit 警告 `use_container_width will be removed`

这是正常的弃用警告，不影响功能。已在代码中修复为 `width='stretch'`。

#### 问题：启动后没有数据加载

可能原因：

1. Streamlit 缓存问题

**解决方法**：

在 Streamlit 界面右上角 → 刷新按钮
或重启 Streamlit 应用

---

## 安装

### 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 获取产品数据

```bash
python -m src.main
```

数据将保存到 `data/products.csv`（或 `output/products.csv`，取决于配置）。

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|---------|------|--------|
| `API_BASE_URL` | API 基础 URL | `https://www.bosc.cn/apiQry` |
| `API_ENDPOINT` | API 端点 | `/apiPCQry/qryPcFinanceProductZh` |
| `TIMEOUT` | 请求超时时间（秒） | `30` |
| `MAX_RETRIES` | 最大重试次数 | `3` |
| `PAGE_SIZE` | 分页大小 | `50` |
| `DATA_DIR` | 数据存储目录 | `data` |

可通过创建 `.env` 文件来覆盖这些默认值。

## 项目结构

```
bsh/
├── src/
│   └── bsh/
│       ├── config/              # 配置管理
│       │   ├── __init__.py
│       │   └── settings.py    # Settings 类，支持环境变量
│       ├── models/              # Pydantic 数据模型
│       │   ├── __init__.py
│       │   └── product.py     # ProductModel, APIResponse
│       ├── repository/          # 数据存储抽象层
│       │   ├── __init__.py
│       │   ├── base.py        # BaseRepository 接口
│       │   ├── csv_repository.py # CsvRepository 实现
│       │   └── factory.py     # RepositoryFactory 工厂
│       ├── scraper/             # API 客户端和解析
│       │   ├── __init__.py
│       │   ├── api_client.py   # ApiClient 类
│       │   └── parser.py      # Parser 类
│       ├── calculator/          # 收益率计算
│       │   ├── __init__.py
│       │   └── yield_calculator.py
│       ├── web/                # Streamlit Web 应用
│       │   ├── __init__.py
│       │   └── app.py
│       ├── cli.py              # 命令行入口
│       ├── main.py             # 主入口
│       └── __init__.py         # 包导出
├── tests/                  # 测试
│   ├── test_csv_repository.py
│   ├── test_main_integration.py
│   ├── test_parser.py
│   ├── test_product.py
│   ├── test_product_url.py
│   ├── test_repository.py
│   ├── test_settings.py
│   ├── test_yield_calculator.py
│   ├── test_exports.py         # 模块导出测试
│   ├── test_cli.py            # CLI 命令测试
│   └── test_web.py             # Web 模块测试
├── data/                   # 数据存储目录
│   └── products.csv
├── doc/                    # 文档
│   ├── v0.0.2-plan.md
│   ├── v0.0.3-plan.md
│   └── url-research.md
├── memory/                 # 开发记录和计划
│   └── project-progress.md
├── pyproject.toml
├── requirements.txt
├── MANIFEST.in
├── LICENSE
└── README.md

---

## 开发

### 运行测试

```bash
pytest
```

### 查看测试覆盖率

```bash
pytest --cov=src --cov-report=html
```

覆盖率目标：≥ 80%

---

## 代码格式化

```bash
ruff format .
ruff check .
```

### 类型检查

```bash
mypy src/
```

---

## 架构设计

### Repository Pattern

项目使用 Repository Pattern 实现数据存储抽象：

- `BaseRepository`: 定义统一的数据访问接口
- `CsvRepository`: CSV 文件存储实现
- `RepositoryFactory`: 根据配置创建对应的 Repository 实例

### 数据流程

```
ApiClient (API 请求)
    ↓
Parser (数据解析)
    ↓
ProductModel (数据模型)
    ↓
CsvRepository (数据存储)
    products.csv
```

---

## API 信息

- **API 基础 URL**: `https://www.bosc.cn/apiQry`
- **产品查询端点**: `/apiPCQry/qryPcFinanceProductZh`
- **请求方式**: POST
- **请求格式**: JSON
- **响应格式**: JSON

---

## 数据字段说明

| 字段 | 说明 |
|------|------|
| `prd_code` | 产品代码 |
| `prd_name` | 产品名称 |
| `rate` | 年化收益率 |
| `rate_script` | 收益率备注 |
| `week_year_rate` | 近七日年化 |
| `month_year_rate` | 近一月年化 |
| `three_month_year_rate` | 近三月年化 |
| `half_year_year_rate` | 近半年年化 |
| `unit_rate` | 单位净值 |
| `estab_ratio` | 成立以来净值 |
| `risk_level` | 风险等级 (1-5) |
| `curr_type` | 币种 (CNY/USD) |
| `pfirst_amt` | 起售金额（元） |
| `sold_out` | 是否售罄 (0=否 1=是) |
| `prd_labels` | 产品标签 (@!@分隔) |
| `detail_page_url` | 产品详情页 URL |
| `fetched_at` | 抓取时间 |

---

## License

MIT
