"""
passenger_flow - 客流OD图表可视化模块

提供客流OD数据的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib import rcParams

# 从原始Passenger-flow-OD-chart-RunningTrainsPlot导入所有公共函数
try:
    from Passenger_flow_OD_chart_RunningTrainsPlot import *
except ImportError:
    # 当原模块不可用时的后备处理
    pass

# 导出主要函数
__all__ = ['plot_passenger_flow', 'load_passenger_data']

def load_passenger_data(file_path):
    """
    加载客流OD数据
    
    参数:
        file_path: 客流数据文件路径
        
    返回:
        data: 客流数据DataFrame
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"加载数据失败: {str(e)}")
        raise

def plot_passenger_flow(data, origin_col='origin', destination_col='destination', 
                        value_col='value', figsize=(10, 8), title='OD 流量图',
                        use_chinese=True, horizontal=True, curve_type='s',
                        save_path=None, show=True, dpi=300, **kwargs):
    """
    绘制客流OD图表
    
    参数:
        data: 客流数据DataFrame，包含起始站、终到站和流量
        origin_col: 起始站列名，默认为'origin'
        destination_col: 终到站列名，默认为'destination'
        value_col: 流量列名，默认为'value'
        figsize: 图表尺寸，默认(10, 8)
        title: 图表标题，默认为'OD 流量图'
        use_chinese: 是否支持中文显示，默认为True
        horizontal: 是否使用水平布局，默认为True（原始代码的布局）
        curve_type: 曲线类型，可选's'或'arc'，默认为's'
        save_path: 保存图表的路径，默认为None
        show: 是否显示图表，默认True
        dpi: 图像分辨率，默认300
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    # 配置中文字体
    if use_chinese:
        rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
        rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
    
    # 创建画布
    fig, ax = plt.subplots(figsize=figsize)
    
    # 获取所有唯一的节点
    nodes = list(set(data[origin_col].tolist() + data[destination_col].tolist()))
    nodes.sort()
    
    # 为每个节点分配一个位置
    node_pos = {node: i for i, node in enumerate(nodes)}
    
    # 设置颜色
    colors = plt.cm.Paired(np.linspace(0, 1, len(nodes)))
    
    # 绘制S型曲线
    for _, row in data.iterrows():
        origin = row[origin_col]
        destination = row[destination_col]
        value = row[value_col]
        
        # 起点和终点的位置
        if horizontal:
            # 水平布局（原始代码方式）
            y_origin = node_pos[origin]
            y_destination = node_pos[destination]
            
            if curve_type == 's':
                # S型曲线的控制点
                path = Path(
                    [
                        (0, y_origin),  # 起点
                        (0.25, y_origin + 0.5),  # 第一个控制点，向外扩展
                        (0.75, y_destination - 0.5),  # 第二个控制点，回收靠近终点
                        (1, y_destination),  # 终点
                    ],
                    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
                )
            else:
                # 弧形曲线
                mid_x = 0.5
                mid_y = (y_origin + y_destination) / 2
                path = Path(
                    [
                        (0, y_origin),  # 起点
                        (mid_x, mid_y),  # 控制点
                        (1, y_destination),  # 终点
                    ],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3]
                )
        else:
            # 垂直布局
            x_origin = node_pos[origin]
            x_destination = node_pos[destination]
            
            if curve_type == 's':
                path = Path(
                    [
                        (x_origin, 0),  # 起点
                        (x_origin + 0.5, 0.25),  # 第一个控制点
                        (x_destination - 0.5, 0.75),  # 第二个控制点
                        (x_destination, 1),  # 终点
                    ],
                    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
                )
            else:
                # 弧形曲线
                mid_x = (x_origin + x_destination) / 2
                mid_y = 0.5
                path = Path(
                    [
                        (x_origin, 0),  # 起点
                        (mid_x, mid_y),  # 控制点
                        (x_destination, 1),  # 终点
                    ],
                    [Path.MOVETO, Path.CURVE3, Path.CURVE3]
                )
        
        # 根据流量值设置线宽
        width = value / 10 if value > 0 else 0.1
        
        # 根据起点站选择颜色
        color = colors[node_pos[origin]]
        
        # 创建路径和绘制曲线
        patch = PathPatch(path, lw=width, edgecolor=color, facecolor="none", alpha=0.6)
        ax.add_patch(patch)
    
    # 设置节点标签
    if horizontal:
        # 设置Y轴刻度和标签
        ax.set_yticks(range(len(nodes)))
        ax.set_yticklabels(nodes, fontsize=12)
        
        # 在右侧添加站点标签
        for i, node in enumerate(nodes):
            ax.text(1.02, i, node, fontsize=12, va="center")
        
        # 设置X轴刻度和标签
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["出发", "到达"], fontsize=12)
        
        # 设置轴范围
        ax.set_xlim(-0.1, 1.2)
        ax.set_ylim(-0.5, len(nodes) - 0.5)
    else:
        # 设置X轴刻度和标签
        ax.set_xticks(range(len(nodes)))
        ax.set_xticklabels(nodes, fontsize=12, rotation=45, ha='right')
        
        # 设置Y轴刻度和标签
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["出发", "到达"], fontsize=12)
        
        # 设置轴范围
        ax.set_xlim(-0.5, len(nodes) - 0.5)
        ax.set_ylim(-0.1, 1.2)
    
    # 美化图形
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # 添加标题
    if title:
        plt.title(title, fontsize=16)
    
    plt.tight_layout()
    
    # 保存图表
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    # 显示图表
    if show:
        plt.show()
        
    return fig, ax 