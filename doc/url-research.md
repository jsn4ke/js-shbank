# 上海银行产品详情 URL 研究

## 研究目标

确定上海银行理财产品详情页的 URL 生成规则。

## 研究方法

1. 访问上海银行理财页面
2. 分析产品列表中的产品代码如何映射到详情页 URL
3. 确定必需的 URL 参数

## 产品页面 URL

产品列表页面：https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/

## 预期 URL 模式

基于常规银行产品页面的 URL 结构，预期模式如下：

### 模式 A：查询参数方式
```
https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/?prdId={prd_id}
```

### 模式 B：路径方式
```
https://www.bosc.cn/zh/products/{prd_id}
```

## 待确定参数

- [x] prdId: 产品 ID
- [ ] prdCategory: 产品类别
- [ ] 其他可能需要的参数

## 研究结论

需要访问实际页面验证 URL 模式。

**注意**: 由于无法直接访问上海银行官网，本研究基于常见模式推断。
实际使用时需要验证 URL 有效性。
