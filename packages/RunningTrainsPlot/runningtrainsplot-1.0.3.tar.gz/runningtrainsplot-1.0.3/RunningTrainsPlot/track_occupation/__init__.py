"""
track_occupation - 列车股道占用可视化模块

提供列车股道占用的可视化功能
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import csv
from datetime import datetime, timedelta

__all__ = ['plot_track_occupation', 'load_track_data']

def load_track_data(file_path):
    """
    加载股道占用数据
    
    参数:
        file_path: 股道数据文件路径
        
    返回:
        data: 股道占用数据DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"加载数据失败: {str(e)}")
        raise

def plot_track_occupation(data, figsize=(12, 6), title='Platform Schedule', show=True, save_path=None, dpi=300, **kwargs):
    """
    绘制列车股道占用可视化图
    
    参数:
        data: 股道占用数据DataFrame，需要包含以下列:
            - train_id: 列车ID
            - platform_id 或 track: 站台/股道编号
            - receiving_time: 接车时间（秒）
            - arrival_time: 到达时间（秒）
            - departure_time: 出发时间（秒）
            - leaving_time: 离站时间（秒）
            - arrival_delay (可选): 到达延误
            - departure_delay (可选): 出发延误
        figsize: 图表尺寸，默认(12, 6)
        title: 图表标题，默认为'Platform Schedule'
        show: 是否显示图表，默认True
        save_path: 保存图表的路径，默认为None
        dpi: 图像分辨率，默认300
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    # 检查必要的列是否存在
    platform_col = None
    if 'platform_id' in data.columns:
        platform_col = 'platform_id'
    elif 'track' in data.columns:
        platform_col = 'track'
    else:
        raise ValueError("数据必须包含'platform_id'或'track'列")
    
    required_cols = ['train_id', platform_col, 'arrival_time', 'departure_time']
    
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(f"数据必须包含'{col}'列")
    
    # 确保接车和离站时间存在，如果不存在则设置默认值
    if 'receiving_time' not in data.columns:
        data['receiving_time'] = data['arrival_time']
    
    if 'leaving_time' not in data.columns:
        data['leaving_time'] = data['departure_time']
    
    # 确保延误列存在，如果不存在则设置为0
    if 'arrival_delay' not in data.columns:
        data['arrival_delay'] = 0
    
    if 'departure_delay' not in data.columns:
        data['departure_delay'] = 0
    
    # 创建画布
    fig, ax = plt.subplots(figsize=figsize)
    
    # 计算最大站台编号和离站时间
    max_platform_id = max(data[platform_col])
    max_leaving_time = max(data['leaving_time'])
    
    # 设置Y轴范围
    plt.ylim(0, max_platform_id + 1)
    
    # 设置Y轴刻度（站台）
    plt.yticks(np.arange(0, max_platform_id + 1, 1))
    
    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7, which='both', axis='both')
    
    # 设置X轴范围
    plt.xlim(0, max_leaving_time + 50)
    
    # 矩形高度
    height = 0.6
    
    # 绘制每个列车的占用时间段
    for _, row in data.iterrows():
        train_id = row['train_id']
        platform = row[platform_col]
        
        receiving_time = row['receiving_time']
        arrival_time = row['arrival_time']
        departure_time = row['departure_time']
        leaving_time = row['leaving_time']
        
        arrival_delay = row['arrival_delay']
        departure_delay = row['departure_delay']
        
        # 确定颜色
        if arrival_delay > 0 or departure_delay > 0:
            color = 'blue'
            edgecolor = 'black'
        else:
            color = 'green'
            edgecolor = 'black'
            
        # 绘制主矩形（到达-出发时间段）
        rect = Rectangle(
            (arrival_time, platform), 
            departure_time - arrival_time, 
            height, 
            color=edgecolor, 
            fill=False, 
            alpha=0.8,
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # 添加列车ID标签
        text_x = arrival_time + (departure_time - arrival_time) / 2
        text_y = platform + height / 2
        plt.text(text_x, text_y, str(train_id), color=color, ha='center', va='center', fontsize=9)
        
        # 添加接车三角形
        arrival_triangle = Polygon(
            [(receiving_time, platform), 
             (arrival_time, platform), 
             (arrival_time, platform + height)],
            closed=True, 
            edgecolor=color, 
            facecolor=color, 
            alpha=0.8
        )
        ax.add_patch(arrival_triangle)
        
        # 添加离站三角形
        departure_triangle = Polygon(
            [(departure_time, platform), 
             (departure_time, platform + height), 
             (leaving_time, platform)],
            closed=True, 
            edgecolor=color, 
            facecolor=color, 
            alpha=0.8
        )
        ax.add_patch(departure_triangle)
        
        # 显示延误信息
        if arrival_delay > 0:
            delay_label_x = arrival_time - 2
            delay_label_y = platform
            plt.text(
                delay_label_x, 
                delay_label_y, 
                f'+{round(arrival_delay/60, 2)}', 
                color='orange', 
                ha='right', 
                va='center', 
                fontsize=8
            )
            
        if departure_delay > 0:
            delay_label_x = departure_time + 2
            delay_label_y = platform + height
            plt.text(
                delay_label_x, 
                delay_label_y, 
                f'+{round(departure_delay/60, 2)}', 
                color='red', 
                ha='right', 
                va='center', 
                fontsize=8
            )
    
    # 设置轴标签和标题
    plt.xlabel('Time (sec)')
    plt.ylabel('Platform ID')
    plt.title(title)
    
    # 移除顶部和右侧的坐标轴线
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # 保存图表
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    # 显示图表
    if show:
        plt.show()
        
    return fig, ax 