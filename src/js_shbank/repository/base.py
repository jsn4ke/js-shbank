"""Repository 基础接口"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from js_shbank.models.product import ProductModel


class BaseRepository(ABC):
    """Repository 抽象基类

    定义数据存储的标准操作接口，所有具体的 Repository 实现都必须遵循此接口。
    """

    @abstractmethod
    def save(self, product: "ProductModel") -> None:  # type: ignore[no-untyped-def]
        """保存单个产品

        Args:
            product: 产品模型对象
        """
        pass

    @abstractmethod
    def save_batch(self, products: list["ProductModel"]) -> None:  # type: ignore[no-untyped-def]
        """批量保存产品

        Args:
            products: 产品模型对象列表
        """
        pass

    @abstractmethod
    def find_by_code(self, code: str):  # type: ignore[no-untyped-def]
        """按产品代码查找

        Args:
            code: 产品代码

        Returns:
            ProductModel | None: 产品对象，如果不存在则返回 None
        """
        pass


    @abstractmethod
    def find_all(self) -> list["ProductModel"]:  # type: ignore[no-untyped-def]
        """查找所有产品

        Returns:
            list[ProductModel]: 所有产品列表
        """
        pass

    @abstractmethod
    def update(self, product: "ProductModel") -> None:  # type: ignore[no-untyped-def]
        """更新产品

        Args:
            product: 产品模型对象
        """
        pass

    @abstractmethod
    def delete(self, code: str) -> None:  # type: ignore[no-untyped-def]
        """删除产品

        Args:
            code: 产品代码
        """
        pass
