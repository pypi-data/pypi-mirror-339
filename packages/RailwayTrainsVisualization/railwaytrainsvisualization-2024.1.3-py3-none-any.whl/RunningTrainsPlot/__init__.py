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
"""

from . import column_flow
from . import speed_curve
from . import cyclic_diagram
from . import track_occupation
from . import passenger_flow
from . import utils

__version__ = '2024.1.3' 