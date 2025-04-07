"""
RunningTrainsPlot - 为研究人员与工程技术人员提供的可扩展、可交互的铁路可视化工具

包含以下子模块:
- column_flow: 列流图可视化
- speed_curve: 速度曲线可视化  
- cyclic_diagram: 循环运行图可视化
- track_occupation: 股道占用图可视化
- passenger_flow: 客流OD图表可视化
- utils: 工具函数

作者: ZeyuShen <sc22zs2@leeds.ac.uk>

该包提供了用于分析和可视化铁路列车运行数据的工具，
包括列车运行图、列流图、客流OD图、股道占用图等功能。

原名称为RailwayTrainsVisualization，现更名为RunningTrainsPlot。
"""

# 配置中文字体支持
import matplotlib.pyplot as plt
import platform
import os

def _setup_chinese_fonts():
    """为不同操作系统配置中文字体支持"""
    system = platform.system()
    if system == 'Windows':
        # Windows系统
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']  # 优先使用微软雅黑
    elif system == 'Darwin':
        # macOS系统
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'STHeiti']
    else:
        # Linux系统
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK JP']
    
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    plt.rcParams['font.family'] = 'sans-serif'  # 设置默认字体

# 初始化时自动配置字体
_setup_chinese_fonts()

from . import column_flow
from . import speed_curve
from . import cyclic_diagram
from . import track_occupation
from . import passenger_flow
from . import utils

__version__ = '1.0.3'
__description__ = '铁路列车运行数据可视化工具'
__author__ = 'NJU Innovation Group'
__license__ = 'MIT'
__project_name__ = 'RunningTrainsPlot'

__all__ = [
    'passenger_flow',
    'column_flow',
    'speed_curve',
    'cyclic_diagram', 
    'track_occupation',
    'utils',
]

# 版本历史:
# 1.0.0 - 初始版本，从RailwayTrainsVisualization更名而来
# 1.0.1 - 新增原生循环运行图(cyclic_diagram)实现，不再依赖外部包
# 1.0.2 - 优化速度曲线模块，默认为速度-时间曲线，增加plot_speed_comparison函数
# 1.0.3 - 全面改进可视化模块，更贴近原始实现效果：
#        1. 列流图模块(column_flow)采用更直观的箭头表示
#        2. 股道占用图(track_occupation)增加三角形表示到发时间
#        3. 循环运行图(cyclic_diagram)重写为完全匹配原始格式
#        4. 客流OD图(passenger_flow)采用S形曲线布局
#        5. 增加中文字体支持，确保所有用户都能正确显示中文 