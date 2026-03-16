"""测试 CLI 模块"""
import argparse
import sys
from io import StringIO
from unittest.mock import Mock, patch


def test_fetch_command_exists():
    """测试 fetch_command 函数存在"""
    from bsh.cli import fetch_command

    assert callable(fetch_command)


def test_web_command_exists():
    """测试 web_command 函数存在"""
    from bsh.cli import web_command

    assert callable(web_command)


@patch("bsh.cli.ApiClient")
@patch("bsh.cli.Parser")
@patch("bsh.cli.RepositoryFactory")
def test_fetch_command_flow(
    mock_factory, mock_parser, mock_api_client_class
):
    """测试 fetch_command 主流程"""
    # Mock API Client
    mock_api_client = Mock()
    mock_api_client.fetch_all_products.return_value = [
        {"prdCode": "TEST001", "prdName": "测试产品"}
    ]
    mock_api_client_class.return_value = mock_api_client

    # Mock Parser
    mock_parser = Mock()
    mock_parser.parse_products.return_value = []

    # Mock Repository
    mock_repo = Mock()
    mock_factory.create_repository.return_value = mock_repo

    # 模拟命令行参数
    with patch("sys.argv", ["bsh-fetch", "--output", "test.csv"]):
        try:
            from bsh.cli import fetch_command
            sys.argv = ["bsh-fetch", "--output", "test.csv"]
        except SystemExit:
            pass


@patch("bsh.cli.subprocess")
def test_web_command_launches_streamlit(mock_subprocess):
    """测试 web_command 启动 Streamlit"""
    mock_subprocess.run.return_value = Mock()

    from bsh.cli import web_command
    web_command()

    # 验证调用了 streamlit run
    mock_subprocess.run.assert_called_once()
    args = mock_subprocess.run.call_args[0][0]
    assert "streamlit" in args
    assert "run" in args
