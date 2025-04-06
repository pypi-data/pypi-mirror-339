#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : cia_plot.py
# @Author  : Qing-Feng Mei
# @Email   : meiqingfeng@mail.iggcas.ac.cn
# @Date    : 2025/3/21
# @Project : geochemseek-project
# @Desc    : None


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geochemseek.config
from geochemseek.utils.ternary_plot import new_ternary_plot, normalize_data_to_scale, rtl_to_xy
from geochemseek.utils.annotate import annotate_samples



def cia_plot(
    data,
    tax=None,
    annotate_sample_names: bool = False,
    sample_labels=None,
    scale=100,
    **kwargs,
):
    """ """
    # 数据归一化处理（将原始数据转换为三元坐标系）
    columns = ["K2O", "Al2O3", "CaO* + Na2O"]  # 固定列名对应相应离子
    normalized_data = normalize_data_to_scale(data=data, columns=columns, scale=scale)

    # 坐标系标签配置
    corner_labels = {"left": r"CaO* + Na$_2$O", "right": r"K$_2$O", "top": r"Al$_2$O$_3$"}

    # 新增：传递 matplotlib axes 对象
    tax = new_ternary_plot(tax=tax, labels=corner_labels, scale=scale, **kwargs)
    left_annotate_dict = {"Plagioclase": (0, 50, 50), "Smectite": (0, 80, 20)}
    right_annotate_dict = {"K-feldspar": (50, 50, 0), "Muscovite": (27, 73, 0),
                           "Illite": (20, 80, 0), "Kaolinite, Chlorite, Gibbsite": (0, 100, 0)}
    for key, value in left_annotate_dict.items():
        tax.annotate(key, value, fontsize=6, ha="right", va="center",color = 'g',
                     xytext=(-2, 0), textcoords="offset points")
    for key, value in right_annotate_dict.items():
        tax.annotate(key, value, fontsize=6, ha="left", va="bottom", color='g',
                     xytext=(1, 2), textcoords="offset points")


    tax.line((27, 73, 0), (17.5, 82.5, 20), linewidth=3, color="green", linestyle="-")
    tax.line((0, 82.5, 17.5), (0, 73, 27), linewidth=3, color="green", linestyle="-")

    start_point_1 = (2, 41, 57)
    end_point_1 = (1, 84, 15)
    tax.ax.annotate('', xy=rtl_to_xy(end_point_1), xytext=rtl_to_xy(start_point_1),
                    ha="center", va="top", fontsize=6,
                    arrowprops=dict(arrowstyle='-|>', color='b', linewidth=1, mutation_scale=8,
                    shrinkA=0, shrinkB=0))
    tax.annotate("average\nbasalt/gabbro", start_point_1, fontsize=6, ha='left', va='top',
                 xytext=(1, -1), textcoords="offset points")

    start_point_2 = (20, 50, 30)
    end_point_2 = (20, 78, 2)
    tax.ax.annotate('', xy=rtl_to_xy(end_point_2), xytext=rtl_to_xy(start_point_2),
                    ha="center", va="top", fontsize=6,
                    arrowprops=dict(arrowstyle='-|>', color='b', linewidth=1, mutation_scale=8,
                    shrinkA=0, shrinkB=0))
    tax.annotate("average\ngranite", start_point_2, fontsize=6, ha='left', va='top',
                 xytext=(1, -1), textcoords="offset points")

    start_point_3 = (17, 81, 2)
    end_point_3 = (1, 97, 2)
    tax.ax.annotate('', xy=rtl_to_xy(end_point_3), xytext=rtl_to_xy(start_point_3),
                    ha="center", va="top", fontsize=6,
                    arrowprops=dict(arrowstyle='-|>', color='b', linewidth=1, mutation_scale=8,
                    shrinkA=0, shrinkB=0))

    tax.ax.annotate("advanced weathering\ntrend for granite", (70, 75), color = 'b',
                 fontsize=6, ha='left', va='center')
    tax.scatter([left_annotate_dict["Plagioclase"], right_annotate_dict["K-feldspar"],
                 right_annotate_dict["Kaolinite, Chlorite, Gibbsite"]], marker='s',s=5, color="green", zorder=2)
    start_point_4 = (12.5, 50, 37.5)
    start_point_5 = (10, 50, 40)
    tax.scatter([start_point_1, start_point_2, start_point_4, start_point_5],
                s=5, color="blue", marker = 's', zorder=2)
    tax.annotate("Grd.", start_point_4, fontsize=6, ha='left', va='top',
                 xytext=(0, -1), textcoords="offset points")
    tax.annotate("Ton.", start_point_5, fontsize=6, ha='right', va='top',
                 xytext=(0, -1), textcoords="offset points")
    tax.ax.plot((70, 56), (75, 75), color = 'k', linewidth=0.5, linestyle='-')

    # 数据点绘制配置
    tax.scatter(normalized_data, s=5, c = None, color="r", zorder=3)

    # 样本标注系统
    if annotate_sample_names:
        if sample_labels is None:
            raise ValueError("启用标注时必须提供 sample_labels 参数")
        else:
            annotate_samples(ax=tax, points=normalized_data, sample_labels=sample_labels, fontsize=4, ha="left",
                             va="bottom", xytext=(2, 2))

    tax.left_corner_label(corner_labels["left"], fontsize=8, offset=0)  # 单个数值表示Y轴偏移
    tax.right_corner_label(corner_labels["right"], fontsize=8, offset=0)  # 单个数值表示Y轴偏移
    tax.right_axis_label("CIA→", fontsize=8, offset=0.2, rotation=120)
    return tax  # 返回坐标系对象便于重复使用


if __name__ == "__main__":
    """
    示例用法：
    1. 准备包含"K2O", "Al2O3", "CaO* + Na2O"列的数据集
    2. 直接调用绘图函数并保存结果
    """

    # 示例数据集（包含样本名称列）

    sample_data = pd.DataFrame(
        {"Al2O3": [20, 30], "CaO* + Na2O": [10, 20], "K2O": [70, 50], "sample": ["S1", "S2"]}
    )

    tax = cia_plot(
        data=sample_data,
        annotate_sample_names=True,
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

