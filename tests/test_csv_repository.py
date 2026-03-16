"""CSV Repository 测试"""
import csv
import datetime as dt
import os
import tempfile
from unittest.mock import Mock

from src.models.product import ProductModel
from src.repository.factory import RepositoryFactory


def _create_test_product(code: str, name: str = "测试产品") -> dict:
    """创建测试产品数据"""
    return {
        "prd_code": code,
        "prd_name": name,
        "rate": "3.5%",
        "rate_script": "业绩比较基准",
        "week_year_rate": "2.3%",
        "month_year_rate": "2.8%",
        "three_month_year_rate": "3.0%",
        "half_year_year_rate": "3.2%",
        "unit_rate": "1.0350",
        "estab_ratio": "1.1234",
        "risk_level": 2,
        "curr_type": "CNY",
        "pfirst_amt": 1000,
        "sold_out": 0,
        "prd_labels": "标签1@!@标签2",
        "fetched_at": dt.datetime.now().isoformat(),
    }


class TestCsvRepositorySave:
    """测试 save 方法"""

    def test_save_creates_file(self, tmp_path) -> None:
        """测试保存会创建文件"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        product = ProductModel.model_validate(_create_test_product("TEST001"))

        repo.save(product)

        assert os.path.exists(tmp_path / "products.csv")

    def test_save_appends_to_file(self, tmp_path) -> None:
        """测试保存是追加写入"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 先创建一个产品
        repo.save(ProductModel.model_validate(_create_test_product("TEST001")))

        # 再保存第二个产品
        repo.save(ProductModel.model_validate(_create_test_product("TEST002")))

        # 验证文件包含两个产品
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 3  # 包含头部 + 2个产品


class TestCsvRepositorySaveBatch:
    """测试 save_batch 方法"""

    def test_save_batch_multiple_products(self, tmp_path) -> None:
        """测试批量保存多个产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        products = [
            ProductModel.model_validate(_create_test_product(f"TEST{i:03d}", f"产品{i}"))
            for i in range(5)
        ]

        repo.save_batch(products)

        # 验证文件包含 5 个产品
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 6  # 包含头部 + 5个产品

    def test_save_batch_empty_list(self, tmp_path) -> None:
        """测试批量保存空列表"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        repo.save_batch([])

        # 验证文件只包含头部
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 1  # 只包含头部


class TestCsvRepositoryFindAll:
    """测试 find_all 方法"""

    def test_find_all_returns_empty_list(self, tmp_path) -> None:
        """测试空文件时返回空列表"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        products = repo.find_all()

        assert products == []

    def test_find_all_returns_products(self, tmp_path) -> None:
        """测试有数据时返回产品列表"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 先保存一些产品
        products = [
            ProductModel.model_validate(_create_test_product(f"TEST{i:03d}", f"产品{i}"))
            for i in range(3)
        ]
        repo.save_batch(products)

        # 查询所有产品
        found_products = repo.find_all()

        assert len(found_products) == 3
        assert found_products[0].prd_code == "TEST000"
        assert found_products[1].prd_code == "TEST001"
        assert found_products[2].prd_code == "TEST002"


class TestCsvRepositoryFindByCode:
    """测试 find_by_code 方法"""

    def test_find_by_code_returns_none(self, tmp_path) -> None:
        """测试找不到时返回 None"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        product = repo.find_by_code("NOTFOUND")

        assert product is None

    def test_find_by_code_returns_product(self, tmp_path) -> None:
        """测试找到时返回产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 先保存一个产品
        repo.save(ProductModel.model_validate(_create_test_product("TEST001")))

        # 查找产品
        product = repo.find_by_code("TEST001")

        assert product is not None
        assert product.prd_code == "TEST001"


class TestCsvRepositoryUpdate:
    """测试 update 方法"""

    def test_update_existing_product(self, tmp_path) -> None:
        """测试更新现有产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 先保存一个产品
        repo.save(ProductModel.model_validate(_create_test_product("TEST001", "原始产品")))

        # 更新产品
        updated_product = ProductModel.model_validate(
            _create_test_product("TEST001", "更新后产品")
        )
        repo.update(updated_product)

        # 验证已更新
        product = repo.find_by_code("TEST001")
        assert product.prd_name == "更新后产品"

    def test_update_non_existing_product(self, tmp_path) -> None:
        """测试更新不存在的产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 更新不存在的产品
        updated_product = ProductModel.model_validate(_create_test_product("TEST001"))

        repo.update(updated_product)

        # 验证文件新增了记录
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 2  # 头部 + 1个产品


class TestCsvRepositoryDelete:
    """测试 delete 方法"""

    def test_delete_existing_product(self, tmp_path) -> None:
        """测试删除现有产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 先保存一个产品
        repo.save(ProductModel.model_validate(_create_test_product("TEST001")))

        # 删除产品
        repo.delete("TEST001")

        # 验证产品被删除
        product = repo.find_by_code("TEST001")
        assert product is None

    def test_delete_non_existing_product(self, tmp_path) -> None:
        """测试删除不存在的产品"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 删除不存在的产品（应该不报错）
        repo.delete("NOTFOUND")

        # 验证文件没有变化（只有头部）
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 1  # 只包含头部


class TestCsvRepositoryFileHandling:
    """测试文件处理"""

    def test_file_not_exists_creates_file(self, tmp_path) -> None:
        """测试文件不存在时自动创建"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        product = ProductModel.model_validate(_create_test_product("TEST001"))

        repo.save(product)

        assert os.path.exists(tmp_path / "products.csv")

    def test_append_to_existing_file(self, tmp_path) -> None:
        """测试追加到已存在的文件"""
        settings = Mock()
        settings.configure_mock(**{"data_dir": tmp_path})

        repo = RepositoryFactory.create_repository(settings, "csv")

        # 创建文件
        with open(tmp_path / "products.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["prd_code", "prd_name"])

        # 追加数据
        repo.save(ProductModel.model_validate(_create_test_product("TEST001")))

        # 验证文件包含两行
        with open(tmp_path / "products.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 2
