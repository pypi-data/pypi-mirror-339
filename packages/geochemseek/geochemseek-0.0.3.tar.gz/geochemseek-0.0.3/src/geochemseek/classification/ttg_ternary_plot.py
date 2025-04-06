#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : ttg_ternary_plot.py
@Time    : 2025/03/18 00:59:34
@Author  : Qing-Feng Mei
@Version : 1.0
@Desc    : None
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geochemseek.config

from geochemseek.utils.ternary_plot import new_ternary_plot, normalize_data_to_scale
from geochemseek.utils.annotate import annotate_samples


def ttg_ternary_plot(
    data,
    plot_type="Barker",
    tax=None,
    annotate_sample_names: bool = False,
    sample_labels=None,
    scale=100,
    **kwargs,
):
    """
    创建 TTG 系列岩石分类三元图

    参数：
        data (pd.DataFrame): 包含 Or(钾长石)、An(钙长石)、Ab(钠长石) 成分的原始数据
        plot_type (str): 绘图类型，可选 "Barker" 或 "O'Connor"（默认："Barker"）
        tax (TernaryAxesSubplot): 可重复使用的三元图坐标系对象（默认：新建坐标系）
        annotate_samples (bool): 是否标注样本名称（默认：False）
        sample_labels (Union[pd.Series, list]): 样本标签序列，当 annotate_samples=True 时必须提供
        scale (int): 三元图坐标尺度（默认：100）
        **kwargs: 传递给 new_ternary_plot 的额外参数

    返回：
        TernaryAxesSubplot: 包含绘图元素的三元图坐标系对象

    异常：
        ValueError: 当 plot_type 参数错误或样本标注参数不完整时抛出
        TypeError: 当 sample_labels 类型不符合要求时抛出
    """
    # 数据归一化处理（将原始数据转换为三元坐标系）
    columns = ["Or", "An", "Ab"]  # 固定列名对应长石成分
    normalized_data = normalize_data_to_scale(data=data, columns=columns, scale=scale)

    # 坐标系标签配置
    corner_labels = {"left": columns[2], "right": columns[0], "top": columns[1]}

    # 新增：传递 matplotlib axes 对象
    tax = new_ternary_plot(tax=tax, labels=corner_labels, scale=scale, **kwargs)

    # Barker 分类方案背景绘制
    if plot_type.lower() == "barker":
        # Barker 方案特征线段数据集
        bg_data = np.array(
            [
                [0, 30, 70],
                [20, 20, 60],
                [20, 32, 48],
                [20, 20, 60],
                [25, 17.5, 57.5],
                [30, 0, 70],
                [25, 17.5, 57.5],
                [35, 15, 50],
                [35, 26, 39],
            ]
        )  # 恢复完整数据集
        tax.plot(bg_data, lw=0.5, color="k", alpha=0.75)
        # 岩石类型标注（坐标经过实验验证）
        tax.annotate("Trondhjemite", (2, 10, 88), fontsize=6)
        tax.annotate("Granite", (30, 10, 60), fontsize=6)
        tax.annotate("Tonalite", (10, 30, 60), rotation=60, fontsize=6)
        tax.annotate("Granodiorite", (25, 20, 55), rotation=60, fontsize=6)
    elif plot_type.lower() == "o'connor":
        # O'Connor 方案特征线段数据集
        lines_solid = [
            [(0, 25, 75), (50, 12.5, 37.5)],
            [(30, 17.5, 52.5), (30, 0, 0)],
            [(20, 20, 60), (20, 45, 35)],
        ]
        lines_dashed = [
            [(50, 12.5, 37.5), (100, 0, 0)],
            [(35, 16.25, 48.75), (35, 38, 27)],
            [(50, 12.5, 37.5), (50, 30, 20)],
        ]
        for p1, p2 in lines_solid:
            tax.line(p1, p2, linewidth=0.5, color="k", linestyle="-", alpha=0.75)
        for p1, p2 in lines_dashed:
            tax.line(p1, p2, linewidth=0.5, color="k", linestyle="--", alpha=0.75)
        tax.annotate("Trondhjemite", (4, 8, 88), fontsize=6)
        tax.annotate("Granite", (35, 8, 57), fontsize=6)
        tax.annotate("Tonalite", (10, 25, 65), rotation=60, fontsize=6)
        tax.annotate("Granodiorite", (25, 22, 53), rotation=60, fontsize=6)
        tax.annotate("Quartz monzonite", (40, 18, 42), rotation=60, fontsize=6)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    # 数据点绘制配置
    tax.scatter(normalized_data, s=5, color="r", alpha=0.8)

    # 样本标注系统
    if annotate_sample_names:
        if sample_labels is None:
            raise ValueError("启用标注时必须提供 sample_labels 参数")
        else:
            annotate_samples(ax=tax, points=normalized_data, sample_labels=sample_labels, fontsize=4, ha="left",
                             va="bottom", xytext=(2, 2))

    return tax  # 返回坐标系对象便于重复使用


if __name__ == "__main__":
    """
    示例用法：
    1. 准备包含 Or、An、Ab 列的数据集
    2. 直接调用绘图函数并保存结果
    """
    # 示例数据集（包含样本名称列）

    sample_data = pd.DataFrame(
        {"An": [20, 30], "Or": [10, 20], "Ab": [70, 50], "sample": ["S1", "S2"]}
    )

    # 生成带样本标注的 Barker 分类图
    ttg_ternary_plot(
        data=sample_data,
        plot_type="Barker",
        annotate_sample_names=True,
        sample_labels=sample_data["sample"],
    )

    # 使用示例

    # 创建标准 matplotlib 子图时指定布局参数
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 3.5))  # 调整宽度比例

    # 绘制常规图表在左轴
    ax1.plot([1, 2, 3], [4, 5, 6])

    # 在右轴绘制三元图
    ttg_ternary_plot(sample_data, tax=ax2, plot_type="Barker")

    plt.show()
