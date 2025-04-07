"""
cyclic_diagram - 循环图表可视化模块

提供循环图表数据的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# 导出主要函数
__all__ = ['plot_cyclic_diagram']  # 在此添加模块的主要函数

def plot_cyclic_diagram(data, figsize=(12, 8), title="循环运行图", **kwargs):
    """
    绘制循环运行图的主函数
    
    参数:
        data: DataFrame, 包含以下字段:
            train_id: 列车ID
            station: 站点名称
            arrival_time: 到达时间
            departure_time: 出发时间
        figsize: 图表尺寸
        title: 图表标题
        **kwargs: 附加参数
    
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 获取所有唯一的列车ID和站点
    train_ids = data['train_id'].unique()
    stations = data['station'].unique()
    
    # 为每个站点分配一个位置
    station_positions = {station: i for i, station in enumerate(stations)}
    
    # 为每个列车ID分配一个颜色
    colors = plt.cm.tab10.colors
    train_colors = {train_id: colors[i % len(colors)] for i, train_id in enumerate(train_ids)}
    
    # 绘制列车运行线
    for train_id in train_ids:
        train_data = data[data['train_id'] == train_id].sort_values('arrival_time')
        
        x_points = []
        y_points = []
        
        for _, row in train_data.iterrows():
            station = row['station']
            y_pos = station_positions[station]
            
            # 添加到达和出发时间点
            arrival_time = row['arrival_time']
            departure_time = row['departure_time']
            
            if isinstance(arrival_time, str):
                arrival_time = datetime.fromisoformat(arrival_time)
            if isinstance(departure_time, str):
                departure_time = datetime.fromisoformat(departure_time)
                
            # 转换为小时格式（浮点数）
            base_time = arrival_time.replace(hour=0, minute=0, second=0, microsecond=0)
            arrival_hour = (arrival_time - base_time).total_seconds() / 3600
            departure_hour = (departure_time - base_time).total_seconds() / 3600
            
            # 添加点
            x_points.extend([arrival_hour, departure_hour])
            y_points.extend([y_pos, y_pos])
            
            # 绘制站停线段（水平线）
            ax.plot([arrival_hour, departure_hour], [y_pos, y_pos], '-', color=train_colors[train_id], lw=2)
        
        # 连接站点之间的线段（对角线）
        for i in range(0, len(x_points)-2, 2):
            ax.plot([x_points[i+1], x_points[i+2]], [y_points[i+1], y_points[i+2]], '-', color=train_colors[train_id], lw=2)
    
    # 设置Y轴为站点名称
    ax.set_yticks(list(station_positions.values()))
    ax.set_yticklabels(list(station_positions.keys()))
    
    # 设置X轴为时间
    ax.set_xlabel('时间 (小时)')
    ax.set_ylabel('站点')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加图例
    handles = [plt.Line2D([0], [0], color=color, lw=2, label=train_id) 
               for train_id, color in train_colors.items()]
    ax.legend(handles=handles, loc='best')
    
    plt.tight_layout()
    return fig, ax 