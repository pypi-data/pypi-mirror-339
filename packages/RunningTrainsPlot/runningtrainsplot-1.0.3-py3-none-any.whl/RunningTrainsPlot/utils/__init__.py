"""
utils - 工具函数模块

提供共享的工具函数和数据处理功能
"""

import numpy as np
import pandas as pd

__all__ = ['load_data', 'preprocess_data']

def load_data(filename, format=None):
    """
    从文件加载数据
    
    参数:
        filename: 文件名
        format: 文件格式，如'csv', 'excel'等
        
    返回:
        加载的数据对象
    """
    if format == 'csv':
        return pd.read_csv(filename)
    elif format == 'excel':
        return pd.read_excel(filename)
    else:
        # 自动检测并加载数据
        if filename.endswith('.csv'):
            return pd.read_csv(filename)
        elif filename.endswith(('.xls', '.xlsx')):
            return pd.read_excel(filename)
        else:
            raise ValueError(f"Unsupported file format: {filename}")

def preprocess_data(data, **kwargs):
    """
    预处理数据
    
    参数:
        data: 输入数据
        **kwargs: 预处理参数
        
    返回:
        预处理后的数据
    """
    # 实现数据预处理步骤
    return data 