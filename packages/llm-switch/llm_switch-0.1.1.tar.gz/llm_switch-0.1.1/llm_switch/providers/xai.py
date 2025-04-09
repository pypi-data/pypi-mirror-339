"""
XAI 提供商實現
"""

from typing import Dict, List, Union, Any

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import XAIError, AuthenticationError, RateLimitError, InvalidRequestError

class XAIProvider(LLMProvider):
    """XAI 提供商實現"""

    def __init__(
        self,
        api_key: str,
        model: str = "grok-2",  # 更新為實際的 XAI 模型名稱
        api_base: str = "https://api.xai.com/v1",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        explanation_level: str = "detailed",
        **kwargs
    ):
        """
        初始化 XAI 提供商

        Args:
            api_key: XAI API 金鑰
            model: 模型名稱
            api_base: API 基礎 URL
            temperature: 溫度參數
            max_tokens: 最大生成 token 數
            explanation_level: 解釋詳細程度 (detailed, basic, none)
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
        self.explanation_level = explanation_level

        # 初始化 OpenAI 客戶端 (假設 XAI 使用 OpenAI 兼容的 API)
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
            XAIError: 當 API 調用失敗時
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
            XAIError: 當 API 調用失敗時
        """
        # 合併參數
        params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        # 從 kwargs 中移除 explanation_level，但不添加到 params 中
        # 因為 XAI API 可能不支援這個參數
        explanation_level = kwargs.pop("explanation_level", self.explanation_level)

        params.update(kwargs)

        try:
            # 調用 XAI API (假設使用 OpenAI 兼容的 API)
            response = self.client.chat.completions.create(
                messages=messages,
                **params
            )

            # 檢查回應是否為 None
            if response is None:
                raise XAIError("API 回應為 None")

            # 檢查 choices 是否存在
            if not hasattr(response, 'choices') or response.choices is None or len(response.choices) == 0:
                raise XAIError(f"API 回應中無 choices: {response}")

            # 提取回應內容
            choice = response.choices[0]
            if not hasattr(choice, 'message') or choice.message is None:
                raise XAIError(f"API 回應中無 message: {choice}")

            if not hasattr(choice.message, 'content') or choice.message.content is None:
                raise XAIError(f"API 回應中無 content: {choice.message}")

            content = choice.message.content

            # 構建使用情況
            usage = {}
            if hasattr(response, 'usage'):
                usage = {
                    'input_tokens': getattr(response.usage, 'prompt_tokens', 0),
                    'output_tokens': getattr(response.usage, 'completion_tokens', 0),
                    'total_tokens': getattr(response.usage, 'total_tokens', 0)
                }

            # 提取解釋 (如果有)
            explanation = None
            if hasattr(response, 'explanation'):
                explanation = response.explanation

            # 如果有解釋，添加到回應中
            if explanation and explanation_level != "none":
                content = f"{content}\n\n解釋:\n{explanation}"

            # 構建標準化回應
            return LLMResponse(
                content=content,
                raw_response=response,
                usage=usage,
                model=self.model,
                provider="xai",
                finish_reason=response.choices[0].finish_reason if hasattr(response.choices[0], 'finish_reason') else None
            )

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"XAI 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"XAI 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"XAI 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise XAIError(f"XAI 錯誤: {str(e)}")

    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量

        Args:
            text: 文本或文本列表
            **kwargs: 其他參數

        Returns:
            嵌入向量或嵌入向量列表

        Raises:
            XAIError: 當 API 調用失敗時
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
            "model": kwargs.get("embedding_model", "xai-embedding"),
        }

        # 從 kwargs 中移除 explanation_level，但不添加到 params 中
        explanation_level = kwargs.pop("explanation_level", "basic")

        params.update({k: v for k, v in kwargs.items() if k != "embedding_model"})

        try:
            # 調用 XAI API (假設使用 OpenAI 兼容的 API)
            response = self.client.embeddings.create(
                input=text_list,
                **params
            )

            # 檢查回應是否為 None
            if response is None:
                raise XAIError("API 回應為 None")

            # 檢查 data 是否存在
            if not hasattr(response, 'data') or response.data is None or len(response.data) == 0:
                raise XAIError(f"API 回應中無 data: {response}")

            # 提取嵌入向量
            embeddings = []
            for item in response.data:
                if not hasattr(item, 'embedding') or item.embedding is None:
                    raise XAIError(f"API 回應中無 embedding: {item}")
                embeddings.append(item.embedding)

            # 如果是單個輸入，返回單個嵌入向量
            if single_input:
                return embeddings[0]

            return embeddings

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"XAI 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"XAI 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"XAI 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise XAIError(f"XAI 錯誤: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊

        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text", "explainable-ai"]

        if "vision" in self.model.lower():
            capabilities.append("image-input")

        if "code" in self.model.lower():
            capabilities.append("code")

        return {
            'model': self.model,
            'provider': "xai",
            'capabilities': capabilities,
            'explanation_level': self.explanation_level
        }

    def explain_response(self, response: LLMResponse) -> str:
        """
        提供回應的解釋

        Args:
            response: LLM 回應物件

        Returns:
            解釋文本
        """
        # 這個方法可以根據實際 XAI API 的實現進行調整
        if hasattr(response.raw_response, 'explanation'):
            return response.raw_response.explanation

        return "無法提供解釋。"

# 註冊提供商
LLMFactory.register("xai", XAIProvider)
