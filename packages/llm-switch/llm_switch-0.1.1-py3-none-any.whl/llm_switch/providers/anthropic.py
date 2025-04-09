"""
Anthropic 提供商實現
"""

import json
from typing import Dict, List, Optional, Union, Any

try:
    import anthropic
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import AnthropicError, AuthenticationError, RateLimitError, InvalidRequestError

class AnthropicProvider(LLMProvider):
    """Anthropic 提供商實現"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-opus-20240229",
        api_base: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 Anthropic 提供商
        
        Args:
            api_key: Anthropic API 金鑰
            model: 模型名稱
            api_base: API 基礎 URL
            temperature: 溫度參數
            max_tokens: 最大生成 token 數
            **kwargs: 其他參數
        
        Raises:
            ImportError: 當 anthropic 套件未安裝時
        """
        super().__init__(api_key=api_key, model=model, **kwargs)
        
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("請安裝 anthropic 套件: pip install anthropic")
        
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # 初始化 Anthropic 客戶端
        client_kwargs = {"api_key": api_key}
        if api_base:
            client_kwargs["base_url"] = api_base
        
        self.client = Anthropic(**client_kwargs)
    
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        生成文本補全
        
        Args:
            prompt: 提示文本
            **kwargs: 其他參數，可覆蓋初始化時的參數
        
        Returns:
            標準化的 LLM 回應物件
        
        Raises:
            AnthropicError: 當 API 調用失敗時
        """
        # 將 prompt 轉換為 messages 格式
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, **kwargs)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        生成聊天補全
        
        Args:
            messages: 聊天訊息列表
            **kwargs: 其他參數，可覆蓋初始化時的參數
        
        Returns:
            標準化的 LLM 回應物件
        
        Raises:
            AnthropicError: 當 API 調用失敗時
        """
        # 合併參數
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        params.update(kwargs)
        
        # 轉換 messages 格式 (從 OpenAI 格式轉換為 Anthropic 格式)
        anthropic_messages = []
        system_message = None
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_message = content
            elif role == "user":
                anthropic_messages.append({"role": "user", "content": content})
            elif role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": content})
            # 忽略其他角色
        
        try:
            # 調用 Anthropic API
            response = self.client.messages.create(
                messages=anthropic_messages,
                system=system_message,
                **params
            )
            
            # 提取回應內容
            content = response.content[0].text
            
            # 構建使用情況
            usage = {}
            if hasattr(response, 'usage'):
                usage = {
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                }
            
            # 構建標準化回應
            return LLMResponse(
                content=content,
                raw_response=response,
                usage=usage,
                model=self.model,
                provider="anthropic",
                finish_reason=response.stop_reason if hasattr(response, 'stop_reason') else None
            )
        
        except anthropic.APIError as e:
            if "authentication" in str(e).lower():
                raise AuthenticationError(f"Anthropic 認證錯誤: {str(e)}")
            elif "rate limit" in str(e).lower():
                raise RateLimitError(f"Anthropic 速率限制錯誤: {str(e)}")
            elif "invalid request" in str(e).lower() or "bad request" in str(e).lower():
                raise InvalidRequestError(f"Anthropic 無效請求錯誤: {str(e)}")
            else:
                raise AnthropicError(f"Anthropic 錯誤: {str(e)}")
        except Exception as e:
            raise AnthropicError(f"Anthropic 錯誤: {str(e)}")
    
    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量
        
        Args:
            text: 文本或文本列表
            **kwargs: 其他參數
        
        Returns:
            嵌入向量或嵌入向量列表
        
        Raises:
            AnthropicError: 當 API 調用失敗時
        """
        # Anthropic 目前不提供官方的嵌入 API，拋出錯誤
        raise AnthropicError("Anthropic 目前不提供官方的嵌入 API")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊
        
        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text"]
        
        # Claude 3 系列支援圖像輸入
        if "claude-3" in self.model.lower():
            capabilities.append("image-input")
        
        return {
            'model': self.model,
            'provider': "anthropic",
            'capabilities': capabilities,
        }

# 註冊提供商
LLMFactory.register("anthropic", AnthropicProvider)
