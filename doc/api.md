# BSH API 参考文档

## 概述

BSH 通过访问上海银行理财产品查询 API 获取数据，API 提供产品列表的 JSON 格式响应。

---

## API 基础信息

| 项目 | 说明 |
|------|------|
| **基础 URL** | `https://www.bosc.cn/apiQry` |
| **端点** | `/apiPCQry/qryPcFinanceProductZh` |
| **完整 URL** | `https://www.bosc.cn/apiQry/apiPCQry/qryPcFinanceProductZh` |
| **请求方式** | POST |
| **请求格式** | JSON |
| **响应格式** | JSON |
| **字符编码** | UTF-8 |

---

## 请求参数

### FetchParams 模型

```python
from bsh.scraper import FetchParams

params = FetchParams(
    daily_dean_red_qry="",
    buy_last_day_qry="",
    rapid_red_prd_qry="",
    prd_code_name="",
    sold_out="",
    prd_time_limit_qry="",
    prd_tpl_type="",
    shelves_type_qry="",
    pfirst_amt_qry="",
    ta_code_qry="",
    client_level="",
    risk_level="",
    curr_type="",
    cross_prod_qry="2",
    size=100,
    current=1,
)
```

### 参数说明

| 字段 | 类型 | 必需 | 说明 | 默认值 |
|------|------|--------|------|--------|
| `daily_dean_red_qry` | string | 否 | 每日赎回查询 | "" |
| `buy_last_day_qry` | string | 否 | 购买最后日期查询 | "" |
| `rapid_red_prd_qry` | string | 否 | 快速赎回产品查询 | "" |
| `prd_code_name` | string | 否 | 产品代码或名称查询 | "" |
| `sold_out` | string | 否 | 是否售罄查询 | "" |
| `prd_time_limit_qry` | string | 否 | 产品期限查询 | "" |
| `prd_tpl_type` | string | 否 | 产品模板类型 | "" |
| `shelves_type_qry` | string | 否 | 上架类型查询 | "" |
| `pfirst_amt_qry` | string | 否 | 起售金额查询 | "" |
| `ta_code_qry` | string | 否 | TA代码查询 | "" |
| `client_level` | string | 否 | 客户等级查询 | "" |
| `risk_level` | string | 否 | 风险等级查询 | "" |
| `curr_type` | string | 否 | 币种查询 | "" |
| `cross_prod_qry` | string | 否 | 跨境产品查询 | "2" |
| `size` | integer | 否 | 每页数量 | 10 |
| `current` | integer | 否 | 当前页码 | 1 |

---

## 响应格式

### APIResponse 模型

```python
from bsh.models import APIResponse

response = APIResponse(
    code=200,
    success=True,
    data={
        "records": [...],
        "total": 260
    }
)
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | 响应状态码，200 表示成功 |
| `success` | boolean | 请求是否成功 |
| `data` | object | 响应数据，包含 `records` 和 `total` |

### data 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `records` | array | 产品记录数组 |
| `total` | integer | 总产品数量 |

---

## 产品数据模型 (ProductModel)

### 基本字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `prd_code` | string | 产品代码（必需） |
| `prd_name` | string | 产品名称（必需） |

### 收益率字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `rate` | string \| null | 年化收益率 |
| `rate_script` | string \| null | 收益率备注 |
| `week_year_rate` | string \| null | 近七日年化 |
| `month_year_rate` | string \| null | 近一月年化 |
| `three_month_year_rate` | string \| null | 近三月年化 |
| `half_year_year_rate` | string \| null | 近半年年化 |

### 净值字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `unit_rate` | string \| null | 单位净值 |
| `estab_ratio` | string \| null | 成立以来净值 |

### 其他信息

| 字段 | 类型 | 说明 |
|------|------|------|
| `risk_level` | integer \| null | 风险等级 0-5 |
| `curr_type` | string \| null | 币种 (CNY/USD) |
| `pfirst_amt` | float \| null | 起售金额（元） |
| `sold_out` | integer \| null | 是否售罄 (0=否 1=是) |
| `prd_labels` | string \| null | 产品标签 (@!@分隔) |

### URL 相关

| 字段 | 类型 | 说明 |
|------|------|------|
| `detail_page_url` | string \| null | 产品详情页 URL |

### 元数据

| 字段 | 类型 | 说明 |
|------|------|------|
| `fetched_at` | datetime | 抓取时间 |

---

## 使用示例

### 基本请求

```python
from bsh import ApiClient, Parser
from bsh.config import Settings

# 创建配置
settings = Settings()
settings.page_size = 50

# 创建客户端
client = ApiClient(settings)

# 获取产品
all_records = client.fetch_all_products()
print(f"共获取 {len(all_records)} 条产品")

# 解析产品
products = [Parser.parse_product(record) for record in all_records]
```

### 分页请求

```python
from bsh.scraper import ApiClient, FetchParams
from bsh.config import Settings

settings = Settings()
client = ApiClient(settings)

# 获取第一页
params = FetchParams(size=50, current=1)
response = client.fetch_products(params)

print(f"当前页: {params.current}")
print(f"总数: {response.data['total']}")
print(f"本页记录数: {len(response.data['records'])}")
```

### 带筛选条件的请求

```python
params = FetchParams(
    risk_level="2",        # 只查询R2低风险产品
    curr_type="CNY",       # 只查询人民币产品
    sold_out="0",          # 只查询未售罄产品
    size=100,
    current=1
)
```

---

## 错误处理

### HTTP 错误

当 HTTP 状态码不是 200 时，会抛出 `RuntimeError`：

```python
try:
    response = client.fetch_products(params)
except RuntimeError as e:
    print(f"HTTP 错误: {e}")
```

### 网络错误

当网络请求失败时，会抛出 `requests.RequestException`：

```python
try:
    response = client.fetch_products(params)
except requests.RequestException as e:
    print(f"网络错误: {e}")
```

---

## 限制

| 限制项 | 说明 |
|--------|------|
| 请求频率 | 建议每次请求间隔至少 1 秒 |
| 单页数量 | 建议不超过 100 条 |
| 最大重试 | 默认 3 次，可配置 |

---

## 相关链接

- [产品详情页](https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do)
- [README](../README.md)
- [架构文档](architecture.md)
