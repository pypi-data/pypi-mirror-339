"""
speed_curve - 速度曲线可视化模块

提供列车速度与时间/距离曲线的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['plot_speed_curve', 'load_speed_data', 'plot_speed_comparison']

def load_speed_data(file_path):
    """
    加载速度曲线数据
    
    参数:
        file_path: 速度数据文件路径
        
    返回:
        data: 速度数据DataFrame
    """
    data = pd.read_csv(file_path)
    return data

def plot_speed_comparison(data, time_col='Time', speed_cols=None, curve_labels=None, 
                         figsize=(10, 6), title='列车速度曲线', save_path=None, 
                         xlabel='Time / s', ylabel='Speed (m/s)', **kwargs):
    """
    绘制速度对比曲线（与原始代码风格一致）
    
    参数:
        data: 包含时间和多条速度曲线数据的DataFrame
        time_col: 时间列名
        speed_cols: 速度列名列表，如['Test_Speed', 'Pred_Speed']
        curve_labels: 曲线标签列表
        figsize: 图表尺寸，默认(10, 6)
        title: 图表标题
        save_path: 保存图表的路径，默认为None
        xlabel: x轴标签
        ylabel: y轴标签
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 默认速度列
    if speed_cols is None:
        if 'Test_Speed' in data.columns and 'Pred_Speed' in data.columns:
            speed_cols = ['Test_Speed', 'Pred_Speed']
        else:
            # 尝试找到所有可能的速度列
            speed_cols = [col for col in data.columns if 'speed' in col.lower() or 'velocity' in col.lower()]
            if not speed_cols:
                speed_cols = [col for col in data.columns if col != time_col]
    
    # 默认标签
    if curve_labels is None:
        curve_labels = speed_cols
    
    # 设置颜色
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    
    # 绘制每条速度曲线
    for i, speed_col in enumerate(speed_cols):
        color = colors[i % len(colors)]
        label = curve_labels[i] if i < len(curve_labels) else speed_col
        ax.plot(data[time_col], data[speed_col], color=color, linewidth=2, label=label)
    
    # 设置图表元素
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    
    # 添加辅助元素
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # 根据数据设置适当的坐标轴范围
    if len(data) > 0:
        x_min = data[time_col].min()
        x_max = data[time_col].max()
        ax.set_xlim(x_min, x_max)
        
        # 找到所有速度列的最大值
        y_max = max(data[col].max() for col in speed_cols if col in data.columns)
        ax.set_ylim(0, y_max * 1.1)  # 增加10%的余量
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig, ax

def plot_speed_curve(data, x_col='time', y_col='speed', train_id=None, 
                    figsize=(12, 6), title='列车速度曲线', save_path=None, **kwargs):
    """
    绘制列车速度曲线
    
    参数:
        data: 包含速度和时间/距离数据的DataFrame
        x_col: x轴列名，可以是'time'或'distance'
        y_col: y轴列名，默认为'speed'
        train_id: 列车编号，如果指定则只绘制该列车的曲线
        figsize: 图表尺寸，默认(12, 6)
        title: 图表标题
        save_path: 保存图表的路径，默认为None
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 过滤数据
    if train_id is not None:
        if 'train_id' in data.columns:
            plot_data = data[data['train_id'] == train_id]
        else:
            plot_data = data
    else:
        plot_data = data
    
    # 绘制速度曲线
    ax.plot(plot_data[x_col], plot_data[y_col], **kwargs)
    
    # 设置轴标签
    if x_col == 'distance' or 'distance' in x_col.lower():
        x_label = '距离 (km)'
        y_label = '速度 (km/h)'
    else:
        x_label = '时间 (s)'
        y_label = '速度 (m/s)'
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    
    # 设置标题
    ax.set_title(title)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 标记关键点
    max_speed_idx = plot_data[y_col].idxmax()
    if max_speed_idx is not None:
        max_speed = plot_data.loc[max_speed_idx, y_col]
        max_speed_pos = plot_data.loc[max_speed_idx, x_col]
        ax.scatter(max_speed_pos, max_speed, color='red', s=80, zorder=5)
        ax.text(max_speed_pos, max_speed*1.05, f'最高速度: {max_speed:.1f}', 
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig, ax

def plot_speed_distance_time(data, figsize=(15, 10), save_path=None):
    """
    同时绘制速度-距离和速度-时间曲线
    
    参数:
        data: 包含速度、距离和时间数据的DataFrame
        figsize: 图表尺寸，默认(15, 10)
        save_path: 保存图表的路径，默认为None
        
    返回:
        fig: matplotlib图表对象
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    # 绘制速度-时间曲线
    ax1.plot(data['time'], data['speed'], 'b-', linewidth=2)
    ax1.set_xlabel('时间 (s)')
    ax1.set_ylabel('速度 (m/s)')
    ax1.set_title('速度-时间曲线')
    ax1.grid(True)
    
    # 绘制速度-距离曲线
    ax2.plot(data['distance'], data['speed'], 'g-', linewidth=2)
    ax2.set_xlabel('距离 (km)')
    ax2.set_ylabel('速度 (km/h)')
    ax2.set_title('速度-距离曲线')
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig 