"""
LLM Switch 服務模組

實現 LLM 服務單例，提供全局訪問點。
"""

from typing import Dict, Any, Optional

from ..config import ConfigManager
from ..exceptions import ConfigError
from .factory import LLMFactory
from .base import LLMProvider

class LLMService:
    """LLM 服務單例"""

    _instance = None

    def __init__(self):
        """初始化服務"""
        self.config_manager = ConfigManager()
        self.initialized = False
        self._provider_cache = {}

    @classmethod
    def get_instance(cls) -> 'LLMService':
        """
        獲取單例實例

        Returns:
            LLMService 實例
        """
        if cls._instance is None:
            cls._instance = LLMService()
        return cls._instance

    @classmethod
    def initialize(cls, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        初始化服務

        Args:
            config_path: 設定檔路徑
            config_dict: 設定字典

        Raises:
            ConfigError: 當初始化失敗時
        """
        instance = cls.get_instance()
        instance.config_manager.load_config(config_path, config_dict)
        instance.initialized = True

        # 清除提供商緩存
        instance._provider_cache = {}

    def get_provider(self, provider_name: Optional[str] = None) -> LLMProvider:
        """
        獲取提供商實例

        Args:
            provider_name: 提供商名稱，如果為 None，則返回預設提供商

        Returns:
            提供商實例

        Raises:
            ConfigError: 當服務未初始化或提供商不存在時
        """
        if not self.initialized:
            raise ConfigError("LLM 服務尚未初始化")

        if provider_name is None:
            provider_name = self.config_manager.get_default_provider()

        # 檢查緩存
        if provider_name in self._provider_cache:
            return self._provider_cache[provider_name]

        # 獲取提供商配置
        provider_config = self.config_manager.get_provider_config(provider_name)

        # 創建提供商實例
        provider = LLMFactory.create(provider_name, **provider_config)

        # 緩存提供商實例
        self._provider_cache[provider_name] = provider

        return provider

    def get_model_info(self, provider_name: str, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        獲取模型資訊

        Args:
            provider_name: 提供商名稱
            model_name: 模型名稱，如果為 None，則返回預設模型資訊

        Returns:
            模型資訊字典

        Raises:
            ConfigError: 當服務未初始化或模型不存在時
        """
        if not self.initialized:
            raise ConfigError("LLM 服務尚未初始化")

        return self.config_manager.get_model_info(provider_name, model_name)
