"""
cyclic_diagram - 循环图表可视化模块

提供循环图表数据的可视化功能
"""

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 导出主要函数
__all__ = ['plot_cyclic_diagram', 'load_cyclic_data']

def load_cyclic_data(diagram_file, station_file=None):
    """
    加载循环运行图数据
    
    参数:
        diagram_file: 运行图数据CSV文件路径
        station_file: 站点数据CSV文件路径，默认为None
        
    返回:
        如果同时提供diagram_file和station_file:
            g_draw_seq_no, train_id, line_id, station_id, station_name, 
            x_time_in_min, y_station_location, stationname, location
        如果只提供diagram_file:
            g_draw_seq_no, train_id, line_id, station_id, station_name, 
            x_time_in_min, y_station_location
    """
    try:
        # 读取列车运行数据
        with open(diagram_file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            
            g_draw_seq_no = []
            train_id = []
            line_id = []
            station_id = []
            station_name = []
            x_time_in_min = []
            y_station_location = []
            
            for row in readCSV:
                g_draw_seq_no.append(row[0])
                train_id.append(row[1])
                line_id.append(row[2])
                station_id.append(row[3])
                station_name.append(row[4])
                x_time_in_min.append(row[5])
                y_station_location.append(row[6])
                
        # 移除标题行
        g_draw_seq_no.remove(g_draw_seq_no[0])
        train_id.remove(train_id[0])
        line_id.remove(line_id[0])
        station_id.remove(station_id[0])
        station_name.remove(station_name[0])
        x_time_in_min.remove(x_time_in_min[0])
        y_station_location.remove(y_station_location[0])
        
        if station_file:
            # 读取站点数据
            with open(station_file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                
                stationname = []
                location = []
                
                for row in readCSV:
                    stationname.append(row[0])
                    location.append(row[1])
                    
            # 移除标题行
            stationname.remove(stationname[0])
            location.remove(location[0])
            
            # 转换位置为浮点数
            float_location = list(map(float, location))
            
            return g_draw_seq_no, train_id, line_id, station_id, station_name, x_time_in_min, y_station_location, stationname, float_location
            
        return g_draw_seq_no, train_id, line_id, station_id, station_name, x_time_in_min, y_station_location
            
    except Exception as e:
        print(f"加载数据失败: {str(e)}")
        raise

def plot_cyclic_diagram(data, station_data=None, figsize=(12, 8), 
                      family='Times new roman', 
                      x_range=(0, 90), x_ticks=range(0, 100, 10),  
                      y_range=None, 
                      save_path=None, show=True, dpi=300, **kwargs):
    """
    绘制循环运行图
    
    参数:
        data: 运行图数据，可以是以下格式之一:
            1. 从load_cyclic_data加载的元组
            2. 包含所需列的DataFrame
            3. 包含所需数据的CSV文件路径
        station_data: 站点数据，可以是以下格式之一:
            1. 从load_cyclic_data加载的元组的一部分
            2. 包含站点数据的DataFrame
            3. 包含站点数据的CSV文件路径
        figsize: 图表尺寸，默认(12, 8)
        family: 字体族，默认'Times new roman'
        x_range: X轴范围，默认(0, 90)
        x_ticks: X轴刻度，默认range(0, 100, 10)
        y_range: Y轴范围，如果为None则自动计算
        save_path: 保存图表的路径，默认为None
        show: 是否显示图表，默认True
        dpi: 图像分辨率，默认300
        **kwargs: 附加参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    # 处理输入数据
    g_draw_seq_no, train_id, line_id, station_id, station_name = None, None, None, None, None
    x_time_in_min, y_station_location = None, None
    stationname, location = None, None
    
    # 如果数据是元组，直接解包
    if isinstance(data, tuple):
        if len(data) >= 7:
            g_draw_seq_no, train_id, line_id, station_id, station_name, x_time_in_min, y_station_location = data[:7]
    
    # 如果数据是DataFrame
    elif isinstance(data, pd.DataFrame):
        df = data
        g_draw_seq_no = df['g_draw_seq_no'].astype(str).tolist()
        train_id = df['train_id'].astype(str).tolist()
        line_id = df['line_id'].astype(str).tolist()
        station_id = df['station_id'].astype(str).tolist()
        station_name = df['station_name'].astype(str).tolist()
        x_time_in_min = df['x_time_in_min'].astype(str).tolist()
        y_station_location = df['y_station_location'].astype(str).tolist()
    
    # 如果数据是CSV文件路径
    elif isinstance(data, str):
        loaded_data = load_cyclic_data(data)
        g_draw_seq_no, train_id, line_id, station_id, station_name, x_time_in_min, y_station_location = loaded_data
    
    # 处理站点数据
    if isinstance(station_data, tuple) and len(station_data) >= 2:
        stationname, location = station_data
    elif isinstance(station_data, list) and len(station_data) >= 8:
        stationname, location = station_data[7:9]
    elif isinstance(station_data, pd.DataFrame):
        df = station_data
        stationname = df['station'].tolist() if 'station' in df.columns else []
        location = df['location'].astype(float).tolist() if 'location' in df.columns else []
    elif isinstance(station_data, str):
        _, _, _, _, _, _, _, stationname, location = load_cyclic_data(data, station_data)
    
    # 设置颜色映射 - 更新匹配参考图像的颜色
    color_value = {
        '1': 'midnightblue', 
        '2': 'mediumblue', 
        '3': 'c',
        '4': 'orangered',
        '5': 'm',
        '6': 'fuchsia',
        '7': 'olive'
    }
    
    # 创建画布
    fig, ax = plt.subplots(figsize=figsize)
    
    # 转换字符串值为数值
    y_values = [int(y) for y in y_station_location]
    x_values = [int(x) for x in x_time_in_min]
    
    # 如果没有指定y_range，则自动计算
    if y_range is None:
        min_y = min(y_values) if y_values else 0
        max_y = max(y_values) if y_values else 100
        y_range = (min_y, max_y)
    
    # 绘制列车运行线
    xlist = []
    ylist = []
    
    for i in range(len(g_draw_seq_no)):
        next_line_no = min(i + 1, len(g_draw_seq_no) - 1)
        
        if train_id[i] == train_id[next_line_no]:  # 当前列车
            if g_draw_seq_no[i] == g_draw_seq_no[next_line_no]:
                if next_line_no == len(g_draw_seq_no) - 1:
                    xlist.append(int(x_time_in_min[i]))
                    ylist.append(int(y_station_location[i]))
                    plt.plot(xlist, ylist, color=color_value[str(line_id[i])], linewidth=1.5)
                    # 添加线路标签 - 调整位置和样式
                    plt.text(xlist[0] + 0.8, ylist[0] + 4, str(line_id[i]), 
                            ha='center', va='bottom', 
                            color=color_value[str(line_id[i])], 
                            weight='bold', family=family, fontsize=9)
                else:
                    xlist.append(int(x_time_in_min[i]))
                    ylist.append(int(y_station_location[i]))
            else:
                xlist.append(int(x_time_in_min[i]))
                ylist.append(int(y_station_location[i]))
                plt.plot(xlist, ylist, color=color_value[str(line_id[i])], linewidth=1.5)
                plt.text(xlist[0] + 0.8, ylist[0] + 4, str(line_id[i]), 
                        ha='center', va='bottom', 
                        color=color_value[str(line_id[i])], 
                        weight='bold', family=family, fontsize=9)
                xlist = []
                ylist = []
        else:
            xlist.append(int(x_time_in_min[i]))
            ylist.append(int(y_station_location[i]))
            plt.plot(xlist, ylist, color=color_value[str(line_id[i])], linewidth=1.5)
            plt.text(xlist[0] + 0.8, ylist[0] + 4, str(line_id[i]), 
                    ha='center', va='bottom', 
                    color=color_value[str(line_id[i])], 
                    weight='bold', family=family, fontsize=9)
            xlist = []
            ylist = []
    
    # 设置精确网格
    plt.grid(True, linestyle='-', alpha=0.3)
    
    # 设置坐标范围
    plt.ylim(*y_range)
    plt.xlim(*x_range)
    plt.xticks(x_ticks)
    
    # 设置站点标签
    if stationname and location:
        # 只显示第一个和最后一个站点名称
        if len(stationname) >= 2:
            labels = [''] * len(location)
            labels[0] = stationname[0]
            labels[-1] = stationname[-1]
            plt.yticks(location, labels)
        else:
            plt.yticks(location, stationname)
    
    # 设置轴标签
    plt.xlabel('Time (min)')
    plt.ylabel('Space (km)')
    
    # 移除轴框
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    # 保存和显示图表
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig, ax 