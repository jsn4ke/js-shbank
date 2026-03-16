# BSH 项目记忆 (MEMORY.md)

> 本文件记录项目相关的长期记忆和关键信息

---

## 项目信息

- **项目名称**: BSH (上海银行理财数据爬取)
- **项目类型**: Python 项目
- **当前版本**: 0.0.1
- **主要功能**: 爬取上海银行理财页面数据，提取产品信息并计算各种年化收益率

---

## API 信息

- **基础 URL**: `https://www.bosc.cn/apiQry`
- **端点**: `/apiPCQry/qryPcFinanceProductZh`
- **请求方法**: POST
- **请求参数**:
  ```json
  {
    "dailyDeanRedQry": "",
    "buyLastDayQry": "",
    "rapidRedPrdQry": "",
    "prdCodeName": "",
    "soldOut": "",
    "prdTimeLimitQry": "",
    "prdTplType": "",
    "shelvesTypeQry": "",
    "pfirstAmtQry": "",
    "taCodeQry": "",
    "clientLevel": "",
    "riskLevel": "",
    "currType": "",
    "crossProdQry": "2",
    "size": 10,
    "current": 1
  }
  ```

---

## 数据模型字段

### ProductModel

| 字段名 | 类型 | 说明 |
|--------|------|------|
| prd_code | str | 产品代码 |
| prd_name | str | 产品名称 |
| rate | str \| None | 年化收益率 |
| rate_script | str \| None | 收益率备注 |
| week_year_rate | str \| None | 近七日年化 |
| month_year_rate | str \| None | 近一月年化 |
| three_month_year_rate | str \| None | 近三月年化 |
| half_year_year_rate | str \| None | 近半年年化 |
| unit_rate | str \| None | 单位净值 |
| estab_ratio | str \| None | 成立以来净值 |
| risk_level | int \| None | 风险等级 0-5 |
| curr_type | str \| None | 币种 CNY/USD |
| pfirst_amt | int \| None | 起售金额 |
| sold_out | int \| None | 是否售罄 0=否 1=是 |
| prd_labels | str \| None | 产品标签 @!@分隔 |
| fetched_at | datetime | 抓取时间 |

---

## 目录结构

```
bsh/
├── src/
│   ├── config/          # 配置管理
│   ├── models/          # Pydantic 数据模型
│   ├── repository/      # 数据存储抽象层
│   ├── scraper/         # API 客户端和解析
│   ├── calculator/      # 年化计算
│   └── main.py          # 主入口
├── tests/               # 测试
├── data/                # 数据存储
├── doc/                 # 文档和计划
├── memory/              # 项目记忆和进度
└── pyproject.toml       # 项目配置
```

---

## 开发规则关键点

1. **所有 Python 操作必须在 venv 虚拟环境下执行**
2. 新分支必须从 main 拉出
3. TDD：先写测试，再写代码
4. 测试覆盖率 ≥ 80%
5. 开发完成后合并到 main 并推送

---

## 相关文档

- `memory/project-progress.md` - 详细开发进度追踪
- `doc/v0.0.1-plan.md` - v0.0.1 详细开发计划
- `.claude/rules/development.md` - 项目开发规则
