# 上海银行产品详情 URL 研究

## 研究目标

确定上海银行理财产品详情页的 URL 生成规则。

## 研究方法

1. 访问上海银行理财页面
2. 分析产品列表中的产品代码如何映射到详情页 URL
3. 确定必需的 URL 参数

## 产品页面 URL

产品列表页面：https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/

## 实际 URL 模式

根据实际访问验证，正确的产品详情页 URL 格式如下：

```
https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode={产品代码}&_locale=zh_CN
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| PortalFlag | 门户标识 | finance |
| PrdCode | 产品代码 | WPXK25M0202A |
| _locale | 语言设置 | zh_CN |

### 完整示例

```
https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode=WPXK25M0202A&_locale=zh_CN
```

## URL 生成规则

- **基础 URL**: `https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do`
- **必需参数**:
  - `PortalFlag=finance`
  - `PrdCode={prdCode}`
  - `_locale=zh_CN`

## 代码实现

```python
@staticmethod
def build_detail_url(prd_code: str | None) -> str | None:
    """构建产品详情页 URL"""
    if not prd_code:
        return None

    base_url = "https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do"
    params = f"?PortalFlag=finance&PrdCode={prd_code}&_locale=zh_CN"
    return base_url + params
```

## 研究结论

✅ URL 模式已确认并验证。
✅ 使用 `prdCode` 字段作为 URL 参数。
✅ 产品详情页可正常访问。
