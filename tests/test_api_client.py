"""API 客户端测试"""

from typing import Any
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

from js_shbank.config.settings import Settings
from js_shbank.scraper.api_client import ApiClient, FetchParams


class TestFetchParams:
    """FetchParams 数据类测试"""

    def test_default_values(self) -> None:
        """测试默认值"""
        params = FetchParams()
        assert params.cross_prod_qry == "2"
        assert params.size == 10
        assert params.current == 1

    def test_custom_values(self) -> None:
        """测试自定义值"""
        params = FetchParams(
            prd_code_name="测试产品",
            size=20,
            current=2,
        )
        assert params.prd_code_name == "测试产品"
        assert params.size == 20
        assert params.current == 2


class TestApiClient:
    """ApiClient 类测试"""

    def test_init(self) -> None:
        """测试初始化"""
        settings = Settings()
        client = ApiClient(settings)
        assert client.settings is settings
        assert client.session is not None

    @patch("requests.Session.post")
    def test_fetch_products_success(self, mock_post: Mock) -> None:
        """测试成功获取产品列表"""
        # 模拟 API 响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "success": True,
            "data": {"records": [], "total": 0, "size": 10, "current": 1},
        }
        mock_post.return_value = mock_response

        settings = Settings()
        client = ApiClient(settings)
        params = FetchParams()

        response = client.fetch_products(params)

        assert response.code == 200
        assert response.success is True
        assert response.data is not None

        # 验证请求参数
        mock_post.assert_called_once_with(
            "https://www.bosc.cn/apiQry/apiPCQry/qryPcFinanceProductZh",
            json=params.to_dict(),
            timeout=30,
        )

    @patch("requests.Session.post")
    def test_fetch_products_http_error(self, mock_post: Mock) -> None:
        """测试 HTTP 错误"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_post.return_value = mock_response

        settings = Settings()
        client = ApiClient(settings)
        params = FetchParams()

        with pytest.raises(RuntimeError, match="HTTP 错误: 404"):
            client.fetch_products(params)

    @patch("requests.Session.post")
    def test_fetch_products_network_error(self, mock_post: Mock) -> None:
        """测试网络错误重试"""
        mock_post.side_effect = RequestException("网络错误")

        settings = Settings(max_retries=2)
        client = ApiClient(settings)
        params = FetchParams()

        with pytest.raises(RequestException, match="网络错误"):
            client.fetch_products(params)

        # 验证重试次数
        assert mock_post.call_count == 3  # 初始 + 2 次重试

    @patch("requests.Session.post")
    def test_fetch_products_timeout(self, mock_post: Mock) -> None:
        """测试超时"""
        mock_post.side_effect = RequestException("Timeout")

        settings = Settings()
        client = ApiClient(settings)
        params = FetchParams()

        with pytest.raises(RequestException, match="Timeout"):
            client.fetch_products(params)

    @patch("requests.Session.post")
    def test_fetch_all_products_empty(self, mock_post: Mock) -> None:
        """测试获取所有产品（空结果）"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "success": True,
            "data": {"records": [], "total": 0, "size": 10, "current": 1},
        }
        mock_post.return_value = mock_response

        settings = Settings()
        client = ApiClient(settings)

        products = client.fetch_all_products()

        assert products == []

    @patch("requests.Session.post")
    def test_fetch_all_products_single_page(self, mock_post: Mock) -> None:
        """测试获取所有产品（单页）"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 200,
            "success": True,
            "data": {
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
                "size": 10,
                "current": 1,
            },
        }
        mock_post.return_value = mock_response

        settings = Settings()
        client = ApiClient(settings)

        products = client.fetch_all_products()

        assert len(products) == 2
        assert products[0]["prdCode"] == "TEST001"
        assert products[1]["prdCode"] == "TEST002"

    @patch("requests.Session.post")
    def test_fetch_all_products_multi_page(self, mock_post: Mock) -> None:
        """测试获取所有产品（多页）"""
        call_count = 0

        def mock_post_response(*args: Any, **kwargs: Any) -> Mock:
            nonlocal call_count
            call_count += 1

            # 第一页响应：返回 10 个产品
            if call_count == 1:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "code": 200,
                    "success": True,
                    "data": {
                        "records": [
                            {"prdCode": "TEST001", "prdName": "测试产品1"},
                            {"prdCode": "TEST002", "prdName": "测试产品2"},
                            {"prdCode": "TEST003", "prdName": "测试产品3"},
                            {"prdCode": "TEST004", "prdName": "测试产品4"},
                            {"prdCode": "TEST005", "prdName": "测试产品5"},
                            {"prdCode": "TEST006", "prdName": "测试产品6"},
                            {"prdCode": "TEST007", "prdName": "测试产品7"},
                            {"prdCode": "TEST008", "prdName": "测试产品8"},
                            {"prdCode": "TEST009", "prdName": "测试产品9"},
                            {"prdCode": "TEST010", "prdName": "测试产品10"},
                        ],
                        "total": 11,
                        "size": 10,
                        "current": 1,
                    },
                }
                return mock_response
            # 第二页响应：返回 1 个产品
            elif call_count == 2:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "code": 200,
                    "success": True,
                    "data": {
                        "records": [
                            {"prdCode": "TEST011", "prdName": "测试产品11"},
                        ],
                        "total": 11,
                        "size": 10,
                        "current": 2,
                    },
                }
                return mock_response

            # 默认空响应（如果有多余调用）
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "code": 200,
                "success": True,
                "data": {"records": [], "total": 0, "size": 10, "current": 1},
            }
            return mock_response

        mock_post.side_effect = mock_post_response

        settings = Settings()
        client = ApiClient(settings)

        products = client.fetch_all_products()

        assert len(products) == 11
        assert products[0]["prdCode"] == "TEST001"
        assert products[10]["prdCode"] == "TEST011"

        # 验证请求了两次
        assert mock_post.call_count == 2
