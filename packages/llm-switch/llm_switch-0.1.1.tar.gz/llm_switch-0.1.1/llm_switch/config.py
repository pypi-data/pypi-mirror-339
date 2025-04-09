"""
LLM Switch 配置管理模組

負責讀取和解析設定檔，支援多種格式 (YAML, JSON, Python 字典)。
"""

import os
import re
import yaml
import json
from typing import Dict, Any, Optional, List

try:
    from dotenv import load_dotenv
except ImportError:
    # 如果沒有安裝 python-dotenv，則定義一個空函數
    def load_dotenv():
        pass

from .exceptions import ConfigError

class ConfigManager:
    """配置管理器，負責讀取和解析設定檔"""

    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.loaded = False

        # 載入環境變量
        load_dotenv()

    def load_config(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        載入設定檔

        Args:
            config_path: 設定檔路徑，支援 YAML 和 JSON 格式
            config_dict: 直接提供設定字典

        Raises:
            ConfigError: 當設定檔載入失敗時
        """
        if config_dict is not None:
            self.config = config_dict
            self.loaded = True
            return

        if config_path is None:
            # 嘗試從預設位置載入
            default_locations = [
                "./llm_config.yaml",
                "./llm_config.yml",
                "./llm_config.json",
                os.path.expanduser("~/.llm_config.yaml"),
                os.path.expanduser("~/.llm_config.yml"),
                os.path.expanduser("~/.llm_config.json"),
            ]

            for location in default_locations:
                if os.path.exists(location):
                    config_path = location
                    break

            if config_path is None:
                raise ConfigError("找不到設定檔，請提供 config_path 或 config_dict")

        if not os.path.exists(config_path):
            raise ConfigError(f"設定檔不存在: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # 替換環境變量
                content = self._replace_env_vars(content)

                if config_path.endswith(('.yaml', '.yml')):
                    self.config = yaml.safe_load(content)
                elif config_path.endswith('.json'):
                    self.config = json.loads(content)
                else:
                    raise ConfigError(f"不支援的設定檔格式: {config_path}")

            # 驗證設定檔格式
            self._validate_config()
            self.loaded = True

        except Exception as e:
            raise ConfigError(f"載入設定檔失敗: {str(e)}")

    def _validate_config(self) -> None:
        """
        驗證設定檔格式

        Raises:
            ConfigError: 當設定檔格式無效時
        """
        if not isinstance(self.config, dict):
            raise ConfigError("設定檔必須是一個字典")

        if 'LLM_CONFIG' not in self.config:
            raise ConfigError("設定檔必須包含 'LLM_CONFIG' 鍵")

        llm_config = self.config['LLM_CONFIG']

        if not isinstance(llm_config, dict):
            raise ConfigError("LLM_CONFIG 必須是一個字典")

        if 'providers' not in llm_config:
            raise ConfigError("LLM_CONFIG 必須包含 'providers' 鍵")

        if not isinstance(llm_config['providers'], dict):
            raise ConfigError("providers 必須是一個字典")

        if 'default_provider' not in llm_config:
            raise ConfigError("LLM_CONFIG 必須包含 'default_provider' 鍵")

        default_provider = llm_config['default_provider']

        if default_provider not in llm_config['providers']:
            raise ConfigError(f"預設提供商 '{default_provider}' 不在提供商列表中")

    def get_provider_config(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """
        獲取提供商配置

        Args:
            provider_name: 提供商名稱，如果為 None，則返回預設提供商配置

        Returns:
            提供商配置字典

        Raises:
            ConfigError: 當提供商不存在或設定檔未載入時
        """
        if not self.loaded:
            raise ConfigError("設定檔尚未載入")

        llm_config = self.config['LLM_CONFIG']

        if provider_name is None:
            provider_name = llm_config['default_provider']

        if provider_name not in llm_config['providers']:
            raise ConfigError(f"提供商 '{provider_name}' 不存在")

        return llm_config['providers'][provider_name]

    def get_model_info(self, provider_name: str, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        獲取模型資訊

        Args:
            provider_name: 提供商名稱
            model_name: 模型名稱，如果為 None，則返回預設模型資訊

        Returns:
            模型資訊字典

        Raises:
            ConfigError: 當模型不存在或設定檔未載入時
        """
        provider_config = self.get_provider_config(provider_name)

        if model_name is None:
            model_name = provider_config.get('model')
            if model_name is None:
                raise ConfigError(f"提供商 '{provider_name}' 未指定預設模型")

        # 檢查是否有詳細的模型配置
        if 'models' in provider_config and model_name in provider_config['models']:
            return provider_config['models'][model_name]

        # 如果沒有詳細配置，返回基本資訊
        return {
            'capabilities': ['text'],  # 假設至少支援文本
            'input_cost_per_1M': 0.0,  # 未知成本
            'output_cost_per_1M': 0.0,  # 未知成本
            'context_window': 4096,  # 假設的上下文窗口
        }

    def get_default_provider(self) -> str:
        """
        獲取預設提供商名稱

        Returns:
            預設提供商名稱

        Raises:
            ConfigError: 當設定檔未載入時
        """
        if not self.loaded:
            raise ConfigError("設定檔尚未載入")

        return self.config['LLM_CONFIG']['default_provider']

    def _replace_env_vars(self, content: str) -> str:
        """
        替換內容中的環境變量引用

        Args:
            content: 要處理的內容

        Returns:
            替換後的內容
        """
        # 匹配 ${ENV_VAR} 或 $ENV_VAR 格式
        pattern = r'\${([^}]+)}|\$([A-Za-z0-9_]+)'

        def replace_env_var(match):
            # 取得環境變量名稱（兩種格式）
            env_var = match.group(1) or match.group(2)
            # 從環境變量中獲取值，如果不存在則保持原樣
            env_value = os.environ.get(env_var)
            if env_value is not None:
                return env_value
            return match.group(0)  # 如果環境變量不存在，保持原樣

        # 替換所有環境變量引用
        return re.sub(pattern, replace_env_var, content)

    def get_all_providers(self) -> List[str]:
        """
        獲取所有提供商名稱

        Returns:
            所有提供商名稱列表

        Raises:
            ConfigError: 當設定檔未載入時
        """
        if not self.loaded:
            raise ConfigError("設定檔尚未載入")

        return list(self.config['LLM_CONFIG']['providers'].keys())
