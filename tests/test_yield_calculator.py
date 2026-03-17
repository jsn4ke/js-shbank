"""年化计算器测试"""

import pytest

from js_shbank.calculator.yield_calculator import YieldCalculator


class TestCalculateFromNav:
    """基础年化计算测试"""

    def test_calculate_from_nav_positive(self) -> None:
        """测试正向年化计算"""
        # 初始净值 1.0，当前净值 1.05，经过 90 天
        # 年化 = (1.05 / 1.0 - 1) × (365 / 90) × 100%
        #       = 0.05 × 4.0556 × 100%
        #       ≈ 20.28%
        result = YieldCalculator.calculate_from_nav(1.0, 1.05, 90)
        assert result == pytest.approx(20.28, 0.01)

    def test_calculate_from_nav_zero_days(self) -> None:
        """测试天数为1（最小有效值）"""
        result = YieldCalculator.calculate_from_nav(1.0, 1.05, 1)
        assert result > 0

    def test_calculate_from_nav_negative_days(self) -> None:
        """测试负天数"""
        with pytest.raises(ValueError, match="天数必须大于0"):
            YieldCalculator.calculate_from_nav(1.0, 1.05, -10)

    def test_calculate_from_nav_zero_initial(self) -> None:
        """测试初始净值为0"""
        with pytest.raises(ValueError, match="初始净值不能为0"):
            YieldCalculator.calculate_from_nav(0.0, 1.05, 90)

    def test_calculate_from_nav_equal_navs(self) -> None:
        """测试净值相等（无增长）"""
        # (1.0 / 1.0 - 1) = 0，年化应为0
        result = YieldCalculator.calculate_from_nav(1.0, 1.0, 90)
        assert result == 0.0

    def test_calculate_from_nav_negative_yield(self) -> None:
        """测试负收益"""
        # 当前净值小于初始净值
        result = YieldCalculator.calculate_from_nav(1.05, 1.0, 90)
        # 年化应该是负数
        assert result < 0

    def test_calculate_from_nav_precision(self) -> None:
        """测试精度保留"""
        # 验证结果保留2位小数
        result = YieldCalculator.calculate_from_nav(1.0, 1.05, 90)
        # 检查小数位数
        decimal_part = str(result).split(".")[1]
        assert len(decimal_part) <= 2


class TestCalculateNDayYield:
    """多日年化计算测试"""

    def test_calculate_7_day_yield(self) -> None:
        """测试7日年化计算"""
        historical_navs = [1.0000, 1.0005, 1.0010, 1.0015, 1.0020, 1.0025, 1.0030]
        # 使用第1天和第7天的净值
        # (1.0030 / 1.0000 - 1) × (365 / 6) × 100%
        result = YieldCalculator.calculate_7_day_yield(historical_navs)
        assert result is not None
        assert result > 0

    def test_calculate_7_day_yield_insufficient_data(self) -> None:
        """测试历史数据不足"""
        historical_navs = [1.0000, 1.0005]
        result = YieldCalculator.calculate_7_day_yield(historical_navs)
        assert result is None

    def test_calculate_7_day_yield_exactly_7(self) -> None:
        """测试正好7天数据"""
        historical_navs = [1.0000, 1.0005, 1.0010, 1.0015, 1.0020, 1.0025, 1.0030]
        result = YieldCalculator.calculate_7_day_yield(historical_navs)
        assert result is not None

    def test_calculate_3_day_yield(self) -> None:
        """测试3日年化计算"""
        historical_navs = [1.0000, 1.0010, 1.0020]
        # 使用第1天和第3天的净值
        result = YieldCalculator.calculate_3_day_yield(historical_navs)
        assert result is not None
        assert result > 0

    def test_calculate_3_day_yield_insufficient_data(self) -> None:
        """测试历史数据不足"""
        historical_navs = [1.0000]
        result = YieldCalculator.calculate_3_day_yield(historical_navs)
        assert result is None

    def test_calculate_3_day_yield_exactly_3(self) -> None:
        """测试正好3天数据"""
        historical_navs = [1.0000, 1.0010, 1.0020]
        result = YieldCalculator.calculate_3_day_yield(historical_navs)
        assert result is not None


class TestCalculateNDayYieldGeneric:
    """通用多日年化计算测试"""

    def test_calculate_n_day_yield_2_day(self) -> None:
        """测试2日年化（边界情况）"""
        historical_navs = [1.0000, 1.0010]
        result = YieldCalculator.calculate_n_day_yield(historical_navs, 2)
        assert result is not None

    def test_calculate_n_day_yield_zero_n(self) -> None:
        """测试n=0（无效情况）"""
        historical_navs = [1.0000, 1.0010]
        with pytest.raises(ValueError, match="天数n必须大于0"):
            YieldCalculator.calculate_n_day_yield(historical_navs, 0)

    def test_calculate_n_day_yield_negative_n(self) -> None:
        """测试负n（无效情况）"""
        historical_navs = [1.0000, 1.0010]
        with pytest.raises(ValueError, match="天数n必须大于0"):
            YieldCalculator.calculate_n_day_yield(historical_navs, -1)


class TestInvalidInputs:
    """无效输入测试"""

    def test_empty_historical_navs(self) -> None:
        """测试空历史数据"""
        result = YieldCalculator.calculate_n_day_yield([], 7)
        assert result is None

    def test_single_nav(self) -> None:
        """测试单个净值（无法计算年化）"""
        result = YieldCalculator.calculate_n_day_yield([1.0], 7)
        assert result is None
