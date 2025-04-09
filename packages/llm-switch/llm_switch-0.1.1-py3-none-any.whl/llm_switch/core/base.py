"""
LLM Switch 基礎介面模組

定義了所有 LLM 提供商必須實現的抽象基類和介面。
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any

from .response import LLMResponse

class LLMProvider(ABC):
    """LLM 提供商抽象基類"""
    
    def __init__(self, api_key: str, model: str, **kwargs):
        """
        初始化 LLM 提供商
        
        Args:
            api_key: API 金鑰
            model: 模型名稱
            **kwargs: 其他參數
        """
        self.api_key = api_key
        self.model = model
        self.kwargs = kwargs
    
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        生成文本補全
        
        Args:
            prompt: 提示文本
            **kwargs: 其他參數
        
        Returns:
            標準化的 LLM 回應物件
        """
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        生成聊天補全
        
        Args:
            messages: 聊天訊息列表，每個訊息是一個字典，包含 'role' 和 'content' 鍵
            **kwargs: 其他參數
        
        Returns:
            標準化的 LLM 回應物件
        """
        pass
    
    @abstractmethod
    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量
        
        Args:
            text: 文本或文本列表
            **kwargs: 其他參數
        
        Returns:
            嵌入向量或嵌入向量列表
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊
        
        Returns:
            模型資訊字典
        """
        # 這個方法可以在子類中覆寫，以提供更詳細的模型資訊
        return {
            'model': self.model,
            'provider': self.__class__.__name__.replace('Provider', '').lower(),
            'capabilities': ['text'],  # 預設只支援文本
        }
    
    def supports_capability(self, capability: str) -> bool:
        """
        檢查是否支援特定能力
        
        Args:
            capability: 能力名稱
        
        Returns:
            是否支援
        """
        return capability in self.get_model_info().get('capabilities', [])
