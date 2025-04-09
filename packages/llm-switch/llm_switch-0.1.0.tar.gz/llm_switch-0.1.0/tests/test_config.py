"""
測試配置管理器
"""

import os
import unittest
from unittest.mock import patch
import tempfile
import yaml

from llm_switch.config import ConfigManager
from llm_switch.exceptions import ConfigError

class TestConfigManager(unittest.TestCase):
    """測試配置管理器"""
    
    def setUp(self):
        """設置測試環境"""
        self.config_manager = ConfigManager()
        
        # 創建臨時配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "test_config.yaml")
        
        # 基本配置
        self.config = {
            "LLM_CONFIG": {
                "default_provider": "test_provider",
                "providers": {
                    "test_provider": {
                        "api_key": "${TEST_API_KEY}",
                        "model": "test-model"
                    }
                }
            }
        }
        
        # 寫入配置文件
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f)
    
    def tearDown(self):
        """清理測試環境"""
        self.temp_dir.cleanup()
    
    def test_load_config_from_file(self):
        """測試從文件載入配置"""
        self.config_manager.load_config(self.config_path)
        self.assertTrue(self.config_manager.loaded)
        self.assertEqual(self.config_manager.get_default_provider(), "test_provider")
    
    def test_load_config_from_dict(self):
        """測試從字典載入配置"""
        self.config_manager.load_config(config_dict=self.config)
        self.assertTrue(self.config_manager.loaded)
        self.assertEqual(self.config_manager.get_default_provider(), "test_provider")
    
    def test_get_provider_config(self):
        """測試獲取提供商配置"""
        self.config_manager.load_config(config_dict=self.config)
        provider_config = self.config_manager.get_provider_config("test_provider")
        self.assertEqual(provider_config["model"], "test-model")
    
    def test_get_default_provider(self):
        """測試獲取預設提供商"""
        self.config_manager.load_config(config_dict=self.config)
        self.assertEqual(self.config_manager.get_default_provider(), "test_provider")
    
    def test_get_all_providers(self):
        """測試獲取所有提供商"""
        self.config_manager.load_config(config_dict=self.config)
        providers = self.config_manager.get_all_providers()
        self.assertEqual(providers, ["test_provider"])
    
    @patch.dict(os.environ, {"TEST_API_KEY": "test-api-key-value"})
    def test_env_var_replacement(self):
        """測試環境變量替換"""
        self.config_manager.load_config(self.config_path)
        provider_config = self.config_manager.get_provider_config("test_provider")
        self.assertEqual(provider_config["api_key"], "test-api-key-value")
    
    def test_invalid_config(self):
        """測試無效配置"""
        invalid_config = {"invalid": "config"}
        with self.assertRaises(ConfigError):
            self.config_manager.load_config(config_dict=invalid_config)

if __name__ == "__main__":
    unittest.main()
