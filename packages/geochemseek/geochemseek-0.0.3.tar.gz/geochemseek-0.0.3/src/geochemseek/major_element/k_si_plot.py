#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : k_si_plot.py
# @Author  : Qing-Feng Mei
# @Email   : meiqingfeng@mail.iggcas.ac.cn
# @Date    : 2025/3/19
# @Project : geochemseek-project
# @Desc    : None


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geochemseek.config
from typing import Optional

def k_si_plot(data: pd.DataFrame, ax: Optional[plt.Axes] = None, **kwargs) -> plt.Axes:
    """
    绘制 K2O-SiO2 图解，用于岩石地球化学分类。

    Parameters
    ----------
    data : pd.DataFrame
        包含 SiO2 和 K2O 数据的 DataFrame，必须包含 'SiO2' 和 'K2O' 两列
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
    >>> data = pd.DataFrame({'SiO2': [45, 50, 55], 'K2O': [1.5, 2.0, 2.5]})
    >>> fig, ax = plt.subplots()
    >>> isinstance(k_si_plot(data, ax=ax, color='red', s=9), plt.Axes)
    True
    """
    if ax is None:
        fig, ax = plt.subplots()
    boundary_1 = (
    (45.0, 1.38), (48.0, 1.7), (56.0, 3.3), (63.0, 4.2), (70.0, 5.1),
    (70.0, 4.61), (63.0, 3.87), (56.0, 2.98), (48.0, 1.6), (45.0, 1.37), (45.0, 1.38))
    boundary_2 = (
    (45.0, 0.98), (49.0, 1.28), (52.0, 1.5), (63.0, 2.48), (70.0, 3.1), (75.0, 3.43),
    (75.0, 3.25), (70.0, 2.86), (63.0, 2.32), (52.0, 1.35), (49.0, 1.1), (45.0, 0.92), (45.0, 0.98))
    boundary_3 = (
    (45.0, 0.2), (48.0, 0.41), (61.0, 0.97), (70.0, 1.38), (75.0, 1.51),
    (75.0, 1.44), (70.0, 1.23), (61.0, 0.8), (48.0, 0.3), (45.0, 0.15), (45.0, 0.2))
    boundary_4 = ((48.0, 1.2), (73.0, 3.575))
    boundary_5 = ((48.0, 0.3), (68.0, 1.2))
    boundary_6 = ((48.0, 0), (48.0, 3.0))
    boundary_1_df = pd.DataFrame(boundary_1, columns=['SiO2','K2O'])
    boundary_2_df = pd.DataFrame(boundary_2, columns=['SiO2','K2O'])
    boundary_3_df = pd.DataFrame(boundary_3, columns=['SiO2','K2O'])
    boundary_4_df = pd.DataFrame(boundary_4, columns=['SiO2','K2O'])
    boundary_5_df = pd.DataFrame(boundary_5, columns=['SiO2','K2O'])
    boundary_6_df = pd.DataFrame(boundary_6, columns=['SiO2','K2O'])
    ax.fill(boundary_1_df['SiO2'], boundary_1_df['K2O'], color='cornflowerblue')
    ax.fill(boundary_2_df['SiO2'], boundary_2_df['K2O'], color='cornflowerblue')
    ax.fill(boundary_3_df['SiO2'], boundary_3_df['K2O'], color='cornflowerblue')
    ax.plot(boundary_4_df['SiO2'], boundary_4_df['K2O'], 'k--', lw=0.5)
    ax.plot(boundary_5_df['SiO2'], boundary_5_df['K2O'], 'k--', lw=0.5)
    ax.plot(boundary_6_df['SiO2'], boundary_6_df['K2O'], 'k--', lw=0.5)
    text_list = ['tholeiitic series', 'calc-alkalic \nseries', 'calc-alkalic \nseries',
                 'shoshonite \nseries', 'low-K', 'medium-K', 'high-K']
    text_positions = [(55, 0.25), (55, 1.2), (55, 2.5), (55, 4.0), (67, 0.5), (67, 2.0), (67, 3.8)]
    for i, text in enumerate(text_list):
        ax.text(text_positions[i][0], text_positions[i][1], text, fontsize=8, ha='left', va='center')
    ax.set_xlim(45, 76)
    ax.set_ylim(0, 6)
    ax.scatter(data['SiO2'], data['K2O'], **kwargs)
    ax.set_xlabel('SiO$_2$ (wt.%)', fontsize=8)
    ax.set_ylabel('K$_2$O (wt.%)', fontsize=8)
    plt.show()
    return ax

if __name__ == '__main__':
    # 创建示例数据
    data = {
        'SiO2': [45.0, 50.0, 55.0, 60.0, 65.0],
        'K2O': [1.5, 2.0, 2.5, 3.0, 3.5]
    }
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize = (3.5,3))
    k_si_plot(df, ax=ax, marker='o', s=9, color='black')