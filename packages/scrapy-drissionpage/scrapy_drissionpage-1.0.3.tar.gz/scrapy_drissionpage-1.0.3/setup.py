import os
from setuptools import setup, find_packages

# 直接指定依赖，而不是从文件读取
INSTALL_REQUIRES = [
    "scrapy>=2.12.0",
    "DrissionPage>=4.1.0.18",
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="scrapy-drissionpage",
    version="1.0.3",
    author="KingKing888",
    author_email="184108270@qq.com",
    description="将Scrapy爬虫框架与DrissionPage网页自动化工具进行无缝集成",
    long_description=long_description,
    url="https://github.com/kingking888/scrapy-drissionpage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.9",
    install_requires=INSTALL_REQUIRES,
    keywords="scrapy, drissionpage, crawler, spider, web scraping, automation, commercial-use, personal-use",
) 