"""年化计算器模块"""


class YieldCalculator:
    """年化收益率计算器"""

    @staticmethod
    def calculate_from_nav(initial_nav: float, current_nav: float, days: int) -> float:
        """从净值计算年化收益率

        Args:
            initial_nav: 初始净值
            current_nav: 当前净值
            days: 经过的天数

        Returns:
            float: 年化收益率（百分比）

        Raises:
            ValueError: 如果输入值无效
        """
        # 验证输入
        if initial_nav == 0:
            raise ValueError("初始净值不能为0")
        if days < 1:
            raise ValueError("天数必须大于0")

        # 计算年化收益率
        # 公式：(当前净值 / 初始净值 - 1) × (365 / 天数) × 100%
        return round(
            (current_nav / initial_nav - 1) * (365 / days) * 100,
            2,
        )

    @staticmethod
    def calculate_n_day_yield(historical_navs: list[float], n: int) -> float | None:
        """计算n日年化收益率

        Args:
            historical_navs: 历史净值列表（从旧到新）
            n: 计算天数

        Returns:
            float | None: 年化收益率（百分比），如果数据不足则返回 None

        Raises:
            ValueError: 如果 n <= 0
        """
        # 验证输入
        if n <= 0:
            raise ValueError("天数n必须大于0")

        # 需要至少 n 个净值数据
        if len(historical_navs) < n:
            return None

        # 使用第1天和第n天的净值计算
        # 历史数据是从旧到新的，第1天是最早的，第n天是当前的
        # 实际经过的天数 = n - 1
        initial_nav = historical_navs[0]
        current_nav = historical_navs[n - 1]

        return YieldCalculator.calculate_from_nav(initial_nav, current_nav, n - 1)

    @staticmethod
    def calculate_7_day_yield(historical_navs: list[float]) -> float | None:
        """计算7日年化收益率

        Args:
            historical_navs: 历史净值列表（从旧到新）

        Returns:
            float | None: 7日年化收益率，如果数据不足则返回 None
        """
        return YieldCalculator.calculate_n_day_yield(historical_navs, 7)

    @staticmethod
    def calculate_3_day_yield(historical_navs: list[float]) -> float | None:
        """计算3日年化收益率

        Args:
            historical_navs: 历史净值列表（从旧到新）

        Returns:
            float | None: 3日年化收益率，如果数据不足则返回 None
        """
        return YieldCalculator.calculate_n_day_yield(historical_navs, 3)
