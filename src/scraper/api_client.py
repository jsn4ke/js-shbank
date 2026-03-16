"""API 客户端模块"""

import time

import requests
from pydantic import BaseModel

from src.config.settings import Settings
from src.models.product import APIResponse


class FetchParams(BaseModel):
    """API 请求参数"""

    # 查询条件
    daily_dean_red_qry: str = ""
    buy_last_day_qry: str = ""
    rapid_red_prd_qry: str = ""
    prd_code_name: str = ""
    sold_out: str = ""
    prd_time_limit_qry: str = ""
    prd_tpl_type: str = ""
    shelves_type_qry: str = ""
    pfirst_amt_qry: str = ""
    ta_code_qry: str = ""
    client_level: str = ""
    risk_level: str = ""
    curr_type: str = ""
    cross_prod_qry: str = "2"

    # 分页参数
    size: int = 10
    current: int = 1

    def to_dict(self) -> dict:
        """转换为字典（使用 API 需要的命名格式）"""
        return {
            "dailyDeanRedQry": self.daily_dean_red_qry,
            "buyLastDayQry": self.buy_last_day_qry,
            "rapidRedPrdQry": self.rapid_red_prd_qry,
            "prdCodeName": self.prd_code_name,
            "soldOut": self.sold_out,
            "prdTimeLimitQry": self.prd_time_limit_qry,
            "prdTplType": self.prd_tpl_type,
            "shelvesTypeQry": self.shelves_type_qry,
            "pfirstAmtQry": self.pfirst_amt_qry,
            "taCodeQry": self.ta_code_qry,
            "clientLevel": self.client_level,
            "riskLevel": self.risk_level,
            "currType": self.curr_type,
            "crossProdQry": self.cross_prod_qry,
            "size": self.size,
            "current": self.current,
        }


class ApiClient:
    """上海银行 API 客户端"""

    def __init__(self, settings: Settings) -> None:
        """初始化客户端

        Args:
            settings: 配置对象
        """
        self.settings = settings
        self.session = requests.Session()

    def fetch_products(self, params: FetchParams) -> APIResponse:
        """获取产品列表（单次请求）

        Args:
            params: 请求参数

        Returns:
            APIResponse: API 响应

        Raises:
            RuntimeError: HTTP 错误
            RequestException: 网络错误
        """
        last_error: Exception | None = None

        for attempt in range(self.settings.max_retries + 1):
            try:
                response = self.session.post(
                    self.settings.full_api_url,
                    json=params.to_dict(),
                    timeout=self.settings.timeout,
                )

                # 检查 HTTP 状态码
                if response.status_code != 200:
                    raise RuntimeError(f"HTTP 错误: {response.status_code}")

                # 解析 JSON 响应
                data = response.json()

                return APIResponse.model_validate(data)

            except requests.RequestException as e:
                last_error = e
                if attempt < self.settings.max_retries:
                    # 等待后重试
                    time.sleep(1)
                    continue
                raise

        # 所有重试都失败
        if last_error:
            raise last_error
        raise RuntimeError("未知错误")

    def fetch_all_products(self) -> list[dict]:
        """获取所有产品（分页处理）

        Returns:
            list[dict]: 所有产品记录
        """
        all_records: list[dict] = []
        current_page = 1
        total = 0

        while True:
            # 构建请求参数
            params = FetchParams(
                size=self.settings.page_size,
                current=current_page,
            )

            # 获取当前页数据
            response = self.fetch_products(params)

            if not response.data:
                break

            records = response.data.get("records", [])
            if not records:
                break

            # 添加到结果列表
            all_records.extend(records)

            # 更新总数
            total = response.data.get("total", 0)

            # 检查是否还有下一页
            if len(all_records) >= total:
                break

            current_page += 1

        return all_records
