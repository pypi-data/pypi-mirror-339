"""
speed_curve - 速度曲线可视化模块

提供列车速度与距离/时间曲线的可视化功能
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

__all__ = ['plot_speed_curve', 'load_speed_data']

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

def plot_speed_curve(data, x_col='distance', y_col='speed', train_id=None, 
                    figsize=(12, 6), title='列车速度曲线', save_path=None, **kwargs):
    """
    绘制列车速度曲线
    
    参数:
        data: 包含速度和距离/时间数据的DataFrame
        x_col: x轴列名，可以是'distance'或'time'
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
    x_label = '距离 (km)' if x_col == 'distance' else '时间 (min)'
    ax.set_xlabel(x_label)
    ax.set_ylabel('速度 (km/h)')
    
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
        ax.text(max_speed_pos, max_speed*1.05, f'最高速度: {max_speed:.1f} km/h', 
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
    
    # 绘制速度-距离曲线
    ax1.plot(data['distance'], data['speed'], 'b-', linewidth=2)
    ax1.set_xlabel('距离 (km)')
    ax1.set_ylabel('速度 (km/h)')
    ax1.set_title('速度-距离曲线')
    ax1.grid(True)
    
    # 绘制速度-时间曲线
    ax2.plot(data['time'], data['speed'], 'g-', linewidth=2)
    ax2.set_xlabel('时间 (min)')
    ax2.set_ylabel('速度 (km/h)')
    ax2.set_title('速度-时间曲线')
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    return fig 