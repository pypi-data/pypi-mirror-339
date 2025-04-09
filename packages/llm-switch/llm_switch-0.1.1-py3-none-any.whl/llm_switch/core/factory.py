"""
LLM Switch 工廠模組

實現工廠模式，用於創建 LLM 提供商實例。
"""

import importlib
from typing import Dict, Type

from ..exceptions import ConfigError
from .base import LLMProvider

class LLMFactory:
    """LLM 提供商工廠"""

    _providers: Dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register(cls, provider_name: str, provider_class: Type[LLMProvider]) -> None:
        """
        註冊提供商類

        Args:
            provider_name: 提供商名稱
            provider_class: 提供商類
        """
        cls._providers[provider_name] = provider_class

    @classmethod
    def create(cls, provider_name: str, **config) -> LLMProvider:
        """
        創建提供商實例

        Args:
            provider_name: 提供商名稱
            **config: 提供商配置

        Returns:
            提供商實例

        Raises:
            ConfigError: 當提供商不存在時
        """
        # 如果提供商尚未註冊，嘗試動態導入
        if provider_name not in cls._providers:
            try:
                # 嘗試導入提供商模組
                module_name = f"llm_switch.providers.{provider_name}"
                module = importlib.import_module(module_name)

                # 尋找提供商類
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                        issubclass(attr, LLMProvider) and
                        attr.__name__.lower().startswith(provider_name.lower())):
                        cls.register(provider_name, attr)
                        break
            except (ImportError, AttributeError):
                pass

        # 檢查提供商是否已註冊
        if provider_name not in cls._providers:
            raise ConfigError(f"未知的提供商: {provider_name}")

        # 創建提供商實例
        provider_class = cls._providers[provider_name]
        return provider_class(**config)

    @classmethod
    def get_registered_providers(cls) -> Dict[str, Type[LLMProvider]]:
        """
        獲取所有註冊的提供商

        Returns:
            提供商字典，鍵為提供商名稱，值為提供商類
        """
        return cls._providers.copy()
