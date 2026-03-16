# Task 4: API 客户端实现计划

## 目标
实现 ApiClient 类，负责与上海银行 API 交互，获取理财产品数据。

## 小功能点清单

### 4.1 创建 API 客户端基础结构
- 创建 `src/scraper/api_client.py`
- 实现 ApiClient 类构造函数，接收 Settings 配置
- 添加请求参数数据类

### 4.2 实现单次请求方法
- 实现 `fetch_products(params: FetchParams) -> APIResponse` 方法
- 构建 HTTP POST 请求
- 解析 JSON 响应
- 错误处理（HTTP 状态码检查）

### 4.3 实现分页获取方法
- 实现 `fetch_all_products() -> list[ProductModel]` 方法
- 循环获取数据直到没有更多页面
- 处理空结果情况

### 4.4 错误处理和重试
- 实现网络错误重试机制
- 使用配置中的 max_retries 参数
- 添加超时处理

### 4.5 编写测试 (TDD - 先写测试)
- 创建 `tests/test_api_client.py`
- 测试单次请求成功场景
- 测试分页获取场景
- 测试错误重试场景
- 测试超时场景

## 开发顺序
1. 写测试 → 测试失败 (RED)
2. 写代码 → 测试通过 (GREEN)
3. 重构 → 代码优化 (IMPROVE)

## 验收标准
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] 能成功调用 API
- [ ] 分页逻辑正确
- [ ] 错误处理完善
