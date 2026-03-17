"""测试数据模型"""
from datetime import datetime

from js_shbank.models.product import APIResponse, ProductModel


class TestProductModel:
    """测试 ProductModel 类"""

    def test_create_minimal_product(self):
        """测试创建最小产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
        )
        assert product.prd_code == "TEST001"
        assert product.prd_name == "测试产品"
        assert product.rate is None

    def test_create_full_product(self):
        """测试创建完整产品"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            rate="3.5",
            rate_script="近七日年化",
            week_year_rate="3.6",
            month_year_rate="3.7",
            three_month_year_rate="3.8",
            half_year_year_rate="3.9",
            unit_rate="1.0123",
            estab_ratio="1.0567",
            risk_level=2,
            curr_type="CNY",
            pfirst_amt=10000,
            sold_out=0,
            prd_labels="新户专享@!@手机专属",
        )
        assert product.prd_code == "TEST001"
        assert product.rate == "3.5"
        assert product.risk_level == 2

    def test_risk_level_string(self):
        """测试风险等级字符串"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            risk_level=3,
        )
        assert product.risk_level == 3

    def test_curr_type_validation(self):
        """测试币种验证"""
        # 有效币种
        ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            curr_type="CNY",
        )
        ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            curr_type="USD",
        )

    def test_model_serialization(self):
        """测试模型序列化"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            rate="3.5",
        )
        data = product.model_dump()
        assert data["prd_code"] == "TEST001"
        assert data["prd_name"] == "测试产品"
        assert data["rate"] == "3.5"

    def test_model_json(self):
        """测试 JSON 序列化"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            rate="3.5",
        )
        json_str = product.model_dump_json()
        assert "TEST001" in json_str

    def test_fetched_at_default(self):
        """测试抓取时间默认值"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
        )
        assert isinstance(product.fetched_at, datetime)

    def test_optional_fields(self):
        """测试可选字段"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
        )
        assert product.rate is None
        assert product.unit_rate is None
        assert product.prd_labels is None

    def test_prd_labels_parser(self):
        """测试产品标签解析"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            prd_labels="新户专享@!@手机专属@!@快赎",
        )
        assert product.prd_labels == "新户专享@!@手机专属@!@快赎"

    def test_empty_prd_labels(self):
        """测试空产品标签"""
        product = ProductModel(
            prd_code="TEST001",
            prd_name="测试产品",
            prd_labels="",
        )
        assert product.prd_labels == ""


class TestAPIResponse:
    """测试 APIResponse 类"""

    def test_create_response_with_products(self):
        """测试创建包含产品的响应"""
        products = [
            ProductModel(prd_code="TEST001", prd_name="产品1"),
            ProductModel(prd_code="TEST002", prd_name="产品2"),
        ]
        response = APIResponse(
            code=200,
            success=True,
            data={
                "records": products,
                "total": 100,
                "size": 10,
                "current": 1,
            },
        )
        assert response.code == 200
        assert response.success is True
        assert len(response.data["records"]) == 2
        assert response.data["total"] == 100
        assert response.data["size"] == 10
        assert response.data["current"] == 1

    def test_create_empty_response(self):
        """测试创建空响应"""
        response = APIResponse(
            code=200,
            success=True,
            data={"records": [], "total": 0, "size": 10, "current": 1},
        )
        assert response.code == 200
        assert len(response.data["records"]) == 0

    def test_failed_response(self):
        """测试失败响应"""
        response = APIResponse(
            code=500,
            success=False,
            data=None,
        )
        assert response.code == 500
        assert response.success is False
        assert response.data is None

    def test_response_serialization(self):
        """测试响应序列化"""
        products = [
            ProductModel(prd_code="TEST001", prd_name="产品1"),
        ]
        response = APIResponse(
            code=200,
            success=True,
            data={
                "records": products,
                "total": 1,
                "size": 10,
                "current": 1,
            },
        )
        data = response.model_dump()
        assert data["code"] == 200
        assert data["success"] is True
        assert len(data["data"]["records"]) == 1
