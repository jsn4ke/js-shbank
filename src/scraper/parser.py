"""数据解析器模块"""

import re
from typing import Any

from src.models.product import ProductModel


class Parser:
    """数据解析器"""

    # 风险等级映射
    RISK_LEVEL_MAP = {
        0: "",
        1: "R1极低风险",
        2: "R2低风险",
        3: "R3中风险",
        4: "R4中高风险",
        5: "R5高风险",
    }

    # 币种映射
    CURRENCY_TYPE_MAP = {
        "CNY": "人民币",
        "USD": "美元",
    }

    @staticmethod
    def parse_labels(labels_str: str | None) -> list[str]:
        """解析标签字符串

        Args:
            labels_str: 标签字符串，使用 @!@ 分隔

        Returns:
            list[str]: 标签列表
        """
        if not labels_str:
            return []
        return labels_str.split("@!@")

    @staticmethod
    def _map_risk_level(risk_level: int | None) -> str | None:
        """映射风险等级

        Args:
            risk_level: 风险等级数字

        Returns:
            str | None: 风险等级描述
        """
        if risk_level is None:
            return None
        return Parser.RISK_LEVEL_MAP.get(risk_level, "未知风险")

    @staticmethod
    def _map_curr_type(curr_type: str | None) -> str | None:
        """映射币种

        Args:
            curr_type: 币种代码

        Returns:
            str | None: 币种名称
        """
        if curr_type is None:
            return None
        return Parser.CURRENCY_TYPE_MAP.get(curr_type, curr_type)

    @staticmethod
    def _map_sold_out(sold_out: int | None) -> str | None:
        """映射是否售罄

        Args:
            sold_out: 是否售罄 0=否 1=是

        Returns:
            str | None: 售罄状态
        """
        if sold_out is None:
            return None
        return "是" if sold_out == 1 else "否"

    @staticmethod
    def _format_amount(amount: int | None) -> str | None:
        """格式化金额

        Args:
            amount: 金额数值

        Returns:
            str | None: 格式化后的金额字符串
        """
        if amount is None:
            return None
        return f"{amount}元"

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """驼峰转下划线

        Args:
            name: 驼峰命名

        Returns:
            str: 下划线命名
        """
        # 将大写字母前插入下划线（除了第一个字母）
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def parse_product(record: dict[str, Any]) -> ProductModel:
        """解析单条产品记录

        Args:
            record: 原始产品记录

        Returns:
            ProductModel: 产品模型对象
        """
        # 转换字段名：驼峰转下划线
        converted: dict[str, Any] = {}
        for key, value in record.items():
            snake_key = Parser._camel_to_snake(key)
            converted[snake_key] = value

        # 使用 ProductModel 解析，允许额外字段
        return ProductModel.model_validate(converted)

    @staticmethod
    def parse_api_response(response_data: dict[str, Any] | None) -> list[ProductModel]:
        """解析 API 响应数据

        Args:
            response_data: API 响应数据

        Returns:
            list[ProductModel]: 产品模型列表
        """
        if not response_data:
            return []

        records = response_data.get("records", [])
        if not records:
            return []

        return [Parser.parse_product(record) for record in records]
