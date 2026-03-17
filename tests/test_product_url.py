"""测试产品 URL 功能"""
import pytest
from js_shbank.models.product import ProductModel


class TestProductURLFields:
    """测试产品 URL 相关字段"""

    def test_product_with_detail_page_url(self):
        """测试创建包含 detail_page_url 的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            detail_page_url="https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode=TEST001&_locale=zh_CN"
        )
        assert product.detail_page_url == "https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode=TEST001&_locale=zh_CN"

    def test_product_without_url_fields(self):
        """测试不包含 URL 字段的产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品"
        )
        assert product.detail_page_url is None


class TestURLGeneration:
    """测试 URL 生成"""

    def test_build_detail_url_with_prd_code(self):
        """测试用 prd_code 生成 URL"""
        from js_shbank.scraper import Parser

        url = Parser.build_detail_url("WPXK25M0202A")
        expected = "https://ebanks.bankofshanghai.com/pweb/OpenDetailRule.do?PortalFlag=finance&PrdCode=WPXK25M0202A&_locale=zh_CN"
        assert url == expected

    def test_build_detail_url_with_none_prd_code(self):
        """测试 prd_code 为 None 时返回 None"""
        from js_shbank.scraper import Parser

        url = Parser.build_detail_url(None)
        assert url is None
