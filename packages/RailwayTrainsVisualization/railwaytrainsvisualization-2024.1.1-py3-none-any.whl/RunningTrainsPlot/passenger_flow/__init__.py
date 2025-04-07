"""
passenger_flow - 客流OD图表可视化模块

提供客流OD数据的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 从原始Passenger-flow-OD-chart-RunningTrainsPlot导入所有公共函数
try:
    from Passenger_flow_OD_chart_RunningTrainsPlot import *
except ImportError:
    # 当原模块不可用时的后备处理
    pass

# 导出主要函数
__all__ = ['plot_passenger_flow', 'load_data']

def load_data(file_path):
    """
    加载客流OD数据
    
    参数:
        file_path: 客流数据文件路径
        
    返回:
        data: 客流数据DataFrame
    """
    data = pd.read_csv(file_path)
    return data

def plot_passenger_flow(data, origin_col='origin', destination_col='destination', 
                       flow_col='flow', figsize=(12, 10), title='客流OD图',
                       station_color='blue', flow_cmap='YlOrRd', save_path=None, **kwargs):
    """
    绘制客流OD图表
    
    参数:
        data: 客流数据DataFrame，包含起始站、终到站和流量
        origin_col: 起始站列名
        destination_col: 终到站列名
        flow_col: 流量列名
        figsize: 图表尺寸，默认(12, 10)
        title: 图表标题
        station_color: 站点颜色
        flow_cmap: 流量颜色映射
        save_path: 保存图表的路径，默认为None
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 获取所有站点
    all_stations = list(set(data[origin_col].tolist() + data[destination_col].tolist()))
    stations = {station: idx for idx, station in enumerate(all_stations)}
    
    # 计算站点位置（圆形布局）
    n_stations = len(stations)
    angles = np.linspace(0, 2*np.pi, n_stations, endpoint=False)
    
    pos = {}
    for station, idx in stations.items():
        pos[station] = (np.cos(angles[idx]), np.sin(angles[idx]))
    
    # 绘制站点
    for station, (x, y) in pos.items():
        ax.scatter(x, y, color=station_color, s=100, zorder=2)
        ax.text(x*1.1, y*1.1, station, ha='center', va='center', fontsize=10)
    
    # 绘制流量
    max_flow = data[flow_col].max()
    
    for _, row in data.iterrows():
        origin = row[origin_col]
        dest = row[destination_col]
        flow = row[flow_col]
        
        if origin != dest:  # 忽略自环
            x1, y1 = pos[origin]
            x2, y2 = pos[dest]
            
            # 确定线宽和颜色
            width = 1 + 5 * (flow / max_flow)
            color_intensity = flow / max_flow
            
            # 创建弧线（避免直线交叉过多）
            # 计算中点偏移
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # 法线方向
            norm_x = -(y2 - y1)
            norm_y = x2 - x1
            length = np.sqrt(norm_x**2 + norm_y**2)
            
            # 弧线控制点
            ctrl_x = mid_x + 0.3 * (norm_x / length)
            ctrl_y = mid_y + 0.3 * (norm_y / length)
            
            # 使用Path和PathPatch创建弧线
            from matplotlib.path import Path
            from matplotlib.patches import PathPatch
            
            path = Path([(x1, y1), (ctrl_x, ctrl_y), (x2, y2)],
                       [Path.MOVETO, Path.CURVE3, Path.CURVE3])
            
            patch = PathPatch(path, facecolor='none', 
                             edgecolor=plt.cm.get_cmap(flow_cmap)(color_intensity), 
                             linewidth=width, alpha=0.7, zorder=1)
            ax.add_patch(patch)
            
            # 在弧线中点添加流量标签
            ax.text(ctrl_x, ctrl_y, f"{flow}", 
                   ha='center', va='center', fontsize=8, 
                   bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    # 设置图表格式
    ax.set_title(title, fontsize=14)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig, ax 