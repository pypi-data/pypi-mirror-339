"""
DeepSeek 提供商實現
"""

from typing import Dict, List, Optional, Union, Any

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import DeepSeekError, AuthenticationError, RateLimitError, InvalidRequestError

class DeepSeekProvider(LLMProvider):
    """DeepSeek 提供商實現"""

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        api_base: str = "https://api.deepseek.com/v1",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 DeepSeek 提供商

        Args:
            api_key: DeepSeek API 金鑰
            model: 模型名稱
            api_base: API 基礎 URL
            temperature: 溫度參數
            max_tokens: 最大生成 token 數
            **kwargs: 其他參數

        Raises:
            ImportError: 當 openai 套件未安裝時
        """
        super().__init__(api_key=api_key, model=model, **kwargs)

        if not OPENAI_AVAILABLE:
            raise ImportError("請安裝 openai 套件: pip install openai")

        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_base = api_base

        # 初始化 OpenAI 客戶端 (DeepSeek 使用 OpenAI 兼容的 API)
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )

    def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        生成文本補全

        Args:
            prompt: 提示文本
            **kwargs: 其他參數，可覆蓋初始化時的參數

        Returns:
            標準化的 LLM 回應物件

        Raises:
            DeepSeekError: 當 API 調用失敗時
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
            DeepSeekError: 當 API 調用失敗時
        """
        # 合併參數
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        params.update(kwargs)

        try:
            # 調用 DeepSeek API (使用 OpenAI 兼容的 API)
            response = self.client.chat.completions.create(
                messages=messages,
                **params
            )

            # 提取回應內容
            content = response.choices[0].message.content

            # 構建使用情況
            usage = {}
            if hasattr(response, 'usage'):
                usage = {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }

            # 構建標準化回應
            return LLMResponse(
                content=content,
                raw_response=response,
                usage=usage,
                model=self.model,
                provider="deepseek",
                finish_reason=response.choices[0].finish_reason
            )

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"DeepSeek 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"DeepSeek 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"DeepSeek 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise DeepSeekError(f"DeepSeek 錯誤: {str(e)}")

    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量

        Args:
            text: 文本或文本列表
            **kwargs: 其他參數

        Returns:
            嵌入向量或嵌入向量列表

        Raises:
            DeepSeekError: 當 API 調用失敗時
        """
        # 確保 text 是列表
        if isinstance(text, str):
            text_list = [text]
            single_input = True
        else:
            text_list = text
            single_input = False

        # 合併參數
        params = {
            "model": kwargs.get("embedding_model", "deepseek-embedding"),
        }
        params.update({k: v for k, v in kwargs.items() if k != "embedding_model"})

        try:
            # 調用 DeepSeek API (使用 OpenAI 兼容的 API)
            response = self.client.embeddings.create(
                input=text_list,
                **params
            )

            # 提取嵌入向量
            embeddings = [item.embedding for item in response.data]

            # 如果是單個輸入，返回單個嵌入向量
            if single_input:
                return embeddings[0]

            return embeddings

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"DeepSeek 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"DeepSeek 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"DeepSeek 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise DeepSeekError(f"DeepSeek 錯誤: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊

        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text"]

        if self.model == "deepseek-coder":
            capabilities.append("code")

        if self.model == "deepseek-math":
            capabilities.append("math")

        if self.model == "deepseek-vision":
            capabilities.append("image-input")

        return {
            'model': self.model,
            'provider': "deepseek",
            'capabilities': capabilities,
        }

# 註冊提供商
LLMFactory.register("deepseek", DeepSeekProvider)
