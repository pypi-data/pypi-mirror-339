# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="llm_switch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.5.0"],
        "google": ["google-generativeai>=0.3.0"],
        "flask": ["flask>=2.0.0"],
        "requests": ["requests>=2.0.0"],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "google-generativeai>=0.3.0",
            "flask>=2.0.0",
            "requests>=2.0.0",
            "python-dotenv>=0.19.0",
        ],
    },
    author="Your Name",  # 請替換為您的名字
    author_email="your.email@example.com",  # 請替換為您的電子郵件
    description="LLM Switch Module - 一個用於切換不同 LLM 提供商的模組",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm_switch",  # 請替換為您的 GitHub 儲存庫 URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
