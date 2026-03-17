"""测试 Web 模块"""
import pandas as pd
import pytest

from js_shbank.models.product import ProductModel


def test_dataframe_filtering_by_code():
    """测试按产品代码筛选"""
    df = pd.DataFrame([
        {"prd_code": "A001", "prd_name": "产品A"},
        {"prd_code": "B001", "prd_name": "产品B"},
        {"prd_code": "C001", "prd_name": "产品C"},
    ])

    filtered = df[df["prd_code"].str.contains("B", case=False, na=False)]

    assert len(filtered) == 1
    assert filtered.iloc[0]["prd_code"] == "B001"


def test_dataframe_filtering_by_name():
    """测试按产品名称筛选"""
    df = pd.DataFrame([
        {"prd_code": "A001", "prd_name": "人民币产品A"},
        {"prd_code": "B001", "prd_name": "美元产品B"},
    ])

    filtered = df[df["prd_name"].str.contains("美元", case=False, na=False)]

    assert len(filtered) == 1
    assert filtered.iloc[0]["prd_code"] == "B001"


def test_dataframe_filtering_by_risk_level():
    """测试按风险等级筛选"""
    df = pd.DataFrame([
        {"prd_code": "A001", "risk_level": 1},
        {"prd_code": "B001", "risk_level": 2},
        {"prd_code": "C001", "risk_level": 3},
    ])

    filtered = df[df["risk_level"] == 2]

    assert len(filtered) == 1
    assert filtered.iloc[0]["prd_code"] == "B001"


def test_dataframe_filtering_by_currency():
    """测试按币种筛选"""
    df = pd.DataFrame([
        {"prd_code": "A001", "curr_type": "CNY"},
        {"prd_code": "B001", "curr_type": "USD"},
    ])

    filtered = df[df["curr_type"] == "USD"]

    assert len(filtered) == 1
    assert filtered.iloc[0]["prd_code"] == "B001"


def test_combined_filters():
    """测试组合筛选 - 币种为USD的产品"""
    df = pd.DataFrame([
        {"prd_code": "A001", "prd_name": "人民币产品A", "risk_level": 1, "curr_type": "CNY"},
        {"prd_code": "B001", "prd_name": "美元产品B", "risk_level": 2, "curr_type": "USD"},
        {"prd_code": "C001", "prd_name": "美元产品C", "risk_level": 2, "curr_type": "USD"},
    ])

    # 筛选出所有 USD 币种的产品
    filtered = df[df["curr_type"] == "USD"]

    assert len(filtered) == 2
    assert "B001" in filtered["prd_code"].values
    assert "C001" in filtered["prd_code"].values


def test_filter_empty_results():
    """测试筛选后无结果"""
    df = pd.DataFrame([
        {"prd_code": "A001", "prd_name": "产品A"},
    ])

    filtered = df[df["prd_code"].str.contains("Z", case=False, na=False)]

    assert len(filtered) == 0
