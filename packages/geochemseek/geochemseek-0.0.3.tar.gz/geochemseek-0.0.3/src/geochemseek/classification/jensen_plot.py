#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : jensen_plot.py
@Time    : 2025/03/18 21:24:16
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




def jensen_plot(
    data,
    plot_type="Jensen",
    tax=None,
    annotate_sample_names: bool = False,
    sample_labels=None,
    scale=100,
    **kwargs,
):
    """ """
    # 数据归一化处理（将原始数据转换为三元坐标系）
    columns = ["Mg", "Fe + Ti", "Al"]  # 固定列名对应相应离子
    normalized_data = normalize_data_to_scale(data=data, columns=columns, scale=scale)

    # 坐标系标签配置
    corner_labels = {"left": "Al", "right": "Mg", "top": r"Fe$_T$ + Ti"}

    # 新增：传递 matplotlib axes 对象
    tax = new_ternary_plot(tax=tax, labels=corner_labels, scale=scale, **kwargs)

    # Jensen 分类方案背景绘制
    if plot_type.lower() == "jensen":
        # Jensen 方案特征线段数据集
        bg_data = np.array(
            [
                [0, 10, 90],
                [18, 28.5, 53.5],
                [18.5, 29, 52.5],
                [19.5, 29, 51.5],
                [22, 27.5, 50.5],
                [24.7, 25, 50.3],
                [29.2, 20, 50.8],
                [36, 12.5, 51.5],
            ]
        )  # 恢复完整数据集
        lines_solid = [
            [(50, 0, 50), (0, 100, 0)],
            [(60, 0, 40), (60, 22, 18)],
            [(60, 30, 10), (60, 40, 0)],
        ]
        lines_dashed = [
            [(20, 0, 80), (10, 10, 80)],
            [(30, 0, 70), (15, 15, 70)],
            [(40, 0, 60), (20, 20, 60)],
            [(0, 30, 70), (7, 23, 70)],
            [(0, 40, 60), (10, 30, 60)],
            [(0, 50, 50), (15, 35, 50)],
            [(15, 35, 50), (17, 32, 51)],
            [(17, 32, 51), (18.5, 29, 52.5)],

            [(24.7, 25, 50.3), (33.3, 33.4, 33.3)],
        ]
        for p1, p2 in lines_solid:
            tax.line(p1, p2, linewidth=1, color="k", linestyle="-")
        for p1, p2 in lines_dashed:
            tax.line(p1, p2, linewidth=0.75, color="k", linestyle=":")

        tax.plot(bg_data, lw=1, color="k")

        # 岩石类型标注（坐标经过实验验证）
        tax.annotate(
            "CALC-ALKALIC",
            (13, 17, 70),
            rotation=30,
            fontsize=7,
            ha="center",
            va="center",
        )
        tax.annotate(
            "THOLEIITIC", (9, 23, 68), rotation=30, fontsize=7, ha="center", va="center"
        )
        tax.annotate(
            "KOMATIITIC", (60, 25, 15), rotation=0, fontsize=7, ha="center", va="center"
        )
        tax.annotate(
            "Komatiitic\nbasalt",
            (50, 18, 32),
            rotation=0,
            fontsize=6,
            ha="center",
            va="center",
        )
        tax.annotate(
            "Komatiite",
            (73.4, 13.3, 13.3),
            rotation=0,
            fontsize=6,
            ha="center",
            va="center",
        )
        tax.annotate(
            "HFT", (15, 48, 37), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "HMT", (33, 22, 45), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "Rh", (10, 5, 85), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "Da", (15, 10, 75), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "An", (20, 15, 65), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "Ba", (25, 20, 55), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "Rh", (3, 24, 73), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "Da", (4, 30, 66), rotation=0, fontsize=6, ha="center", va="center"
        )
        tax.annotate(
            "An", (5, 40, 55), rotation=0, fontsize=6, ha="center", va="center"
        )

        # 添加图例框解释缩写（使用标准坐标系）
        legend_text = "\n".join(
            [
                "HFT: High-Fe tholeiite",
                "HMT: High-Mg tholeiite",
                "Rh: Rhyolite",
                "Da: Dacite",
                "An: Andesite",
                "Ba: Basalt",
            ]
        )
        # 获取底层 matplotlib 坐标系
        tax.ax.annotate(
            legend_text,
            xy=(0.00, 0.90),  # 坐标系比例定位
            xycoords="axes fraction",  # 使用标准坐标系
            fontsize=6,
            ha="left",
            va="top",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="none", edgecolor="none", alpha=1
            ),
        )

    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    # 数据点绘制配置
    tax.scatter(normalized_data, c = None, s=5, color='red', alpha=0.8, **kwargs)

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
    1. 准备包含 "Mg", "Fe + Ti", "Al" 列的数据集
    2. 直接调用绘图函数并保存结果
    """

    # 示例数据集（包含样本名称列）
    plt.rcParams['figure.dpi'] = 300  # 默认 100，建议 150~300
    plt.rcParams['savefig.dpi'] = 300  # 保存图片时的分辨率
    sample_data = pd.DataFrame(
        {"Mg": [20, 30], "Fe + Ti": [10, 20], "Al": [70, 50], "sample": ["S1", "S2"]}
    )


    tax = jensen_plot(
        data=sample_data,
        plot_type="Jensen",
        annotate_sample_names=False,
        sample_labels=sample_data["sample"],
    )
    plt.show()

    # 保存为 PDF 并显示路径
    # import os
    # save_path = os.path.abspath('jensen_demo.pdf')
    # plt.savefig(save_path,
    #            format='pdf',
    #            dpi=300,
    #            bbox_inches='tight')
    # print(f"PDF 已保存至：{save_path}")
    # plt.close()

