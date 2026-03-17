"""BSH - 上海银行理财数据爬取库"""

__version__ = "0.0.2"

from js_shbank.models import ProductModel
from js_shbank.config import Settings
from js_shbank.scraper import ApiClient, Parser
from js_shbank.repository import BaseRepository, CsvRepository, RepositoryFactory
from js_shbank.calculator import YieldCalculator

__all__ = [
    "__version__",
    "ProductModel",
    "Settings",
    "ApiClient",
    "Parser",
    "BaseRepository",
    "CsvRepository",
    "RepositoryFactory",
    "YieldCalculator",
]
