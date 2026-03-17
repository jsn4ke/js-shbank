"""产品数据模型"""
import datetime
from typing import Any

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    """理财产品数据模型"""

    # 基本信息
    prd_code: str = Field(..., description="产品代码")
    prd_name: str = Field(..., description="产品名称")

    # 收益率相关
    rate: str | None = Field(None, description="年化收益率")
    rate_script: str | None = Field(None, description="收益率备注")
    week_year_rate: str | None = Field(None, description="近七日年化")
    month_year_rate: str | None = Field(None, description="近一月年化")
    three_month_year_rate: str | None = Field(None, description="近三月年化")
    half_year_year_rate: str | None = Field(None, description="近半年年化")

    # 净值相关
    unit_rate: str | None = Field(None, description="单位净值")
    estab_ratio: str | None = Field(None, description="成立以来净值")

    # 其他信息
    risk_level: int | None = Field(None, description="风险等级 0-5")
    curr_type: str | None = Field(None, description="币种 CNY/USD")
    pfirst_amt: float | None = Field(None, description="起售金额(单位:元)")
    sold_out: int | None = Field(None, description="是否售罄 0=否 1=是")
    prd_labels: str | None = Field(None, description="产品标签 @!@分隔")

    # URL 相关
    detail_page_url: str | None = Field(default=None, description="产品详情页 URL")

    # 元数据
    fetched_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description="抓取时间",
    )


class APIResponse(BaseModel):
    """API 响应数据模型"""

    code: int = Field(..., description="响应码")
    success: bool = Field(..., description="是否成功")
    data: dict[str, Any] | None = Field(None, description="响应数据")
