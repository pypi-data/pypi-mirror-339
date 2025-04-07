"""
column_flow - 列流图可视化模块

提供铁路列流数据的可视化功能
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['plot_column_flow', 'load_flow_data']

def load_flow_data(stations_file, flows_file):
    """
    加载列流图所需的数据
    
    参数:
        stations_file: 站点数据文件路径
        flows_file: 流量数据文件路径
        
    返回:
        stations: 站点数据DataFrame
        flows: 流量数据DataFrame
    """
    stations = pd.read_csv(stations_file)
    flows = pd.read_csv(flows_file)
    return stations, flows

def plot_column_flow(stations, flows, figsize=(12, 8), save_path=None, **kwargs):
    """
    绘制铁路列流图
    
    参数:
        stations: 站点数据DataFrame，包含站点名称和位置
        flows: 流量数据DataFrame，包含起始站、终到站和流量
        figsize: 图表尺寸，默认(12, 8)
        save_path: 保存图表的路径，默认为None
        **kwargs: 附加绘图参数
        
    返回:
        fig, ax: matplotlib图表对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 绘制站点
    station_positions = {}
    for i, row in stations.iterrows():
        station_name = row['name']
        position = row['position']
        station_positions[station_name] = position
        ax.text(position, 0, station_name, ha='center', va='bottom', fontsize=12)
        ax.plot([position, position], [0, 0.1], 'k-', lw=2)
    
    # 绘制铁路线
    min_pos = min(station_positions.values())
    max_pos = max(station_positions.values())
    ax.plot([min_pos, max_pos], [0, 0], 'k-', lw=3)
    
    # 绘制流量
    for i, flow in flows.iterrows():
        start = flow['start']
        end = flow['end']
        value = flow['value']
        
        if start in station_positions and end in station_positions:
            x1 = station_positions[start]
            x2 = station_positions[end]
            mid = (x1 + x2) / 2
            height = 0.5 + i * 0.2  # 避免重叠
            
            # 绘制弧线
            x = np.linspace(x1, x2, 100)
            y = np.zeros_like(x)
            y = height * np.sin(np.pi * (x - x1) / (x2 - x1))
            
            # 根据流量设置线宽
            lw = 1 + value / 10
            ax.plot(x, y, 'b-', lw=lw, alpha=0.7)
            
            # 流量标签
            ax.text(mid, height + 0.05, f"{value}", ha='center', va='bottom')
    
    ax.set_ylim(0, 3)
    ax.set_xlim(min_pos - 1, max_pos + 1)
    ax.set_title("铁路列流图", fontsize=16)
    ax.set_yticks([])
    ax.set_xlabel("站点位置", fontsize=12)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig, ax 