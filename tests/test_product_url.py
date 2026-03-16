"""测试产品 URL 功能"""
import pytest
from bsh.models.product import ProductModel


class TestProductURLFields:
    """测试产品 URL 相关字段"""

    def test_product_with_prd_id(self):
        """测试创建包含 prd_id 的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            prd_id="123456"
        )
        assert product.prd_id == "123456"

    def test_product_with_prd_category(self):
        """测试创建包含 prd_category 的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            prd_category="01"
        )
        assert product.prd_category == "01"

    def test_product_with_detail_page_url(self):
        """测试创建包含 detail_page_url 的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            detail_page_url="https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/?prdId=123"
        )
        assert product.detail_page_url == "https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/?prdId=123"

    def test_product_without_url_fields(self):
        """测试不包含 URL 字段的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品"
        )
        assert product.prd_id is None
        assert product.prd_category is None
        assert product.detail_page_url is None


class TestURLGeneration:
    """测试 URL 生成"""

    def test_build_detail_url_with_prd_id_only(self):
        """测试只用 prd_id 生成 URL"""
        from bsh.scraper import Parser

        url = Parser.build_detail_url("123456", None)
        expected = "https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/?prdId=123456"
        assert url == expected

    def test_build_detail_url_with_prd_id_and_category(self):
        """测试用 prd_id 和 category 生成 URL"""
        from bsh.scraper import Parser

        url = Parser.build_detail_url("123456", "01")
        expected = "https://www.bosc.cn/zh/gryw/tzlc/lc/zxcpxx/?prdId=123456&prdCategory=01"
        assert url == expected

    def test_build_detail_url_with_none_prd_id(self):
        """测试 prd_id 为 None 时返回 None"""
        from bsh.scraper import Parser

        url = Parser.build_detail_url(None, "01")
        assert url is None
