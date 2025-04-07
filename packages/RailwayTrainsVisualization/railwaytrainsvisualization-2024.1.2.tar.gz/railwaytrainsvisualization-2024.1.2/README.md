# RunningTrainsPlot

为研究人员与工程技术人员提供的可扩展、可交互的铁路可视化工具。

## 功能特点

- **列流图 (Column Flow Chart)**：铁路线路流量可视化
- **速度曲线 (Speed Curve)**：列车速度-距离/时间曲线可视化
- **循环运行图 (Cyclic Diagram)**：列车循环运行图可视化
- **股道占用图 (Track Occupation)**：列车股道占用可视化
- **客流OD图 (Passenger Flow OD Chart)**：站点间客流可视化
- **工具函数**：数据加载、预处理和可视化工具

## 安装

```bash
pip install RunningTrainsPlot
```

## 快速开始

### 列流图

```python
from RunningTrainsPlot import column_flow

# 加载数据
stations, flows = column_flow.load_flow_data("stations.csv", "flows.csv")

# 绘制图表
column_flow.plot_column_flow(stations, flows)
```

### 速度曲线

```python
from RunningTrainsPlot import speed_curve

# 加载数据
data = speed_curve.load_speed_data("speed_data.csv")

# 绘制速度-距离曲线
speed_curve.plot_speed_curve(data, x_col='distance', y_col='speed')

# 绘制速度-时间曲线
speed_curve.plot_speed_curve(data, x_col='time', y_col='speed')

# 同时绘制两种曲线
speed_curve.plot_speed_distance_time(data)
```

### 循环运行图

```python
from RunningTrainsPlot import cyclic_diagram

# 加载数据
data = cyclic_diagram.load_data("cycle_data.csv")

# 绘制图表
cyclic_diagram.plot_cyclic_diagram(data)
```

### 股道占用图

```python
from RunningTrainsPlot import track_occupation

# 加载数据
data = track_occupation.load_track_data("track_data.csv")

# 绘制股道占用图
track_occupation.plot_track_occupation(data)
```

### 客流OD图表

```python
from RunningTrainsPlot import passenger_flow

# 加载数据
data = passenger_flow.load_data("passenger_data.csv")

# 绘制图表
passenger_flow.plot_passenger_flow(data)
```

## 数据工具

```python
from RunningTrainsPlot import utils

# 加载数据
data = utils.load_data("data.csv")

# 预处理数据
processed_data = utils.preprocess_data(data)
```

## 作者

- ZeyuShen <sc22zs2@leeds.ac.uk>

## 许可证

MIT
