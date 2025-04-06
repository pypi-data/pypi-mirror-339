#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : tas_plot.py
# @Author  : Qing-Feng Mei
# @Email   : meiqingfeng@mail.iggcas.ac.cn
# @Date    : 2025/3/20
# @Project : geochemseek-project
# @Desc    : None


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geochemseek.config
from typing import Optional
from scipy.interpolate import make_interp_spline

def tas_plot(data: pd.DataFrame, ax: Optional[plt.Axes] = None, show_boundary = True, **kwargs) -> plt.Axes:
    """
    绘制 TAS（Total Alkali-Silica）图解，用于火山岩分类。

    Parameters
    ----------
    data : pd.DataFrame
        包含 SiO2、Na2O 和 K2O 数据的 DataFrame，必须包含 'SiO2'、'Na2O' 和 'K2O' 三列
    ax : Optional[plt.Axes], default None
        如果提供，将在指定的 Axes 对象上绘图；否则创建新的 figure 和 axes
    **kwargs : dict
        传递给 scatter 函数的其他参数，用于自定义散点图的样式

    Returns
    -------
    plt.Axes
        包含绘图的 Axes 对象

    Examples
    --------
    >>> data = pd.DataFrame({'SiO2': [45, 50, 55], 'K2O': [1.5, 2.0, 2.5], 'Na2O': [0.5, 1.0, 1.5]})
    >>> fig, ax = plt.subplots()
    >>> isinstance(tas_plot(data, ax=ax, color='red', s=9), plt.Axes)
    True

    Notes
    -----
    该函数基于 Le Bas et al. (1986) 提出的 TAS 分类方案绘制火山岩分类图。
    图中包含以下边界线：
    - 碱性系列与亚碱性系列的分界线
    - 不同火山岩类型的分界线
    """
    if ax is None:
        fig, ax = plt.subplots()
    boundary_1 = ((41, 0.3), (41, 3), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5),(63, 14.5625))
    boundary_2 = ((45, 0.3), (45, 3), (45, 5), (52, 5), (57, 5.9), (63, 7), (69, 8),(76.22, 0.3), (69, 8), (69, 13))
    boundary_3 = ((52, 0.3), (52, 5), (49.4, 7.3), (45, 9.4), (48.4, 11.5), (52.5, 14))
    boundary_4 = ((57, 0.3), (57, 5.9), (53, 9.3), (48.4, 11.5))
    boundary_5 = ((63, 0.3), (63, 7), (57.6, 11.7), (52.5, 14), (49.5, 15.353))
    boundary_6 = ((41, 3), (41, 7), (45, 9.4))
    boundary_main = ((41.56, 1), (43.28, 2.0), (45.47, 3), (48.18, 4.0), (51.02, 5), (53.72, 6.0),
                    (56.58, 7), (60.47, 8.0), (66.82, 9), (77.15, 10.0))

    boundary_1_df = pd.DataFrame(boundary_1, columns=['SiO2','total alkalis'])
    boundary_2_df = pd.DataFrame(boundary_2, columns=['SiO2','total alkalis'])
    boundary_3_df = pd.DataFrame(boundary_3, columns=['SiO2','total alkalis'])
    boundary_4_df = pd.DataFrame(boundary_4, columns=['SiO2','total alkalis'])
    boundary_5_df = pd.DataFrame(boundary_5, columns=['SiO2','total alkalis'])
    boundary_6_df = pd.DataFrame(boundary_6, columns=['SiO2','total alkalis'])
    ax.plot(boundary_1_df['SiO2'], boundary_1_df['total alkalis'], 'k-', lw=0.5)
    ax.plot(boundary_2_df['SiO2'], boundary_2_df['total alkalis'], 'k-', lw=0.5)
    ax.plot(boundary_3_df['SiO2'], boundary_3_df['total alkalis'], 'k-', lw=0.5)
    ax.plot(boundary_4_df['SiO2'], boundary_4_df['total alkalis'], 'k-', lw=0.5)
    ax.plot(boundary_5_df['SiO2'], boundary_5_df['total alkalis'], 'k-', lw=0.5)
    ax.plot(boundary_6_df['SiO2'], boundary_6_df['total alkalis'], 'k--', lw=0.5)

    boundary_main_df = pd.DataFrame(boundary_main, columns=['SiO2','total alkalis'])
    x_smooth = np.linspace(boundary_main_df['SiO2'].min(), boundary_main_df['SiO2'].max(), 300)
    spl = make_interp_spline(boundary_main_df['SiO2'], boundary_main_df['total alkalis'], k=3)
    y_smooth = spl(x_smooth)
    if show_boundary:
        ax.plot(x_smooth, y_smooth, 'k--', lw=1)

    ax.text(64, 4, 'sub-alkalic\nseries',  color= 'cornflowerblue',fontsize=8, ha='center', va='center', bbox=dict(
        boxstyle='square',edgecolor='w',facecolor='w'), zorder=2)
    ax.text(51.8, 12.5, 'alkalic series', color= 'cornflowerblue',fontsize=8, ha='center', va='center', bbox=dict(
        boxstyle='square',edgecolor='w',facecolor='w'), zorder=2)
    # text_list = ['tholeiitic series', 'calc-alkalic \nseries', 'calc-alkalic \nseries',
    #              'shoshonite \nseries', 'low-K', 'medium-K', 'high-K']
    # text_positions = [(55, 0.25), (55, 1.2), (55, 2.5), (55, 4.0), (67, 0.5), (67, 2.0), (67, 3.8)]
    # for i, text in enumerate(text_list):
    #     ax.text(text_positions[i][0], text_positions[i][1], text, fontsize=8, ha='left', va='center')

    ax.set_xlim(35, 80)
    ax.set_ylim(0, 16)
    ax.scatter(data['SiO2'], data['Na2O'] + data['K2O'], zorder=3, **kwargs)
    ax.set_xlabel('SiO$_2$ (wt.%)', fontsize=8)
    ax.set_ylabel('Na$_2$O+ K$_2$O (wt.%)', fontsize=8)
    plt.show(bbox_inches='tight')
    return ax

if __name__ == '__main__':
    # 创建示例数据
    data = {
        'SiO2': [45.0, 50.0, 55.0, 60.0, 65.0],
        'K2O': [1.5, 2.0, 2.5, 3.0, 3.5],
        'Na2O': [0.5, 1.0, 1.5, 2.0, 2.5]
    }
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize = (3.5,3))
    tas_plot(df, ax=ax, marker='o', s=9, color='black')
    plt.tight_layout()