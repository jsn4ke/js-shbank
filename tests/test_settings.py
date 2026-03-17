"""测试配置管理模块"""
from pathlib import Path

import pytest

from js_shbank.config.settings import Settings, get_settings


class TestSettings:
    """测试 Settings 类"""

    def test_default_values(self):
        """测试默认值"""
        settings = Settings()
        assert settings.api_base_url == "https://www.bosc.cn/apiQry"
        assert settings.timeout == 30
        assert settings.max_retries == 3
        assert settings.page_size == 50
        assert settings.data_dir == Path("data")
        assert settings.api_endpoint == "/apiPCQry/qryPcFinanceProductZh"

    def test_api_base_url_from_env(self, monkeypatch):
        """测试从环境变量读取 API_BASE_URL"""
        monkeypatch.setenv("API_BASE_URL", "https://test.example.com/api")
        settings = Settings()
        assert settings.api_base_url == "https://test.example.com/api"

    def test_timeout_from_env(self, monkeypatch):
        """测试从环境变量读取 TIMEOUT"""
        monkeypatch.setenv("TIMEOUT", "60")
        settings = Settings()
        assert settings.timeout == 60

    def test_max_retries_from_env(self, monkeypatch):
        """测试从环境变量读取 MAX_RETRIES"""
        monkeypatch.setenv("MAX_RETRIES", "5")
        settings = Settings()
        assert settings.max_retries == 5

    def test_page_size_from_env(self, monkeypatch):
        """测试从环境变量读取 PAGE_SIZE"""
        monkeypatch.setenv("PAGE_SIZE", "20")
        settings = Settings()
        assert settings.page_size == 20

    def test_data_dir_from_env(self, monkeypatch, tmp_path):
        """测试从环境变量读取 DATA_DIR"""
        monkeypatch.setenv("DATA_DIR", str(tmp_path))
        settings = Settings()
        assert settings.data_dir == tmp_path

    def test_full_api_url(self):
        """测试完整 API URL 构建"""
        settings = Settings()
        expected = "https://www.bosc.cn/apiQry/apiPCQry/qryPcFinanceProductZh"
        assert settings.full_api_url == expected

    def test_invalid_timeout_env(self, monkeypatch):
        """测试无效的 TIMEOUT 环境变量"""
        monkeypatch.setenv("TIMEOUT", "invalid")
        with pytest.raises(ValueError):
            Settings()

    def test_invalid_max_retries_env(self, monkeypatch):
        """测试无效的 MAX_RETRIES 环境变量"""
        monkeypatch.setenv("MAX_RETRIES", "invalid")
        with pytest.raises(ValueError):
            Settings()

    def test_negative_values(self):
        """测试负值验证"""
        with pytest.raises(ValueError):
            Settings(timeout=-1)
        with pytest.raises(ValueError):
            Settings(max_retries=-1)
        with pytest.raises(ValueError):
            Settings(page_size=0)


class TestGetSettings:
    """测试 get_settings 函数"""

    def test_singleton_behavior(self):
        """测试单例行为"""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

    def test_same_instance(self):
        """测试返回同一实例"""
        settings = get_settings()
        settings_same = get_settings()
        assert settings == settings_same
