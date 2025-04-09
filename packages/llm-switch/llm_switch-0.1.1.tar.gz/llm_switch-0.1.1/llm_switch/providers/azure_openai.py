"""
Azure OpenAI 提供商實現
"""

from typing import Dict, List, Optional, Union, Any

try:
    import openai
    from openai import AzureOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..core.base import LLMProvider
from ..core.response import LLMResponse
from ..core.factory import LLMFactory
from ..exceptions import AzureOpenAIError, AuthenticationError, RateLimitError, InvalidRequestError

class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI 提供商實現"""

    def __init__(
        self,
        api_key: str,
        model: str,
        api_base: str,
        api_version: str = "2023-05-15",
        deployment_name: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ):
        """
        初始化 Azure OpenAI 提供商

        Args:
            api_key: Azure OpenAI API 金鑰
            model: 模型名稱 (在 Azure 中通常是部署名稱)
            api_base: API 基礎 URL (例如: https://{your-resource-name}.openai.azure.com)
            api_version: API 版本
            deployment_name: 部署名稱 (如果與 model 不同)
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
        self.api_version = api_version
        self.deployment_name = deployment_name or model

        # 初始化 Azure OpenAI 客戶端
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_base
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
            AzureOpenAIError: 當 API 調用失敗時
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
            AzureOpenAIError: 當 API 調用失敗時
        """
        # 合併參數
        params = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        params.update(kwargs)

        # 獲取部署名稱
        deployment_name = kwargs.pop("deployment_name", self.deployment_name)

        try:
            # 調用 Azure OpenAI API
            response = self.client.chat.completions.create(
                model=deployment_name,  # Azure 使用部署名稱而不是模型名稱
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
                provider="azure_openai",
                finish_reason=response.choices[0].finish_reason
            )

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"Azure OpenAI 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"Azure OpenAI 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"Azure OpenAI 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise AzureOpenAIError(f"Azure OpenAI 錯誤: {str(e)}")

    def embed(self, text: Union[str, List[str]], **kwargs) -> Union[List[float], List[List[float]]]:
        """
        生成嵌入向量

        Args:
            text: 文本或文本列表
            **kwargs: 其他參數

        Returns:
            嵌入向量或嵌入向量列表

        Raises:
            AzureOpenAIError: 當 API 調用失敗時
        """
        # 確保 text 是列表
        if isinstance(text, str):
            text_list = [text]
            single_input = True
        else:
            text_list = text
            single_input = False

        # 獲取嵌入部署名稱
        embedding_deployment = kwargs.pop("embedding_deployment", kwargs.get("embedding_model", None))
        if embedding_deployment is None:
            # 如果未指定嵌入部署名稱，使用預設部署名稱
            embedding_deployment = self.deployment_name

        try:
            # 調用 Azure OpenAI API
            response = self.client.embeddings.create(
                model=embedding_deployment,
                input=text_list,
                **kwargs
            )

            # 提取嵌入向量
            embeddings = [item.embedding for item in response.data]

            # 如果是單個輸入，返回單個嵌入向量
            if single_input:
                return embeddings[0]

            return embeddings

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"Azure OpenAI 認證錯誤: {str(e)}")
        except openai.RateLimitError as e:
            raise RateLimitError(f"Azure OpenAI 速率限制錯誤: {str(e)}")
        except openai.BadRequestError as e:
            raise InvalidRequestError(f"Azure OpenAI 無效請求錯誤: {str(e)}")
        except Exception as e:
            raise AzureOpenAIError(f"Azure OpenAI 錯誤: {str(e)}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        獲取模型資訊

        Returns:
            模型資訊字典
        """
        # 根據模型名稱判斷能力
        capabilities = ["text"]

        # 根據模型名稱判斷能力 (與 OpenAI 類似)
        if "gpt-4-vision" in self.model:
            capabilities.append("image-input")

        if "gpt-4" in self.model and "turbo" in self.model:
            capabilities.append("json-mode")

        if "gpt-3.5-turbo" in self.model:
            capabilities.append("json-mode")

        return {
            'model': self.model,
            'provider': "azure_openai",
            'capabilities': capabilities,
            'deployment_name': self.deployment_name
        }

# 註冊提供商
LLMFactory.register("azure_openai", AzureOpenAIProvider)
