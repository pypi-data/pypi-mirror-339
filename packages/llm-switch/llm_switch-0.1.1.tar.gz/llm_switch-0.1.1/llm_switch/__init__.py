"""
LLM Switch - 一個用於切換不同 LLM 提供商的模組

這個模組允許程式設計師輕鬆地在不同的 LLM 提供商之間切換，
只需通過修改設定檔，無需更改程式碼。
"""

from .core.service import LLMService

__version__ = "0.1.1"  # 更新版本號，增加自動安裝相依套件
__all__ = ["LLMService"]
