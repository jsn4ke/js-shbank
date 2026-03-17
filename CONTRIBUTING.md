# 贡献指南

感谢您对 BSH 项目的关注！我们欢迎各种形式的贡献。

---

## 如何贡献

### 报告问题

如果您发现了 Bug 或有功能建议：

1. 在 [Issues](https://github.com/xxx/bsh/issues) 中搜索现有问题
2. 如果没有找到，创建新的 Issue
3. 清晰描述问题或建议

### 提交代码

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feat/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feat/AmazingFeature`)
5. 创建 Pull Request

---

## 开发环境搭建

### 1. 克隆仓库

```bash
git clone https://github.com/xxx/bsh.git
cd bsh
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 验证安装

```bash
python -c "import js_shbank; print(bsh.__version__)"
```

---

## 开发流程

### 分支策略

- `main` - 主分支，始终保持稳定
- `feat/xxx` - 新功能开发
- `fix/xxx` - Bug 修复
- `refactor/xxx` - 重构
- `docs/xxx` - 文档更新

### 提交规范

使用 Conventional Commits 格式：

```
<type>: <subject>

<body>
```

**类型 (type)**：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 代码重构 |
| `docs` | 文档更新 |
| `test` | 测试相关 |
| `chore` | 构建/工具链相关 |

**示例**：

```bash
feat: 添加按币种筛选功能
fix: 修复 URL 生成错误
docs: 更新 API 文档
test: 添加 Repository 测试
```

### Pull Request 要求

- [ ] 代码通过所有测试 (`pytest`)
- [ ] 测试覆盖率 ≥ 80%
- [ ] 代码通过 ruff 检查 (`ruff check .`)
- [ ] 代码通过 mypy 类型检查 (`mypy src/`)
- [ ] 更新相关文档
- [ ] 清晰描述 PR 内容

---

## 代码规范

### Python 风格

遵循 PEP 8 规范，使用 ruff 格式化：

```bash
ruff format .
ruff check .
```

### 类型注解

使用 Python 类型注解：

```python
from typing import List, Optional

def get_products(limit: int = 100) -> List[dict]:
    """获取产品列表"""
    return []
```

### 文档字符串

使用 Google 风格的 docstring：

```python
def fetch_products(self, params: FetchParams) -> APIResponse:
    """获取产品列表（单次请求）

    Args:
        params: 请求参数

    Returns:
        APIResponse: API 响应

    Raises:
        RuntimeError: HTTP 错误
        RequestException: 网络错误
    """
```

---

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_parser.py

# 运行特定测试
pytest tests/test_parser.py::test_parse_product
```

### 查看覆盖率

```bash
# 生成 HTML 覆盖率报告
pytest --cov=src --cov-report=html

# 查看报告
# 打开 htmlcov/index.html
```

### 编写测试

遵循 TDD (测试驱动开发) 流程：

1. **编写测试**（预期失败）
2. **运行测试**（确认失败）
3. **实现代码**（使测试通过）
4. **重构**（优化代码）

#### 测试示例

```python
import pytest
from js_shbank.scraper import Parser
from js_shbank.models import ProductModel

class TestParser:
    def test_parse_product_basic(self):
        """测试基本产品解析"""
        record = {
            "prdCode": "TEST001",
            "prdName": "测试产品",
            "rate": "3.5",
        }
        product = Parser.parse_product(record)

        assert product.prd_code == "TEST001"
        assert product.prd_name == "测试产品"
        assert product.rate == "3.5"

    def test_build_detail_url(self):
        """测试 URL 生成"""
        url = Parser.build_detail_url("TEST001")
        expected = "https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode=TEST001&_locale=zh_CN"
        assert url == expected
```

---

## 项目结构

```
bsh/
├── src/bsh/        # 源代码
│   ├── config/      # 配置
│   ├── models/      # 数据模型
│   ├── repository/  # 数据访问
│   ├── scraper/     # 数据获取
│   ├── calculator/  # 业务计算
│   ├── web/         # Web 界面
│   ├── cli.py       # 命令行
│   └── main.py      # 主入口
├── tests/          # 测试
├── doc/            # 文档
├── data/           # 数据目录
└── README.md       # 项目说明
```

---

## 常见问题

### Q: 如何调试？

```bash
# 启用调试模式
python -m pytest --pdb

# 或使用 print 调试
print(f"Debug: {variable}")
```

### Q: 如何添加新的依赖？

1. 在 `pyproject.toml` 的 `dependencies` 中添加
2. 运行 `pip install -e .` 安装
3. 更新 `requirements.txt`

### Q: 测试失败怎么办？

```bash
# 查看详细错误信息
pytest --tb=long

# 只运行失败的测试
pytest --lf
```

---

## 行为准则

### 我们的承诺

- 尊重所有贡献者
- 及时回应 Issue 和 PR
- 保持代码质量
- 清晰的代码审查反馈

### 期望贡献者

- 礼貌和尊重
- 清晰沟通
- 遵循代码规范
- 编写测试

---

## 许可证

通过贡献代码，您同意您的贡献将根据 MIT 许可证进行许可。

---

## 相关链接

- [项目 README](README.md)
- [API 文档](doc/api.md)
- [架构文档](doc/architecture.md)
