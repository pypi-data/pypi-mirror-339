import os
from setuptools import setup, find_packages

# 读取README.md文件内容
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="RunningTrainsPlot",
    version="1.0.2",  # 更新版本号
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'plotly',
    ],
    author="NJU Innovation Group",
    author_email="example@example.com",
    description="铁路列车运行数据可视化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RunningTrainsPlot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
