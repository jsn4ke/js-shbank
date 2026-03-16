"""CSV Repository 实现"""
import csv
import os

from bsh.models.product import ProductModel
from bsh.repository.base import BaseRepository


class CsvRepository(BaseRepository):  # type: ignore[abstract]
    """CSV 文件存储实现"""

    CSV_HEADER = [
        "prd_code",
        "prd_name",
        "rate",
        "rate_script",
        "week_year_rate",
        "month_year_rate",
        "three_month_year_rate",
        "half_year_year_rate",
        "unit_rate",
        "estab_ratio",
        "risk_level",
        "curr_type",
        "pfirst_amt",
        "sold_out",
        "prd_labels",
        "fetched_at",
    ]

    def __init__(self, settings) -> None:
        """初始化 CSV Repository

        Args:
            settings: 配置对象（data_dir 可以是完整文件路径）
        """
        self.settings = settings
        data_dir = str(settings.data_dir)

        # 如果 data_dir 是完整文件路径（包含 .csv），直接使用
        # 否则拼接目录和文件名
        if data_dir.endswith(".csv"):
            self.file_path = data_dir
        else:
            # 确保目录存在
            os.makedirs(data_dir, exist_ok=True)
            self.file_path = os.path.join(data_dir, "products.csv")

    def _load(self) -> dict[str, list[str]]:
        """加载 CSV 文件内容

        Returns:
            dict[str, list[str]]: CSV 行数据，按产品代码分组
        """
        if not os.path.exists(self.file_path):
            return {}

        data: dict[str, list[str]] = {}
        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get("prd_code", "")
                if code:
                    data[code] = []
                data[code].append(row)
        return data

    def _save(self, data: dict[str, list[str]]) -> None:
        """写入 CSV 文件"""
        with open(self.file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADER)
            writer.writeheader()
            for code, rows in data.items():
                for row in rows:
                    row["prd_code"] = code
                    writer.writerow(row)

    def save(self, product) -> None:
        """保存单个产品

        Args:
            product: 产品模型对象
        """
        data = self._load()
        code = product.prd_code

        if code not in data:
            data[code] = []
        data[code].append(product.model_dump())

        self._save(data)

    def save_batch(self, products) -> None:
        """批量保存产品

        Args:
            products: 产品模型对象列表
        """
        data = self._load()
        for product in products:
            code = product.prd_code
            if code not in data:
                data[code] = []
            data[code].append(product.model_dump())

        self._save(data)

    def find_all(self):
        """查找所有产品

        Returns:
            list[ProductModel]: 所有产品列表
        """
        products = []

        data = self._load()
        for code, rows in data.items():
            for row in rows:
                # 转换为 ProductModel
                product = ProductModel(**row)
                products.append(product)

        return products

    def find_by_code(self, code: str):
        """按产品代码查找

        Args:
            code: 产品代码

        Returns:
            ProductModel | None: 产品对象，如果不存在则返回 None
        """
        data = self._load()
        rows = data.get(code, [])
        if not rows:
            return None

        # 返回第一个匹配的产品
        product = ProductModel(**rows[0])
        return product

    def update(self, product) -> None:
        """更新产品

        Args:
            product: 产品模型对象
        """
        data = self._load()
        code = product.prd_code

        rows = data.get(code, [])
        if not rows:
            # 不存在，追加新记录
            data[code] = [product.model_dump()]
        else:
            # 存在，更新记录
            rows[0] = product.model_dump()
            data[code] = rows

        self._save(data)

    def delete(self, code: str) -> None:
        """删除产品

        Args:
            code: 产品代码
        """
        data = self._load()

        if code in data:
            # 产品存在，删除
            rows = data[code]
            del data[code]

        # 重写文件（即使产品不存在也写入，确保文件存在）
        self._save(data)
