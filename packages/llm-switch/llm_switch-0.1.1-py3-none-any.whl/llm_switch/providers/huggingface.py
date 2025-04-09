"""
HuggingFace 提供商實現
"""

import json
import requests
from typing import Dict, List, Optional, Union, Any

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import HuggingFaceError, AuthenticationError, RateLimitError, InvalidRequestError

class HuggingFaceProvider(LLMProvider):
    """HuggingFace 提供商實現"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "mistralai/Mistral-7B-Instruct-v0.2",
        api_base: str = "https://api-inference.huggingface.co/models",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 HuggingFace 提供商
        
        Args:
            api_key: HuggingFace API 金鑰
            model: 模型名稱
            api_base: API 基礎 URL
            temperature: 溫度參數
            max_tokens: 最大生成 token 數
            **kwargs: 其他參數
        """
        super().__init__(api_key=api_key, model=model, **kwargs)
        
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_base = api_base
        
        # 設置 API URL
        self.api_url = f"{api_base}/{model}"
        
        # 設置 headers
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        生成文本補全
        
        Args:
            prompt: 提示文本
            **kwargs: 其他參數，可覆蓋初始化時的參數
        
        Returns:
            標準化的 LLM 回應物件
        
        Raises:
            HuggingFaceError: 當 API 調用失敗時
        """
        # 合併參數
        params = {
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "top_p": kwargs.get("top_p", 0.95),
            "top_k": kwargs.get("top_k", 50),
        }
        
        # 構建請求數據
        payload = {
            "inputs": prompt,
            "parameters": params
        }
        
        try:
            # 調用 HuggingFace API
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            # 檢查回應狀態
            if response.status_code == 200:
                # 解析回應
                result = response.json()
                
                # HuggingFace API 的回應格式可能因模型而異
                # 嘗試提取生成的文本
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], dict) and "generated_text" in result[0]:
                        content = result[0]["generated_text"]
                    else:
                        content = str(result[0])
                elif isinstance(result, dict) and "generated_text" in result:
                    content = result["generated_text"]
                else:
                    content = str(result)
                
                # 構建使用情況 (HuggingFace API 可能不提供詳細的使用情況)
                usage = {
                    'input_tokens': 0,  # HuggingFace API 可能不提供
                    'output_tokens': 0,  # HuggingFace API 可能不提供
                    'total_tokens': 0    # HuggingFace API 可能不提供
                }
                
                # 構建標準化回應
                return LLMResponse(
                    content=content,
                    raw_response=result,
                    usage=usage,
                    model=self.model,
                    provider="huggingface",
                    finish_reason="stop"  # HuggingFace API 可能不提供詳細的完成原因
                )
            
            elif response.status_code == 401:
                raise AuthenticationError(f"HuggingFace 認證錯誤: {response.text}")
            elif response.status_code == 429:
                raise RateLimitError(f"HuggingFace 速率限制錯誤: {response.text}")
            elif response.status_code == 400:
                raise InvalidRequestError(f"HuggingFace 無效請求錯誤: {response.text}")
            else:
                raise HuggingFaceError(f"HuggingFace 錯誤 ({response.status_code}): {response.text}")
        
        except requests.RequestException as e:
            raise HuggingFaceError(f"HuggingFace 請求錯誤: {str(e)}")
        except Exception as e:
            raise HuggingFaceError(f"HuggingFace 錯誤: {str(e)}")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        生成聊天補全
        
        Args:
            messages: 聊天訊息列表
            **kwargs: 其他參數，可覆蓋初始化時的參數
        
        Returns:
            標準化的 LLM 回應物件
        
        Raises:
            HuggingFaceError: 當 API 調用失敗時
        """
        # 將 messages 轉換為單一提示文本
        prompt = self._convert_messages_to_prompt(messages)
        
        # 調用 complete 方法
        return self.complete(prompt, **kwargs)
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        將聊天訊息列表轉換為單一提示文本
        
        Args:
            messages: 聊天訊息列表
        
        Returns:
            提示文本
        """
        prompt = ""
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                prompt += f"System: {content}\n\n"
            elif role == "user":
                prompt += f"User: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        prompt += "Assistant: "
        
        return prompt
    
    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量
        
        Args:
            text: 文本或文本列表
            **kwargs: 其他參數
        
        Returns:
            嵌入向量或嵌入向量列表
        
        Raises:
            HuggingFaceError: 當 API 調用失敗時
        """
        # 確保 text 是列表
        if isinstance(text, str):
            text_list = [text]
            single_input = True
        else:
            text_list = text
            single_input = False
        
        # 獲取嵌入模型
        embedding_model = kwargs.get("embedding_model", "sentence-transformers/all-MiniLM-L6-v2")
        
        # 設置嵌入 API URL
        embedding_url = f"{self.api_base}/{embedding_model}"
        
        try:
            # 調用 HuggingFace API
            embeddings = []
            
            for t in text_list:
                payload = {"inputs": t}
                response = requests.post(embedding_url, headers=self.headers, json=payload)
                
                # 檢查回應狀態
                if response.status_code == 200:
                    # 解析回應
                    result = response.json()
                    
                    # HuggingFace API 的回應格式可能因模型而異
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0], list):
                            # 如果是嵌入向量列表的列表，取第一個
                            embeddings.append(result[0])
                        else:
                            # 如果是單個嵌入向量列表
                            embeddings.append(result)
                    else:
                        raise HuggingFaceError(f"無法解析嵌入向量: {result}")
                
                elif response.status_code == 401:
                    raise AuthenticationError(f"HuggingFace 認證錯誤: {response.text}")
                elif response.status_code == 429:
                    raise RateLimitError(f"HuggingFace 速率限制錯誤: {response.text}")
                elif response.status_code == 400:
                    raise InvalidRequestError(f"HuggingFace 無效請求錯誤: {response.text}")
                else:
                    raise HuggingFaceError(f"HuggingFace 錯誤 ({response.status_code}): {response.text}")
            
            # 如果是單個輸入，返回單個嵌入向量
            if single_input:
                return embeddings[0]
            
            return embeddings
        
        except requests.RequestException as e:
            raise HuggingFaceError(f"HuggingFace 請求錯誤: {str(e)}")
        except Exception as e:
            raise HuggingFaceError(f"HuggingFace 錯誤: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊
        
        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text"]
        
        # 根據模型名稱判斷能力
        model_lower = self.model.lower()
        
        if "stable-diffusion" in model_lower:
            capabilities = ["image-generation"]
        
        if "sentence-transformers" in model_lower or "embedding" in model_lower:
            capabilities = ["embeddings"]
        
        if "llava" in model_lower or "vision" in model_lower:
            capabilities.append("image-input")
        
        return {
            'model': self.model,
            'provider': "huggingface",
            'capabilities': capabilities,
        }

# 註冊提供商
LLMFactory.register("huggingface", HuggingFaceProvider)
