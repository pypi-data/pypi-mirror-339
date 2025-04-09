"""
Google (Gemini) 提供商實現
"""

import json
from typing import Dict, List, Optional, Union, Any

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import GoogleError, AuthenticationError, RateLimitError, InvalidRequestError

class GoogleProvider(LLMProvider):
    """Google (Gemini) 提供商實現"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-pro",
        api_base: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 Google (Gemini) 提供商
        
        Args:
            api_key: Google API 金鑰
            model: 模型名稱
            api_base: API 基礎 URL (Google API 通常不需要)
            temperature: 溫度參數
            max_tokens: 最大生成 token 數
            **kwargs: 其他參數
        
        Raises:
            ImportError: 當 google-generativeai 套件未安裝時
        """
        super().__init__(api_key=api_key, model=model, **kwargs)
        
        if not GOOGLE_AVAILABLE:
            raise ImportError("請安裝 google-generativeai 套件: pip install google-generativeai")
        
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # 初始化 Google Generative AI
        genai.configure(api_key=api_key)
        
        # 創建模型
        self.genai = genai
        self.generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "top_p": kwargs.get("top_p", 0.95),
            "top_k": kwargs.get("top_k", 0),
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
            GoogleError: 當 API 調用失敗時
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
            GoogleError: 當 API 調用失敗時
        """
        # 合併參數
        generation_config = self.generation_config.copy()
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs.pop("temperature")
        if "max_tokens" in kwargs:
            generation_config["max_output_tokens"] = kwargs.pop("max_tokens")
        if "top_p" in kwargs:
            generation_config["top_p"] = kwargs.pop("top_p")
        if "top_k" in kwargs:
            generation_config["top_k"] = kwargs.pop("top_k")
        
        # 獲取模型
        model_name = kwargs.pop("model", self.model)
        
        # 轉換 messages 格式 (從 OpenAI 格式轉換為 Google 格式)
        google_messages = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "user":
                google_messages.append({"role": "user", "parts": [{"text": content}]})
            elif role == "assistant":
                google_messages.append({"role": "model", "parts": [{"text": content}]})
            elif role == "system":
                # 系統訊息作為第一條用戶訊息
                if not google_messages:
                    google_messages.append({"role": "user", "parts": [{"text": f"System: {content}"}]})
                # 如果已經有訊息，則添加為用戶訊息
                else:
                    google_messages.append({"role": "user", "parts": [{"text": f"System: {content}"}]})
        
        try:
            # 獲取模型
            model = self.genai.GenerativeModel(model_name=model_name, generation_config=generation_config)
            
            # 調用 Google API
            response = model.generate_content(google_messages)
            
            # 提取回應內容
            content = response.text
            
            # 構建使用情況 (Google API 可能不提供詳細的使用情況)
            usage = {
                'input_tokens': 0,  # Google API 可能不提供
                'output_tokens': 0,  # Google API 可能不提供
                'total_tokens': 0    # Google API 可能不提供
            }
            
            # 如果有使用情況資訊，更新 usage
            if hasattr(response, 'usage_metadata'):
                if hasattr(response.usage_metadata, 'prompt_token_count'):
                    usage['input_tokens'] = response.usage_metadata.prompt_token_count
                if hasattr(response.usage_metadata, 'candidates_token_count'):
                    usage['output_tokens'] = response.usage_metadata.candidates_token_count
                usage['total_tokens'] = usage['input_tokens'] + usage['output_tokens']
            
            # 構建標準化回應
            return LLMResponse(
                content=content,
                raw_response=response,
                usage=usage,
                model=model_name,
                provider="google",
                finish_reason="stop"  # Google API 可能不提供詳細的完成原因
            )
        
        except Exception as e:
            error_message = str(e).lower()
            if "authentication" in error_message or "api key" in error_message:
                raise AuthenticationError(f"Google 認證錯誤: {str(e)}")
            elif "rate limit" in error_message or "quota" in error_message:
                raise RateLimitError(f"Google 速率限制錯誤: {str(e)}")
            elif "invalid" in error_message or "bad request" in error_message:
                raise InvalidRequestError(f"Google 無效請求錯誤: {str(e)}")
            else:
                raise GoogleError(f"Google 錯誤: {str(e)}")
    
    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量
        
        Args:
            text: 文本或文本列表
            **kwargs: 其他參數
        
        Returns:
            嵌入向量或嵌入向量列表
        
        Raises:
            GoogleError: 當 API 調用失敗時
        """
        # 確保 text 是列表
        if isinstance(text, str):
            text_list = [text]
            single_input = True
        else:
            text_list = text
            single_input = False
        
        # 獲取嵌入模型
        embedding_model = kwargs.get("embedding_model", "embedding-001")
        
        try:
            # 調用 Google API
            embeddings = []
            for t in text_list:
                result = self.genai.embed_content(
                    model=embedding_model,
                    content=t,
                    task_type="retrieval_document"
                )
                embeddings.append(result["embedding"])
            
            # 如果是單個輸入，返回單個嵌入向量
            if single_input:
                return embeddings[0]
            
            return embeddings
        
        except Exception as e:
            error_message = str(e).lower()
            if "authentication" in error_message or "api key" in error_message:
                raise AuthenticationError(f"Google 認證錯誤: {str(e)}")
            elif "rate limit" in error_message or "quota" in error_message:
                raise RateLimitError(f"Google 速率限制錯誤: {str(e)}")
            elif "invalid" in error_message or "bad request" in error_message:
                raise InvalidRequestError(f"Google 無效請求錯誤: {str(e)}")
            else:
                raise GoogleError(f"Google 錯誤: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊
        
        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text"]
        
        # Gemini 1.5 支援多模態輸入
        if "gemini-1.5" in self.model:
            capabilities.extend(["image-input", "video-input", "audio-input"])
        # Gemini 1.0 Pro Vision 支援圖像輸入
        elif "gemini-1.0-pro-vision" in self.model:
            capabilities.append("image-input")
        # Gemini 1.0 Pro 支援文本
        elif "gemini-1.0-pro" in self.model:
            pass  # 已經有 text 能力
        
        return {
            'model': self.model,
            'provider': "google",
            'capabilities': capabilities,
        }

# 註冊提供商
LLMFactory.register("google", GoogleProvider)
