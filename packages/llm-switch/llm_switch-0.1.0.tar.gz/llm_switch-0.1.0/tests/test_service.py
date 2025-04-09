"""
測試 LLM 服務
"""

import unittest
from unittest.mock import patch, MagicMock

from llm_switch.core.service import LLMService
from llm_switch.exceptions import ConfigError

class TestLLMService(unittest.TestCase):
    """測試 LLM 服務"""
    
    def setUp(self):
        """設置測試環境"""
        # 重置單例
        LLMService._instance = None
        
        # 基本配置
        self.config = {
            "LLM_CONFIG": {
                "default_provider": "test_provider",
                "providers": {
                    "test_provider": {
                        "api_key": "test-api-key",
                        "model": "test-model"
                    }
                }
            }
        }
    
    def test_get_instance(self):
        """測試獲取單例實例"""
        instance1 = LLMService.get_instance()
        instance2 = LLMService.get_instance()
        self.assertIs(instance1, instance2)
    
    def test_initialize(self):
        """測試初始化服務"""
        LLMService.initialize(config_dict=self.config)
        instance = LLMService.get_instance()
        self.assertTrue(instance.initialized)
    
    def test_get_provider_without_initialization(self):
        """測試在未初始化時獲取提供商"""
        instance = LLMService.get_instance()
        with self.assertRaises(ConfigError):
            instance.get_provider()
    
    @patch("llm_switch.core.factory.LLMFactory.create")
    def test_get_provider(self, mock_create):
        """測試獲取提供商"""
        # 設置模擬對象
        mock_provider = MagicMock()
        mock_create.return_value = mock_provider
        
        # 初始化服務
        LLMService.initialize(config_dict=self.config)
        
        # 獲取提供商
        instance = LLMService.get_instance()
        provider = instance.get_provider()
        
        # 驗證
        self.assertEqual(provider, mock_provider)
        mock_create.assert_called_once_with("test_provider", api_key="test-api-key", model="test-model")
    
    @patch("llm_switch.core.factory.LLMFactory.create")
    def test_get_specific_provider(self, mock_create):
        """測試獲取特定提供商"""
        # 設置模擬對象
        mock_provider = MagicMock()
        mock_create.return_value = mock_provider
        
        # 初始化服務
        LLMService.initialize(config_dict=self.config)
        
        # 獲取特定提供商
        instance = LLMService.get_instance()
        provider = instance.get_provider("test_provider")
        
        # 驗證
        self.assertEqual(provider, mock_provider)
        mock_create.assert_called_once_with("test_provider", api_key="test-api-key", model="test-model")
    
    def test_get_model_info(self):
        """測試獲取模型資訊"""
        # 初始化服務
        LLMService.initialize(config_dict=self.config)
        
        # 獲取模型資訊
        instance = LLMService.get_instance()
        model_info = instance.get_model_info("test_provider")
        
        # 驗證
        self.assertEqual(model_info["capabilities"], ["text"])

if __name__ == "__main__":
    unittest.main()
