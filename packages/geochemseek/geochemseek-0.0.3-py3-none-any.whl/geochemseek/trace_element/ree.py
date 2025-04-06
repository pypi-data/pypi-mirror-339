#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ree.py
# @Author  : Qing-Feng Mei
# @Email   : meiqingfeng@mail.iggcas.ac.cn
# @Time    : 2025/4/3 22:49
# @Project : geochemseek-project
# @Desc    : None


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple

from matplotlib.lines import Line2D


class REEConfig:
    """稀土元素分析配置参数

    Attributes:
        ELEMENTS (list): 原始稀土元素列名列表
        ELEMENTS_N (list): 标准化后稀土元素列名列表
        STANDARDS (dict): 标准化值字典，包含不同模式的标准值
        MODE_NAMES (dict): 标准化模式全称映射
    """
    ELEMENTS = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd',
                'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    ELEMENTS_N = ['La_N', 'Ce_N', 'Pr_N', 'Nd_N', 'Sm_N', 'Eu_N', 'Gd_N',
                'Tb_N', 'Dy_N', 'Ho_N', 'Er_N', 'Tm_N', 'Yb_N', 'Lu_N']

    STANDARDS = {
        # Sun and McDonough (1989)
        "CHON": pd.Series(
            [0.2370, 0.6120, 0.0950, 0.4670, 0.1530, 0.0580, 0.2055,
             0.0374, 0.2540, 0.0566, 0.1655, 0.0255, 0.1700, 0.0254],
            index=ELEMENTS
        ),
        # McDonough and Sun (1995)
        "PM": pd.Series(
            [0.648, 1.675, 0.254, 1.250, 0.406, 0.154, 0.544,
             0.099, 0.674, 0.149, 0.438, 0.068, 0.441, 0.0675],
            index=ELEMENTS
        ),
        # Sun and McDonough (1989)
        "PM1989": pd.Series(
            [0.687, 1.775, 0.276, 1.354, 0.444, 0.168, 0.596,
             0.108, 0.737, 0.164, 0.480, 0.074, 0.493, 0.074],
            index=ELEMENTS
        ),
        # Sun and McDonough (1989)
        "NMORB": pd.Series(
            [2.5, 7.5, 1.32, 7.3, 2.63, 1.02, 3.68,
             0.67, 4.55, 1.01, 2.97, 0.456, 3.05, 0.455],
            index=ELEMENTS
        )
    }

    MODE_NAMES = {
        "CHON": "chondrite",
        "PM": "primitive mantle",
        "PM1989": "primitive mantle",
        "NMORB": "NMORB"
    }

def validate_input_parameters(
    data: pd.DataFrame,
    sample: list[str] | None,
    mode: str
) -> pd.DataFrame:
    """统一验证输入参数有效性

    Args:
        data: 输入数据框
        sample: 样品名称列表
        mode: 标准化模式

    Returns:
        pd.DataFrame: 验证通过并筛选后的数据框

    Raises:
        ValueError: 当输入参数无效时
    """
    missing_elements = set(REEConfig.ELEMENTS) - set(data.columns)
    if missing_elements:
        raise ValueError(f"数据缺失必要稀土元素: {', '.join(missing_elements)}")
    if sample is not None:
        # 查找不区分大小写的列名
        sample_cols = [col for col in data.columns if col.lower().replace(' ', '') in ['group', 'subgroup',
                       'samplename', 'sampleid']]
        if not sample_cols:
            raise ValueError("筛选样品需要数据包含'group'、'subgroup'、'sample name'或'sample ID'列")
        sample_col = sample_cols[0]  # 取第一个匹配的列名
        data = data[data[sample_col].isin(sample)]
        if len(data) == 0:
            raise ValueError(f"未找到匹配样品: {', '.join(sample)}")
    if (normalized_mode := mode.upper()) not in REEConfig.STANDARDS:
        raise ValueError(f"无效标准化模式: {normalized_mode}，可用模式: {', '.join(REEConfig.STANDARDS.keys())}")
    return data

def normalize_ree(
    data: pd.DataFrame,
    sample: list[str] | None = None,
    mode: str = 'CHON'
) -> pd.DataFrame:
    """标准化稀土元素数据

    Args:
        data: 包含稀土元素含量（ppm）的原始数据
        sample: 要处理的样品名称列表，None表示处理全部样品
        mode: 标准化模式 (CHON/PM/NMORB)

    Returns:
        pd.DataFrame: 标准化后的数据框，_N后缀表示标准化后的值

    Raises:
        ValueError: 当输入参数无效时
    """
    data = validate_input_parameters(data, sample, mode)
    print(f"[INFO] 正在标准化 {len(data)} 个数据点，标准化模式: {mode.upper()}")
    normalized_values = REEConfig.STANDARDS[mode.upper()]
    normalized_data = data.copy()
    normalized_data[REEConfig.ELEMENTS_N] = data[REEConfig.ELEMENTS].div(normalized_values)
    return normalized_data


def plot_ree(
    data: pd.DataFrame,
    ax: plt.Axes = None,
    sample: list[str] | None = None,
    y_limits: Tuple[float, float] = (1, 10000),
    perform_normalization: bool = True,
    mode: str = 'CHON',
    **kwargs
) -> list[Line2D]:
    """绘制稀土元素配分模式图

    Args:
        data: 输入数据框，标准化前（ppm）或标准化后的数据
        ax: matplotlib坐标轴对象，None则创建新坐标轴
        sample: 要绘制的样品名称列表，None表示全部样品
        y_limits: Y轴范围，默认为(1, 10000)
        perform_normalization: 是否执行标准化，默认为True
        mode: 标准化模式 (CHON/PM/NMORB)
        **kwargs: 其他传递给matplotlib.plot的参数

    Raises:
        ValueError: 当输入参数无效时
    """
    data = validate_input_parameters(data, sample, mode)
    ax = ax if ax else plt.gca()
    # 数据标准化处理
    if perform_normalization:
        data = normalize_ree(data, sample=sample, mode=mode)
        data_plot = data[REEConfig.ELEMENTS_N]
    else:
        data_plot = data[REEConfig.ELEMENTS]
    # 生成绘图位置
    x_positions = np.arange(len(REEConfig.ELEMENTS))
    # 核心绘图逻辑 转置矩阵适配matplotlib格式
    print(f"[INFO] 正在绘制 {len(data)} 个数据点")
    lines: list[Line2D] = ax.plot(x_positions, data_plot.values.T, **kwargs)
    # 坐标轴设置
    ax.set_yscale('log')
    ax.set_ylim(y_limits)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(REEConfig.ELEMENTS, ha='center')
    ax.set_ylabel(f'Samples/{REEConfig.MODE_NAMES[mode.upper()]}')
    # plt.show()
    return lines

def add_Eu_anomaly_col(data: pd.DataFrame) -> pd.DataFrame:
    """计算并添加Eu异常值列

    Args:
        data: 包含Sm、Eu、Gd元素浓度的数据框

    Returns:
        pd.DataFrame: 新增'Eu/Eu*'列的数据框

    Raises:
        ValueError: 当数据缺失必要元素列时
    """
    if not all(col in data.columns for col in ['Sm', 'Eu', 'Gd']):
        raise ValueError("数据缺失必要稀土元素: ['Sm', 'Eu', 'Gd']")

    data['Eu/Eu*'] = (data['Eu']/REEConfig.STANDARDS["CHON"].loc['Eu']) / np.sqrt(
        (data['Sm']/REEConfig.STANDARDS["CHON"].loc['Sm']) *
        (data['Gd']/REEConfig.STANDARDS["CHON"].loc['Gd']))
    return data

def add_Ce_anomaly_col(data: pd.DataFrame) -> pd.DataFrame:
    """计算并添加Ce异常值列

    Args:
        data: 包含La、Ce、Pr元素浓度的数据框

    Returns:
        pd.DataFrame: 新增'Ce/Ce*'列的数据框

    Raises:
        ValueError: 当数据缺失必要元素列时
    """
    if not all(col in data.columns for col in ['La', 'Ce', 'Pr']):
        raise ValueError("数据缺失必要稀土元素: ['La', 'Ce', 'Pr']")

    data['Ce/Ce*'] = (data['Ce']/REEConfig.STANDARDS["CHON"].loc['Ce']) / np.sqrt(
        (data['La']/REEConfig.STANDARDS["CHON"].loc['La']) *
        (data['Pr']/REEConfig.STANDARDS["CHON"].loc['Pr']))
    return data

