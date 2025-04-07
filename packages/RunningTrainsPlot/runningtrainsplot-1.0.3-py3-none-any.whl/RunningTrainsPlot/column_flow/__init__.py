"""
column_flow - 列流图可视化模块

提供列流图可视化功能，显示各个车站间的流量关系
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# 导出主要函数
__all__ = ['plot_column_flow', 'load_column_flow_data']

def load_column_flow_data(station_file, flow_file):
    """
    加载列流图数据
    
    参数:
        station_file: 站点数据CSV文件路径，包含station列
        flow_file: 流量数据CSV文件路径，包含label, start, end, layer列
        
    返回:
        stations: 站点列表
        flows: 流量数据列表
    """
    try:
        # 读取站点信息
        stations_df = pd.read_csv(station_file, header=0)
        stations = stations_df['station'].tolist()
        
        # 读取列流信息
        flows_df = pd.read_csv(flow_file, header=0)
        flows = flows_df.to_dict('records')
        
        return stations, flows
    
    except FileNotFoundError as e:
        print(f"文件未找到: {e.filename}")
        raise
    except KeyError as e:
        print(f"CSV文件格式错误，缺少必要列: {e}")
        print("stations.csv必须包含'station'列")
        print("flows.csv必须包含label, start, end, layer四列")
        raise

def plot_column_flow(stations, flows, figsize=(12, 4.5), 
                   save_path=None, show=True, dpi=300,
                   station_spacing=2.0, node_size=800, base_y=0.5, 
                   flow_gap=0.3, flow_y_base=-0.3, label_offset=0.15,
                   **kwargs):
    """
    绘制列流图
    
    参数:
        stations: 站点列表
        flows: 流量数据列表，每个元素需要包含label, start, end, layer属性
        figsize: 图表尺寸，默认(12, 4.5)
        save_path: 保存图表的路径，默认为None
        show: 是否显示图表，默认True
        dpi: 图像分辨率，默认300
        station_spacing: 站点间距，默认2.0
        node_size: 节点大小，默认800
        base_y: 基准线高度，默认0.5
        flow_gap: 流线垂直间距，默认0.3
        flow_y_base: 流线基准高度偏移，默认-0.3
        label_offset: 标签偏移量，默认0.15
        **kwargs: 附加参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    # 初始化画布
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()  # 关闭坐标轴
    
    # 计算布局参数
    start_x = -station_spacing / 2
    end_x = (len(stations) - 1) * station_spacing + station_spacing / 2
    
    # 绘制基准线
    ax.plot([start_x, end_x], [base_y, base_y],
            color='black', linewidth=2, zorder=1)
    
    # 绘制编组站节点
    station_x = [i * station_spacing for i in range(len(stations))]
    ax.scatter(station_x, [base_y] * len(stations), s=node_size,
               color='black', zorder=2, edgecolor='none')
    
    # 添加车站标签
    for x, name in zip(station_x, stations):
        ax.text(x, base_y + label_offset, name,
                ha='center', va='bottom',
                fontsize=14, weight='bold')
    
    # 绘制列流系统
    for flow in flows:
        x_start = flow['start'] * station_spacing
        x_end = flow['end'] * station_spacing
        y_pos = base_y + flow_y_base - flow['layer'] * flow_gap
        
        # 添加箭头
        ax.annotate('',
                    xy=(x_end, y_pos),
                    xytext=(x_start, y_pos),
                    arrowprops=dict(
                        arrowstyle='->',
                        color='#1F77B4',
                        lw=2,
                        shrinkA=0,
                        shrinkB=0
                    ),
                    zorder=3)
        
        # 添加标签
        ax.text((x_start + x_end) / 2,
                y_pos - label_offset,
                flow['label'],
                ha='center',
                va='top',
                fontsize=12,
                bbox=dict(
                    boxstyle='round,pad=0.3',
                    facecolor='white',
                    edgecolor='#DDDDDD',
                    alpha=0.9
                ))
    
    # 设置显示范围
    ax.set_xlim(start_x - 0.5, end_x + 0.5)
    ax.set_ylim(base_y - 1.3, base_y + 0.3)
    
    # 保存图表
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    # 显示图表
    if show:
        plt.show()
    
    return fig, ax 