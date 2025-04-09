#!/usr/bin/env python3
"""
Llama Voice - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="llama-voice",
    version="0.1.0",
    description="Voice processing for LlamaSearch AI",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Nik Jois",
    author_email="nikjois@llamasearch.ai",
    url="https://github.com/llamasearchai/llama-voice",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
        "torch>=2.0.0",
        "transformers>=4.28.0"
    ],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
)
