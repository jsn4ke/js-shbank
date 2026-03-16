"""CSV Repository 实现"""
import os

from src.repository.base import BaseRepository


class CsvRepository(BaseRepository):  # type: ignore[abstract]
    """CSV 文件存储实现

    注意：此文件是占位符，Task 8 将完善此实现。
    """

    def __init__(self, settings) -> None:
        """初始化 CSV Repository

        Args:
            settings: 配置对象
        """
        self.settings = settings
        self.file_path = os.path.join(str(self.settings.data_dir), "products.csv")

    def save(self, product) -> None:
        """保存单个产品（占位符）"""
        pass

    def save_batch(self, products) -> None:
        """批量保存产品（占位符）"""
        pass

    def find_by_code(self, code):
        """按产品代码查找（占位符）"""
        return None

    def find_all(self):
        """查找所有产品（占位符）"""
        return []

    def update(self, product) -> None:
        """更新产品（占位符）"""
        pass

    def delete(self, code) -> None:
        """删除产品（占位符）"""
        pass
