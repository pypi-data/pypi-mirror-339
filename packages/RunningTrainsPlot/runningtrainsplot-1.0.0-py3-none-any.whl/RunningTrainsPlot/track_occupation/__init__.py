"""
track_occupation - 列车股道占用可视化模块

提供列车股道占用的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

__all__ = ['plot_track_occupation', 'load_track_data']

def load_track_data(file_path):
    """
    加载股道占用数据
    
    参数:
        file_path: 股道数据文件路径
        
    返回:
        data: 股道占用数据DataFrame
    """
    data = pd.read_csv(file_path)
    
    # 处理日期时间列
    if 'arrival_time' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['arrival_time']):
        data['arrival_time'] = pd.to_datetime(data['arrival_time'])
    
    if 'departure_time' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['departure_time']):
        data['departure_time'] = pd.to_datetime(data['departure_time'])
    
    return data

def plot_track_occupation(data, figsize=(15, 8), title='列车股道占用图', show_train_labels=True, 
                         color_map=None, save_path=None, **kwargs):
    """
    绘制列车股道占用可视化图
    
    参数:
        data: 股道占用数据DataFrame，需包含列：'train_id', 'track', 'arrival_time', 'departure_time'
        figsize: 图表尺寸，默认(15, 8)
        title: 图表标题，默认为'列车股道占用图'
        show_train_labels: 是否显示列车编号标签
        color_map: 列车类型对应的颜色映射字典，如{'G':'red', 'D':'blue'}
        save_path: 保存图表的路径，默认为None
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 获取所有股道
    track_col = 'track' if 'track' in data.columns else 'platform'
    tracks = sorted(data[track_col].unique())
    
    # 设置Y轴为股道
    ax.set_yticks(range(len(tracks)))
    ax.set_yticklabels(tracks)
    ax.set_ylim(-0.5, len(tracks) - 0.5)
    
    # 设置网格
    ax.grid(axis='y', linestyle='-', alpha=0.3)
    
    # 默认颜色映射
    if color_map is None:
        color_map = {'G': 'skyblue', 'D': 'lightgreen', 'K': 'lightcoral'}
    
    # 存储最早和最晚时间，用于设置X轴范围
    min_time = None
    max_time = None
    
    # 绘制每个列车的占用时间段
    for idx, row in data.iterrows():
        train_id = row['train_id']
        track = row[track_col]
        arrival = row['arrival_time']
        departure = row['departure_time']
        
        # 更新最早和最晚时间
        if min_time is None or arrival < min_time:
            min_time = arrival
        if max_time is None or departure > max_time:
            max_time = departure
        
        # 获取股道索引
        track_idx = tracks.index(track)
        
        # 确定颜色
        train_type = train_id[0] if isinstance(train_id, str) and len(train_id) > 0 else 'X'
        color = color_map.get(train_type, 'skyblue')
        
        # 创建矩形表示列车占用时间段
        rect = patches.Rectangle(
            (mdates.date2num(arrival), track_idx - 0.4),
            mdates.date2num(departure) - mdates.date2num(arrival),
            0.8,
            linewidth=1,
            edgecolor='black',
            facecolor=color,
            alpha=0.7
        )
        ax.add_patch(rect)
        
        # 添加列车号标签
        if show_train_labels:
            center_time = arrival + (departure - arrival) / 2
            ax.text(mdates.date2num(center_time), track_idx, 
                    train_id, ha='center', va='center', 
                    fontsize=9, color='black', fontweight='bold')
    
    # 设置X轴为时间
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # 添加标题和标签
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('时间', fontsize=12)
    ax.set_ylabel('股道', fontsize=12)
    
    # 自动设置X轴范围，确保能看到所有矩形
    if min_time is not None and max_time is not None:
        buffer = timedelta(minutes=30)  # 添加30分钟的缓冲区
        ax.set_xlim(
            mdates.date2num(min_time - buffer),
            mdates.date2num(max_time + buffer)
        )
    
    # 添加图例
    if color_map:
        handles = [patches.Patch(color=color, label=train_type) 
                 for train_type, color in color_map.items()]
        ax.legend(handles=handles, title='列车类型', loc='upper right')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig, ax 