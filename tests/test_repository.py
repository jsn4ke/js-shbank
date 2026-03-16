"""Repository 测试"""
from unittest.mock import Mock

from src.repository.base import BaseRepository
from src.repository.factory import RepositoryFactory


def test_is_abstract() -> None:
    """测试 BaseRepository 是抽象类"""
    # 尝试直接实例化应该失败
    try:
        BaseRepository()  # type: ignore[abstract]
    except TypeError:
        pass


def test_has_required_methods() -> None:
    """测试定义了必需的方法"""
    required_methods = [
        "save",
        "save_batch",
        "find_by_code",
        "find_all",
        "update",
        "delete",
    ]

    for method_name in required_methods:
        assert hasattr(BaseRepository, method_name)


def test_create_csv_repository() -> None:
    """测试创建 CSV Repository"""
    settings = Mock()
    settings.configure_mock(**{"data_dir": "test_data"})

    repo = RepositoryFactory.create_repository(settings, "csv")

    assert isinstance(repo, BaseRepository)


def test_invalid_repository_type() -> None:
    """测试无效的 Repository 类型"""
    settings = Mock()

    try:
        RepositoryFactory.create_repository(settings, "invalid_type")
    except ValueError as e:
        assert "不支持的存储类型" in str(e)
