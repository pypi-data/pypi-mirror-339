"""
LLM Switch 異常處理模組

定義了 LLM Switch 模組中使用的所有異常類別。
"""

class LLMException(Exception):
    """LLM Switch 模組的基礎異常類別"""
    pass

class ConfigError(LLMException):
    """配置錯誤"""
    pass

class AuthenticationError(LLMException):
    """認證錯誤"""
    pass

class RateLimitError(LLMException):
    """速率限制錯誤"""
    pass

class InvalidRequestError(LLMException):
    """無效請求錯誤"""
    pass

class ProviderSpecificError(LLMException):
    """提供商特有錯誤的基礎類別"""
    pass

class OpenAIError(ProviderSpecificError):
    """OpenAI 特有錯誤"""
    pass

class AnthropicError(ProviderSpecificError):
    """Anthropic 特有錯誤"""
    pass

class GoogleError(ProviderSpecificError):
    """Google 特有錯誤"""
    pass

class DeepSeekError(ProviderSpecificError):
    """DeepSeek 特有錯誤"""
    pass

class XAIError(ProviderSpecificError):
    """XAI 特有錯誤"""
    pass

class AzureOpenAIError(ProviderSpecificError):
    """Azure OpenAI 特有錯誤"""
    pass

class HuggingFaceError(ProviderSpecificError):
    """HuggingFace 特有錯誤"""
    pass
