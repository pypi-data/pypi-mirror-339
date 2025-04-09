"""
LLM Switch 提供商模組

包含所有 LLM 提供商的實現。
"""

# 自動導入所有提供商
import os
import importlib
from pathlib import Path

# 獲取當前目錄中的所有 Python 文件
current_dir = Path(__file__).parent
for file_path in current_dir.glob("*.py"):
    if file_path.name != "__init__.py":
        module_name = file_path.stem
        try:
            importlib.import_module(f"llm_switch.providers.{module_name}")
        except ImportError:
            pass
