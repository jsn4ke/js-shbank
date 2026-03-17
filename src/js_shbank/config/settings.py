"""配置管理模块"""
import os
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator


class Settings(BaseModel):
    """配置类"""

    api_base_url: str = Field(
        default="https://www.bosc.cn/apiQry",
        description="API 基础 URL",
    )
    api_endpoint: str = Field(
        default="/apiPCQry/qryPcFinanceProductZh",
        description="API 端点",
    )
    timeout: int = Field(
        default=30,
        description="请求超时时间（秒）",
    )
    max_retries: int = Field(
        default=3,
        description="最大重试次数",
    )
    page_size: int = Field(
        default=50,
        description="分页大小",
    )
    data_dir: Path = Field(
        default=Path("data"),
        description="数据存储目录",
    )

    @model_validator(mode="before")
    @classmethod
    def load_from_env(cls, values: dict) -> dict:
        """从环境变量加载配置"""
        env_mapping = {
            "API_BASE_URL": "api_base_url",
            "API_ENDPOINT": "api_endpoint",
            "TIMEOUT": "timeout",
            "MAX_RETRIES": "max_retries",
            "PAGE_SIZE": "page_size",
            "DATA_DIR": "data_dir",
        }
        for env_key, field_name in env_mapping.items():
            env_value = os.getenv(env_key)
            if env_value is not None:
                values[field_name] = env_value
        return values

    @field_validator("timeout", "max_retries", "page_size", mode="before")
    @classmethod
    def validate_positive_int(cls, v: str | int) -> int:
        """验证正整数"""
        if isinstance(v, str):
            try:
                v = int(v)
            except ValueError as e:
                raise ValueError("必须是正整数") from e
        if v <= 0:
            raise ValueError("必须是正整数")
        return v

    @field_validator("data_dir", mode="before")
    @classmethod
    def validate_data_dir(cls, v: str | Path) -> Path:
        """验证数据目录"""
        if isinstance(v, str):
            v = Path(v)
        return v

    @property
    def full_api_url(self) -> str:
        """获取完整的 API URL"""
        return f"{self.api_base_url}{self.api_endpoint}"


# 全局配置实例
_settings: Settings | None = None


def get_settings() -> Settings:
    """获取配置单例实例"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
