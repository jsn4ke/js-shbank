"""命令行入口模块"""
import argparse
import subprocess
import sys

from bsh.scraper import ApiClient, Parser
from bsh.repository import RepositoryFactory
from bsh.config import Settings


def fetch_command() -> None:
    """获取产品数据并保存到 CSV

    使用方法:
        bsh-fetch --output data/products.csv --page-size 100
    """
    parser = argparse.ArgumentParser(description="获取上海银行理财产品数据")
    parser.add_argument("--output", "-o", help="输出文件路径", default="data/products.csv")
    parser.add_argument("--page-size", help="每页数量", type=int, default=100)

    try:
        args = parser.parse_args()
    except SystemExit:
        # 用户输入了 --help
        return

    settings = Settings()
    settings.page_size = args.page_size

    print(f"正在获取产品数据 (每页 {args.page_size} 条)...")

    client = ApiClient(settings)
    parser_obj = Parser()
    repository = RepositoryFactory.create_repository(settings, "csv", filepath=args.output)

    total_fetched = 0

    try:
        for page_data in client.fetch_all_products():
            products = parser_obj.parse_products(page_data)
            if products:
                repository.save_batch(products)
                total_fetched += len(products)
                print(f"已获取 {total_fetched} 条产品数据...")

        print(f"\n完成！共获取 {total_fetched} 条产品数据")
        print(f"数据已保存到: {args.output}")

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def web_command() -> None:
    """启动 Web 查看界面

    使用方法:
        bsh-web
    """
    print("启动 BSH Web 查看界面...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "bsh.web.app"])


if __name__ == "__main__":
    fetch_command()
