"""
speed_curve - 列车速度曲线可视化模块

提供列车速度曲线的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 导出主要函数
__all__ = ['plot_speed_curve', 'load_speed_data']

def load_speed_data(file_path):
    """
    加载速度曲线数据
    
    参数:
        file_path: 速度数据CSV文件路径
        
    返回:
        data: 速度数据DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"加载数据失败: {str(e)}")
        raise

def plot_speed_curve(data, figsize=(10, 6), 
                   title='Train Speed Curves', 
                   x_label='Time / s', y_label='Speed (m/s)',
                   x_range=(0, 500), y_range=(0, 22),
                   test_col='Test_Speed', pred_col='Pred_Speed', time_col='Time',
                   test_label='test curve', pred_label='pred curve',
                   test_color='b', pred_color='r',
                   show=True, save_path=None, dpi=300, **kwargs):
    """
    绘制列车速度曲线图
    
    参数:
        data: 速度数据，可以是以下格式之一:
            1. 包含所需列的DataFrame
            2. CSV文件路径
        figsize: 图表尺寸，默认(10, 6)
        title: 图表标题，默认'Train Speed Curves'
        x_label: X轴标签，默认'Time / s'
        y_label: Y轴标签，默认'Speed (m/s)'
        x_range: X轴范围，默认(0, 500)
        y_range: Y轴范围，默认(0, 22)
        test_col: 测试速度列名，默认'Test_Speed'
        pred_col: 预测速度列名，默认'Pred_Speed'
        time_col: 时间列名，默认'Time'
        test_label: 测试曲线标签，默认'test curve'
        pred_label: 预测曲线标签，默认'pred curve'
        test_color: 测试曲线颜色，默认'b'
        pred_color: 预测曲线颜色，默认'r'
        show: 是否显示图表，默认True
        save_path: 保存图表的路径，默认为None
        dpi: 图像分辨率，默认300
        **kwargs: 附加参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    # 处理输入数据
    if isinstance(data, str):
        df = load_speed_data(data)
    else:
        df = data
    
    # 验证数据列
    required_cols = [time_col, test_col, pred_col]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"数据必须包含'{col}'列")
    
    # 创建画布和坐标轴
    fig, ax = plt.subplots(figsize=figsize)
    
    # 绘制两条曲线
    ax.plot(df[time_col], df[test_col],
            color=test_color, linewidth=2, label=test_label)
    ax.plot(df[time_col], df[pred_col],
            color=pred_color, linewidth=2, label=pred_label)
    
    # 设置图表元素
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    
    # 设置坐标轴范围
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    
    # 添加辅助元素
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    # 设置刻度标注
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    ax.set_yticks([0, 5, 10, 15, 20])
    
    # 移除顶部和右侧的坐标轴线
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    
    # 保存图表
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    # 显示图表
    if show:
        plt.show()
    
    return fig, ax

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