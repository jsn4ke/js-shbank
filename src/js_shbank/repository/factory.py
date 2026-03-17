"""Repository 工厂模块"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from js_shbank.config.settings import Settings
    from js_shbank.repository.base import BaseRepository


class RepositoryFactory:
    """Repository 工厂类

    根据 配置创建对应的 Repository 实例。
    """

    @staticmethod
    def create_repository(settings: "Settings", repo_type: str, filepath: str | None = None) -> "BaseRepository":
        """创建 Repository 实例

        Args:
            settings: 配置对象
            repo_type: Repository 类型，目前支持 "csv"
            filepath: 可选的文件路径，用于覆盖配置中的默认路径

        Returns:
            BaseRepository: Repository 实例

        Raises:
            ValueError: 如果 repo_type 不支持
        """
        from js_shbank.repository.csv_repository import CsvRepository

        # 根据类型创建对应的 Repository
        if repo_type == "csv":
            if filepath:
                # 如果指定了 filepath，需要临时修改 settings
                class CustomSettings:
                    data_dir = filepath
                return CsvRepository(CustomSettings())
            return CsvRepository(settings)

        raise ValueError(f"不支持的存储类型: {repo_type}")
