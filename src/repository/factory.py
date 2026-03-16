"""Repository 工厂模块"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config.settings import Settings
    from src.repository.base import BaseRepository


class RepositoryFactory:
    """Repository 工厂类

    根据 配置创建对应的 Repository 实例。
    """

    @staticmethod
    def create_repository(settings: "Settings", repo_type: str) -> "BaseRepository":
        """创建 Repository 实例

        Args:
            settings: 配置对象
            repo_type: Repository 类型，目前支持 "csv"

        Returns:
            BaseRepository: Repository 实例

        Raises:
            ValueError: 如果 repo_type 不支持
        """
        from src.repository.csv_repository import CsvRepository

        # 根据类型创建对应的 Repository
        if repo_type == "csv":
            return CsvRepository(settings)

        raise ValueError(f"不支持的存储类型: {repo_type}")
