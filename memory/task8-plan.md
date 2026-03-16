# Task 8: CSV Repository 实现计划

## 目标
完善 CsvRepository 类，实现 CSV 文件存储的完整功能。

## 小功能点清单

### 8.1 实现 CSV 文件读写
- 创建 CSV 文件（如果不存在）
- 写入 CSV 文件头部
- 读取 CSV 文件内容

### 8.2 实现 save 方法
- 将 ProductModel 转换为字典
- 添加到 CSV 记录列表
- 追加写入到文件

### 8.3 实现 save_batch 方法
- 批量转换 ProductModel 为字典
- 追加写入多个记录

### 8.4 实现 find_all 方法
- 读取 CSV 文件
- 将每行解析为字典
- 转换为 ProductModel 列表

### 8.5 实现 find_by_code 方法
- 读取 CSV 文件
- 查找匹配 prdCode 的记录
- 转换为 ProductModel

### 8.6 实现 update 方法
- 读取所有记录
- 找到匹配的记录
- 更新记录
- 重写整个文件

### 8.7 实现 delete 方法
- 读取所有记录
- 过滤掉要删除的记录
- 重写文件

### 8.8 实现辅助方法
- `_load()` - 读取 CSV 文件
- `_save()` - 写入 CSV 文件
- `_ensure_file_exists()` - 确保文件存在

### 8.9 编写测试 (TDD - 先写测试)
- 创建 `tests/test_csv_repository.py`
- 测试 save 方法
- 测试 save_batch 方法
- 测试 find_all 方法
- 测试 find_by_code 方法
- 测试 update 方法
- 测试 delete 方法
- 测试文件不存在时的行为

## 开发顺序
1. 写测试 → 测试失败 (RED)
2. 写代码 → 测试通过 (GREEN)
3. 重构 → 代码优化 (IMPROVE)

## 验收标准
- [ ] 所有测试通过
- [ ] 测试覆盖率 ≥ 80%
- [ ] CSV 文件格式正确
- [ ] 文件不存在时自动创建
- [ ] 数据正确序列化和反序列化
