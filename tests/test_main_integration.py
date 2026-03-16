"""主流程集成测试"""
from unittest.mock import Mock, patch

from src.config.settings import Settings


class TestMainIntegration:
    """测试主流程集成"""

    @patch("src.scraper.api_client.ApiClient")
    @patch("src.repository.factory.RepositoryFactory")
    def test_main_flow_fetches_and_saves_products(
        self, mock_repo_factory, mock_api_client_class
    ):
        """测试主流程：获取数据并保存"""
        # Mock API Client
        mock_api_client = Mock()
        mock_api_client.fetch_all_products.return_value = [
            {
                "prdCode": "TEST001",
                "prdName": "测试产品",
                "nav": "1.0350",
                "navDate": "2026-03-16",
                "estabRatio": "1.1234",
            }
        ]
        mock_api_client_class.return_value = mock_api_client

        # Mock Repository
        mock_repo = Mock()
        mock_repo_factory.create_repository.return_value = mock_repo

        # Import main after mocking
        from src.main import main

        # Run main
        result = main()

        # Verify API was called
        mock_api_client.fetch_all_products.assert_called_once()

        # Verify save was called
        mock_repo.save_batch.assert_called_once()

    @patch("src.scraper.api_client.ApiClient")
    @patch("src.repository.factory.RepositoryFactory")
    def test_main_flow_handles_api_error(
        self, mock_repo_factory, mock_api_client_class
    ):
        """测试主流程：处理 API 错误"""
        # Mock API Client to raise error
        mock_api_client = Mock()
        mock_api_client.fetch_all_products.side_effect = Exception("API Error")
        mock_api_client_class.return_value = mock_api_client

        # Mock Repository
        mock_repo = Mock()
        mock_repo_factory.create_repository.return_value = mock_repo

        # Import main after mocking
        from src.main import main

        # Run main - should not crash
        result = main()

        # Verify save was NOT called
        mock_repo.save_batch.assert_not_called()

    @patch("src.scraper.api_client.ApiClient")
    @patch("src.repository.factory.RepositoryFactory")
    def test_main_flow_handles_empty_data(
        self, mock_repo_factory, mock_api_client_class
    ):
        """测试主流程：处理空数据"""
        # Mock API Client to return empty list
        mock_api_client = Mock()
        mock_api_client.fetch_all_products.return_value = []
        mock_api_client_class.return_value = mock_api_client

        # Mock Repository
        mock_repo = Mock()
        mock_repo_factory.create_repository.return_value = mock_repo

        # Force reload main module to get fresh mocks
        import importlib
        import sys
        if "src.main" in sys.modules:
            importlib.reload(sys.modules["src.main"])
        from src.main import main

        # Run main
        result = main()

        # Verify save was called with empty list
        mock_repo.save_batch.assert_called_once_with([])


class TestMainCLI:
    """测试命令行接口"""

    def test_main_returns_success_code(self):
        """测试主流程返回成功状态码"""
        with patch("src.scraper.api_client.ApiClient"), patch(
            "src.repository.factory.RepositoryFactory"
        ):
            from src.main import main

            result = main()
            assert result == 0
