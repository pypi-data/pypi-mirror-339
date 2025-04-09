#!/usr/bin/env python
"""
Setup script for iiko-pkg
"""

import os
from setuptools import setup, find_packages

# Read the long description from README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="iiko-pkg",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "isort>=5.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
            "tox>=3.20.0",
        ],
    },
    author="Muhammad Ali",
    author_email="example@example.com",
    description="Python library for iiko.services API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "iiko", "iikobiz", "iikocard", "iikodelivery",
        "iiko-api", "iikocloudapi", "iiko-integration",
        "iiko-python", "python-iiko", "iiko-example",
        "restaurant-management", "pos-system", "food-delivery",
        "delivery-management", "telegram-bot", "python3",
        "uzbekistan", "tashkent", "restaurant-pos", "cafe-automation",
        "restoran-avtomatizatsiya", "dostavka"
    ],
    url="https://github.com/yourusername/iiko-pkg",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
)
