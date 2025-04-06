#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : generate_ternary_plot.py
@Time    : 2025/03/17 21:34:56
@Author  : Qing-Feng Mei
@Version : 1.0
@Desc    : None
"""

import ternary
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def normalize_data_to_scale(
    data: pd.DataFrame | np.ndarray, columns: list[str] = None, scale=100
) -> np.ndarray:
    """
    将输入数据归一化为和为100的比例坐标

    适用于三元图数据预处理，将原始数据转换为比例坐标系

    Parameters:
        data : Union[pd.DataFrame, np.ndarray]
            输入数据，支持Pandas DataFrame或Numpy数组
            当为DataFrame时，会自动转换为Numpy数组
        columns : Optional[list[str]], default=None
            仅当输入为DataFrame时有效，指定要使用的列名
            默认使用所有列

    Returns:
        np.ndarray
            归一化后的Numpy数组，形状与输入一致
            每行元素总和为100（百分比形式）

    Raises:
        ValueError: 当输入数据类型不符合要求时抛出

    Example:
        >>> data = pd.DataFrame({'A': [10,20], 'B': [20,30], 'C': [70,50]})
        >>> normalize_data(data)
        array([[10., 20., 70.],
               [20., 30., 50.]])
    """
    # 类型检查和处理
    if isinstance(data, pd.DataFrame):
        # 未指定列时使用全部列
        if columns is None:
            columns = data.columns
        data = data[columns].values  # 转换为numpy数组
    elif not isinstance(data, np.ndarray):
        raise ValueError("输入数据必须为Numpy数组或Pandas DataFrame")

    # 计算行和并保持二维结构（用于广播）
    row_sums = np.sum(data, axis=1).reshape(-1, 1)
    # 归一化计算（避免除以零错误）
    normalized_data = np.divide(data, row_sums, where=row_sums != 0) * scale

    return normalized_data


def new_ternary_plot(
    tax: ternary.TernaryAxesSubplot = None,
    fontsize: int = 8,
    labels: dict = None,
    scale: int = 100,
    **kwargs,
) -> ternary.TernaryAxesSubplot:
    """
    Configure basic ternary plot settings.
    """
    # 新增图形比例设置
    # 在创建坐标系后添加背景色设置
    if tax is None:
        fig, tax = ternary.figure(scale=scale, **kwargs)
        fig.set_size_inches(3.5, 3.5)

    else:
        tax = (
            tax
            if isinstance(tax, ternary.TernaryAxesSubplot)
            else ternary.TernaryAxesSubplot(ax=tax, scale=scale)
        )
    # 统一应用基础样式

    # 隐藏底层笛卡尔坐标

    tax.clear_matplotlib_ticks()
    tax.get_axes().axis("off")
    tax.get_axes().set_aspect("equal")  # 强制等比例显示
    # tax.get_axes().fill([0, 100, 50],[0, 0, 50*(3**0.5)], color='lightblue', alpha=1, zorder =0)
    tax.gridlines(color="gray", multiple=10, linewidth=0.5, alpha=0.5)
    tax.boundary(linewidth=1.0, **kwargs)
    # 设置标签（保持原有逻辑）
    default_labels = {"left": "Left", "right": "Right", "top": "Top"}
    if labels:
        if not all(key in default_labels for key in labels):
            raise ValueError(
                "Labels dictionary must contain keys: 'left', 'right', 'top'"
            )
        default_labels.update(labels)

    tax.left_corner_label(default_labels["left"], fontsize=fontsize)
    tax.right_corner_label(default_labels["right"], fontsize=fontsize)
    tax.top_corner_label(default_labels["top"], fontsize=fontsize)

    tax.ticks(
        axis="lbr",
        linewidth=1,
        multiple=10,
        offset=0.02,  # 保持一致的偏移量
        fontsize=fontsize - 2,  # 统一设置刻度标签字号
    )

    return tax

import math

def rtl_to_xy(ternary_rtl, scale=100):
    """
    将三元坐标（右, 上, 左）转换为笛卡尔坐标

    参数:
        ternary : 元组，格式为 (右, 上, 左)，例如 (30, 40, 30)
        scale   : 三元坐标总和，默认100

    返回:
        (x, y)  : 笛卡尔坐标元组

    规则:
        - 右顶点坐标： (scale, 0)
        - 上顶点坐标： (scale/2, scale*sqrt(3)/2)
        - 左顶点坐标： (0, 0)
    """
    # 输入校验
    if len(ternary_rtl) != 3:
        raise ValueError("元组必须包含三个元素：右、上、左")
    right, top, left = ternary_rtl
    if (total := right + top + left) != scale:
        raise ValueError(f"三元坐标和必须为 {scale}（当前和为 {total}）")

    # 计算笛卡尔坐标（左分量不参与计算）
    x = right + top / 2          # 右分量 + 上分量的水平投影
    y = top * (math.sqrt(3) / 2) # 上分量的垂直高度
    return (x, y)


def xy_to_rtl(cartesian_xy, scale=100):
    """
    将笛卡尔坐标转换为三元坐标（右, 上, 左）

    参数:
        cartesian_xy : 元组，格式为 (x, y)
        scale        : 三元坐标总和，默认100

    返回:
        (right, top, left) : 三元坐标元组

    规则:
        基于等边三角形坐标系转换：
        - y轴方向对应三元坐标的top分量
        - x轴在三角形底边从左(0,0)到右(scale,0)
    """
    x, y = cartesian_xy

    # 计算top分量（垂直高度）
    top = y * 2 / math.sqrt(3)

    # 计算right分量（水平投影）
    right = x - top / 2

    # 计算left分量（剩余部分）
    left = scale - right - top

    # 校验坐标有效性
    if any(n < 0 for n in (right, top, left)):
        raise ValueError(f"坐标超出三元图范围: ({right:.2f}, {top:.2f}, {left:.2f})")

    return (right, top, left)


if __name__ == "__main__":
    data = pd.DataFrame({"A": [10, 20], "B": [20, 30], "C": [70, 50]})
    tax = new_ternary_plot()
    tax.scatter(normalize_data_to_scale(data), s=5, color="r", alpha=0.8)
    plt.show()
    # 顶点测试
    print(rtl_to_xy((100, 0, 0)))   # 右顶点 → (100, 0)
    print(rtl_to_xy((0, 100, 0)))   # 上顶点 → (50, 86.60)
    print(rtl_to_xy((0, 0, 100)))   # 左顶点 → (0, 0)

    # 混合测试
    print(rtl_to_xy((30, 40, 30)))  # → (30+20=50, 40 * 0.866≈34.64)


    print(xy_to_rtl((100, 0)))          # (100.0, 0.0, 0.0)
    print(xy_to_rtl((50, 86.6025)))     # (0.0, 100.0, 0.0)
    print(xy_to_rtl((0, 0)))            # (0.0, 0.0, 100.0)

    # 测试内部点
    print(xy_to_rtl((50, 34.641)))      # (30.0, 40.0, 30.0)