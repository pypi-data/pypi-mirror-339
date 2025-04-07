import os
from setuptools import setup, find_packages

# 读取README.md文件内容作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 基本设置
setup(
    name="RunningTrainsPlot",
    version="1.0.3",  # 版本号
    author="NJU Innovation Group",
    author_email="sc22zs2@leeds.ac.uk",
    description="铁路列车运行数据可视化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RunningTrainsPlot",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.1.0",
        "plotly>=5.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="railway, train, visualization, plot, diagram, flow",
)
