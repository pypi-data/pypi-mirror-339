"""
LLM Switch 回應模組

定義了標準化的 LLM 回應物件。
"""

from typing import Dict, Any, Optional

class LLMResponse:
    """標準化的 LLM 回應物件"""

    def __init__(
        self,
        content: str,
        raw_response: Any = None,
        usage: Optional[Dict[str, int]] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
        finish_reason: Optional[str] = None
    ):
        """
        初始化 LLM 回應物件

        Args:
            content: 回應內容
            raw_response: 原始回應物件
            usage: 使用情況，如 token 數
            model: 使用的模型
            provider: 使用的提供商
            finish_reason: 完成原因
        """
        self.content = content
        self.raw_response = raw_response
        self.usage = usage or {}
        self.model = model
        self.provider = provider
        self.finish_reason = finish_reason

    def __str__(self) -> str:
        """字串表示"""
        return self.content

    def __repr__(self) -> str:
        """詳細表示"""
        return f"LLMResponse(content='{self.content[:50]}...', model='{self.model}', provider='{self.provider}')"

    @property
    def input_tokens(self) -> int:
        """輸入 token 數"""
        return self.usage.get('input_tokens', 0)

    @property
    def output_tokens(self) -> int:
        """輸出 token 數"""
        return self.usage.get('output_tokens', 0)

    @property
    def total_tokens(self) -> int:
        """總 token 數"""
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            'content': self.content,
            'usage': self.usage,
            'model': self.model,
            'provider': self.provider,
            'finish_reason': self.finish_reason
        }
