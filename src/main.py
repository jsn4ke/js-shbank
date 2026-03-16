"""BSH 主入口模块

集成了 API 客户端、数据解析器和存储库，提供完整的爬取和存储流程。
"""
import logging

from src.config.settings import get_settings
from src.repository.factory import RepositoryFactory
from src.scraper.api_client import ApiClient
from src.scraper.parser import Parser

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> int:
    """主函数：爬取上海银行理财数据并存储为 CSV

    Returns:
        int: 状态码，0 表示成功，非 0 表示失败
    """
    try:
        # 加载配置
        settings = get_settings()
        logger.info(f"配置加载完成，数据目录: {settings.data_dir}")

        # 初始化组件
        api_client = ApiClient(settings=settings)
        parser = Parser()
        repository = RepositoryFactory.create_repository(settings, "csv")

        logger.info("开始获取产品数据...")
        # 获取所有产品数据
        api_data_list = api_client.fetch_all_products()
        logger.info(f"获取到 {len(api_data_list)} 个产品的原始数据")

        # 解析数据
        products = []
        for api_data in api_data_list:
            try:
                product = parser.parse_product(api_data)
                products.append(product)
            except Exception as e:
                logger.warning(f"解析产品 {api_data.get('prdCode', 'unknown')} 失败: {e}")

        logger.info(f"成功解析 {len(products)} 个产品")

        # 保存数据（即使空列表也保存，确保文件存在）
        repository.save_batch(products)
        if products:
            logger.info(f"成功保存 {len(products)} 个产品到 CSV")
        else:
            logger.warning("没有可保存的产品数据，仅创建文件结构")

        logger.info("主流程执行完成")
        return 0

    except Exception as e:
        logger.error(f"主流程执行失败: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
