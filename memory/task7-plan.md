# Task 7: Repository 接口设计计划

## 目标
实现 Repository 抽象层，定义数据存储的统一接口。

## 小功能点清单

### 7.1 创建 Repository 基础结构
- 创建 `src/repository/base.py`
- 实现 BaseRepository 抽象基类
- 定义标准操作方法：
  - `save(product: ProductModel)` - 保存单个产品
  - `save_batch(products: list[ProductModel])` - 批量保存
  - `find_by_code(code: str)` - 按代码查找
  - `find_all()` - 查找所有
  - `update(product: ProductModel)` - 更新产品
  - `delete(code: str)` - 删除产品

### 7.2 创建 RepositoryFactory
- 创建 `src/repository/factory.py`
- 实现 RepositoryFactory 类
- 根据 配置创建对应的 Repository 实例
- 目前只支持 CSV，预留扩展其他存储方式

### 7.3 编写测试 (TDD - 先写测试)
- 创建 `tests/test_repository.py`
- 测试 BaseRepository 抽象接口
- 测试 RepositoryFactory 创建逻辑
- 测试 CSV Repository 实现的接口

## 开发顺序
1. 写测试 → 测试失败 (RED)
2. 写代码 → 测试通过 (GREEN)
3. 重构 → 代码优化 (IMPROVE)

## 验收标准
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] 抽象接口定义完整
- [ ] 工厂模式正确实现
- [ ] 代码符合 Repository Pattern
