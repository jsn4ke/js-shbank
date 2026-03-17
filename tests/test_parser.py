"""数据解析器测试"""

from js_shbank.models.product import ProductModel
from js_shbank.scraper.parser import Parser


class TestParserLabels:
    """标签解析测试"""

    def test_parse_labels_empty(self) -> None:
        """测试解析空标签"""
        result = Parser.parse_labels("")
        assert result == []

    def test_parse_labels_none(self) -> None:
        """测试解析 None 标签"""
        result = Parser.parse_labels(None)
        assert result == []

    def test_parse_labels_single(self) -> None:
        """测试解析单个标签"""
        result = Parser.parse_labels("灵活申赎")
        assert result == ["灵活申赎"]

    def test_parse_labels_multiple(self) -> None:
        """测试解析多个标签"""
        result = Parser.parse_labels("灵活申赎@!@低风险@!@人民币")
        assert result == ["灵活申赎", "低风险", "人民币"]

    def test_parse_labels_with_separator_at_start(self) -> None:
        """测试标签以分隔符开头"""
        result = Parser.parse_labels("@!@标签1@!@标签2")
        assert result == ["", "标签1", "标签2"]

    def test_parse_labels_with_separator_at_end(self) -> None:
        """测试标签以分隔符结尾"""
        result = Parser.parse_labels("标签1@!@标签2@!@")
        assert result == ["标签1", "标签2", ""]


class TestParserFieldMapping:
    """字段映射测试"""

    def test_map_risk_level_zero(self) -> None:
        """测试风险等级 0"""
        result = Parser._map_risk_level(0)
        assert result == ""

    def test_map_risk_level_one(self) -> None:
        """测试风险等级 1"""
        result = Parser._map_risk_level(1)
        assert result == "R1极低风险"

    def test_map_risk_level_five(self) -> None:
        """测试风险等级 5"""
        result = Parser._map_risk_level(5)
        assert result == "R5高风险"

    def test_map_risk_level_none(self) -> None:
        """测试风险等级 None"""
        result = Parser._map_risk_level(None)
        assert result is None

    def test_map_risk_level_invalid(self) -> None:
        """测试无效风险等级"""
        result = Parser._map_risk_level(10)
        assert result == "未知风险"

    def test_map_curr_type_cny(self) -> None:
        """测试币种 CNY"""
        result = Parser._map_curr_type("CNY")
        assert result == "人民币"

    def test_map_curr_type_usd(self) -> None:
        """测试币种 USD"""
        result = Parser._map_curr_type("USD")
        assert result == "美元"

    def test_map_curr_type_none(self) -> None:
        """测试币种 None"""
        result = Parser._map_curr_type(None)
        assert result is None

    def test_map_curr_type_unknown(self) -> None:
        """测试未知币种"""
        result = Parser._map_curr_type("EUR")
        assert result == "EUR"

    def test_map_sold_out_zero(self) -> None:
        """测试未售罄"""
        result = Parser._map_sold_out(0)
        assert result == "否"

    def test_map_sold_out_one(self) -> None:
        """测试已售罄"""
        result = Parser._map_sold_out(1)
        assert result == "是"

    def test_map_sold_out_none(self) -> None:
        """测试 None"""
        result = Parser._map_sold_out(None)
        assert result is None

    def test_format_amount_none(self) -> None:
        """测试格式化金额 None"""
        result = Parser._format_amount(None)
        assert result is None

    def test_format_amount_value(self) -> None:
        """测试格式化金额"""
        result = Parser._format_amount(1000)
        assert result == "1000元"


class TestParserProduct:
    """产品解析测试"""

    def test_parse_product_minimal(self) -> None:
        """测试解析最简产品"""
        record = {
            "prdCode": "TEST001",
            "prdName": "测试产品",
        }
        product = Parser.parse_product(record)

        assert isinstance(product, ProductModel)
        assert product.prd_code == "TEST001"
        assert product.prd_name == "测试产品"

    def test_parse_product_full(self) -> None:
        """测试解析完整产品"""
        record = {
            "prdCode": "TEST001",
            "prdName": "测试产品",
            "rate": "3.5%",
            "rateScript": "业绩比较基准",
            "weekYearRate": "2.3%",
            "monthYearRate": "2.8%",
            "threeMonthYearRate": "3.0%",
            "halfYearYearRate": "3.2%",
            "unitRate": "1.0350",
            "estabRatio": "1.1234",
            "riskLevel": 2,
            "currType": "CNY",
            "pfirstAmt": 1000,
            "soldOut": 0,
            "prdLabels": "灵活申赎@!@低风险",
        }
        product = Parser.parse_product(record)

        assert product.prd_code == "TEST001"
        assert product.prd_name == "测试产品"
        assert product.rate == "3.5%"
        assert product.rate_script == "业绩比较基准"
        assert product.week_year_rate == "2.3%"
        assert product.risk_level == 2
        assert product.curr_type == "CNY"
        assert product.pfirst_amt == 1000
        assert product.sold_out == 0
        assert product.prd_labels == "灵活申赎@!@低风险"

    def test_parse_product_with_none_values(self) -> None:
        """测试解析带 None 值的产品"""
        record = {
            "prdCode": "TEST001",
            "prdName": "测试产品",
            "rate": None,
            "riskLevel": None,
            "currType": None,
        }
        product = Parser.parse_product(record)

        assert product.prd_code == "TEST001"
        assert product.rate is None
        assert product.risk_level is None
        assert product.curr_type is None

    def test_parse_product_camel_case_to_snake_case(self) -> None:
        """测试驼峰转下划线"""
        record = {
            "prdCode": "TEST001",
            "prdName": "测试产品",
            "weekYearRate": "2.3%",
        }
        product = Parser.parse_product(record)

        assert product.week_year_rate == "2.3%"


class TestParserApiResponse:
    """API 响应解析测试"""

    def test_parse_api_response_with_data(self) -> None:
        """测试解析有数据的响应"""
        response_data = {
            "records": [
                {
                    "prdCode": "TEST001",
                    "prdName": "测试产品1",
                },
                {
                    "prdCode": "TEST002",
                    "prdName": "测试产品2",
                },
            ],
            "total": 2,
        }
        products = Parser.parse_api_response(response_data)

        assert len(products) == 2
        assert products[0].prd_code == "TEST001"
        assert products[1].prd_code == "TEST002"

    def test_parse_api_response_empty(self) -> None:
        """测试解析空响应"""
        response_data = {"records": [], "total": 0}
        products = Parser.parse_api_response(response_data)

        assert products == []

    def test_parse_api_response_none(self) -> None:
        """测试解析 None 响应"""
        products = Parser.parse_api_response(None)

        assert products == []
