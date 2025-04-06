#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : spider.py
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



class TraceElementConfig:
    """微量元素分析配置参数(支持自定义元素顺序和标准化值)"""

    # 默认元素顺序(稀土元素)
    DEFAULT_ELEMENTS = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd',
                        'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    # 完整的标准化值配置(12种数据源)
    # References:
    # CHON: McDonough and Sun (1995);
    # CHON2014: Palme and O'Neill (2014);
    # PM: McDonough and Sun (1995);
    # PM2014 Palme and O'Neill (2014);
    # MORB: White and Klein (2014);
    # MORBLN: Arevalo and McDonough (2010);
    # NMORB: White and Klein (2014);
    # NMORB1989: Sun and McDonough (1989);
    # NASC: Gromet et al. (1984);
    # UCC: Rudnick and Gao (2014);
    # CC: Rudnick and Gao (2014);
    # GLOSSII: Plank (2014).”

    STANDARD_VALUES = {
        "CHON": {
            'Cs': 0.1900, 'Rb': 2.3000, 'Ba': 2.4100, 'Th': 0.0290, 'U': 0.0074,
            'K': 550, 'Nb': 0.2400, 'Ta': 0.0136, 'La': 0.2370, 'Ce': 0.6130,
            'Pb': 2.4700, 'Pr': 0.0928, 'Sr': 7.2500, 'Nd': 0.4570, 'Be': 0.0250,
            'Zr': 3.8200, 'Hf': 0.1030, 'Sm': 0.1480, 'Eu': 0.0563, 'Ti': 440,
            'Gd': 0.1990, 'Tb': 0.0361, 'Dy': 0.2460, 'Ho': 0.0546, 'Y': 1.5700,
            'Er': 0.1600, 'Tm': 0.0247, 'Yb': 0.1610, 'Lu': 0.0246, 'Li': 1.5000
        },
        "CHON2014": {
            'Cs': 0.1880, 'Rb': 2.3200, 'Ba': 2.4200, 'Th': 0.0300, 'U': 0.0081,
            'K': 546, 'Nb': 0.2830, 'Ta': 0.0150, 'La': 0.2414, 'Ce': 0.6194,
            'Pb': 2.6200, 'Pr': 0.0939, 'Sr': 7.7900, 'Nd': 0.4737, 'Be': 0.0219,
            'Zr': 3.6300, 'Hf': 0.1065, 'Sm': 0.1536, 'Eu': 0.0588, 'Ti': 447,
            'Gd': 0.2069, 'Tb': 0.0380, 'Dy': 0.2558, 'Ho': 0.0564, 'Y': 1.4600,
            'Er': 0.1655, 'Tm': 0.0261, 'Yb': 0.1687, 'Lu': 0.0250, 'Li': 1.9700
        },
        "PM": {
            'Cs': 0.0210, 'Rb': 0.6000, 'Ba': 6.6000, 'Th': 0.0795, 'U': 0.0203,
            'K': 240, 'Nb': 0.6580, 'Ta': 0.0370, 'La': 0.6480, 'Ce': 1.6750,
            'Pb': 0.1500, 'Pr': 0.2540, 'Sr': 19.9000, 'Nd': 1.2500, 'Be': 0.0680,
            'Zr': 10.5000, 'Hf': 0.2830, 'Sm': 0.4060, 'Eu': 0.1540, 'Ti': 1205,
            'Gd': 0.5440, 'Tb': 0.0990, 'Dy': 0.6740, 'Ho': 0.1490, 'Y': 4.3000,
            'Er': 0.4380, 'Tm': 0.0680, 'Yb': 0.4410, 'Lu': 0.0675, 'Li': 1.6000
        },
        "PM2014": {
            'Cs': 0.0180, 'Rb': 0.6050, 'Ba': 6.8500, 'Th': 0.0849, 'U': 0.0229,
            'K': 260, 'Nb': 0.5950, 'Ta': 0.0340, 'La': 0.6832, 'Ce': 1.7529,
            'Pb': 0.1850, 'Pr': 0.2657, 'Sr': 22.0000, 'Nd': 1.3410, 'Be': 0.0620,
            'Zr': 10.3000, 'Hf': 0.3014, 'Sm': 0.4347, 'Eu': 0.1665, 'Ti': 1265,
            'Gd': 0.5855, 'Tb': 0.1075, 'Dy': 0.7239, 'Ho': 0.1597, 'Y': 4.1300,
            'Er': 0.4684, 'Tm': 0.0738, 'Yb': 0.4774, 'Lu': 0.0708, 'Li': 1.4500
        },
        "MORB": {
            'Cs': 0.053, 'Rb': 4.050, 'Ba': 43.400, 'Th': 0.491, 'U': 0.157,
            'K': 1237, 'Nb': 6.440, 'Ta': 0.417, 'La': 4.870, 'Ce': 13.100,
            'Pb': 0.657, 'Pr': 2.080, 'Sr': 138.000, 'Nd': 10.400, 'Be': 0.640,
            'Zr': 103.000, 'Hf': 2.620, 'Sm': 3.370, 'Eu': 1.200, 'Ti': 9110,
            'Gd': 4.420, 'Tb': 0.810, 'Dy': 5.280, 'Ho': 1.140, 'Y': 32.400,
            'Er': 3.300, 'Tm': 0.490, 'Yb': 3.170, 'Lu': 0.480, 'li': 6.630
        },
        "MORBLN": {
            'Cs': 0.019, 'Rb': 1.360, 'Ba': 14.700, 'Th': 0.186, 'U': 0.068,
            'K': 857, 'Nb': 2.330, 'Ta': 0.194, 'La': 3.390, 'Ce': 10.200,
            'Pb': 0.460, 'Pr': 1.740, 'Sr': 110.000, 'Nd': 9.220, 'Be': 0.500,
            'Zr': 88.800, 'Hf': 2.360, 'Sm': 3.190, 'Eu': 1.150, 'Ti': None,
            'Gd': 4.290, 'Tb': 0.810, 'Dy': 5.270, 'Ho': 1.140, 'Y': 32.200,
            'Er': 3.310, 'Tm': 0.490, 'Yb': 3.200, 'Lu': 0.450, 'Li': 6.640
        },
        "NMORB": {
            'Cs': 0.019, 'Rb': 1.360, 'Ba': 14.700, 'Th': 0.186, 'U': 0.068,
            'K': 857, 'Nb': 2.330, 'Ta': 0.194, 'La': 3.390, 'Ce': 10.200,
            'Pb': 0.460, 'Pr': 1.740, 'Sr': 110.000, 'Nd': 9.220, 'Be': 0.500,
            'Zr': 88.800, 'Hf': 2.360, 'Sm': 3.190, 'Eu': 1.150, 'Ti': None,
            'Gd': 4.290, 'Tb': 0.810, 'Dy': 5.270, 'Ho': 1.140, 'Y': 32.200,
            'Er': 3.310, 'Tm': 0.490, 'Yb': 3.200, 'Lu': 0.450, 'Li': 6.640
        },
        "NMORB1989": {
            'Cs': 0.007, 'Rb': 0.560, 'Ba': 6.300, 'Th': 0.120, 'U': 0.047,
            'K': 600, 'Nb': 2.330, 'Ta': 0.132, 'La': 2.500, 'Ce': 7.500,
            'Pb': 0.300, 'Pr': 1.320, 'Sr': 90.000, 'Nd': 7.300, 'Be': None,
            'Zr': 74.000, 'Hf': 2.050, 'Sm': 2.630, 'Eu': 1.020, 'Ti': 7600,
            'Gd': 3.680, 'Tb': 0.670, 'Dy': 4.550, 'Ho': 1.010, 'Y': 28.000,
            'Er': 2.970, 'Tm': 0.456, 'Yb': 3.050, 'Lu': 0.455, 'Li': 4.300
        },
        "NASC": {
            'Cs': 5.16, 'Rb': 125.00, 'Ba': 636.00, 'Th': 12.30, 'U': 2.66,
            'K': 31545, 'Nb': None, 'Ta': 1.12, 'La': 31.10, 'Ce': 66.70,
            'Pb': None, 'Pr': None, 'Sr': 142.00, 'Nd': 27.40, 'Be': None,
            'Zr': 200.00, 'Hf': 6.30, 'Sm': 5.59, 'Eu': 1.18, 'Ti': 4705,
            'Gd': None, 'Tb': 0.85, 'Dy': None, 'Ho': None, 'Y': None,
            'Er': None, 'Tm': None, 'Yb': 3.06, 'Lu': 0.456, 'Li': None
        },
        "UCC": {
            'Cs': 4.90, 'Rb': 84.00, 'Ba': 628.00, 'Th': 10.50, 'U': 2.70,
            'K': 23244, 'Nb': 12.00, 'Ta': 0.90, 'La': 31.00, 'Ce': 63.00,
            'Pb': 17.00, 'Pr': 7.10, 'Sr': 320.00, 'Nd': 27.00, 'Be': 2.10,
            'Zr': 193.00, 'Hf': 5.30, 'Sm': 4.70, 'Eu': 1.00, 'Ti': 3836,
            'Gd': 4.00, 'Tb': 0.70, 'Dy': 3.90, 'Ho': 0.83, 'Y': 21.00,
            'Er': 2.30, 'Tm': 0.30, 'Yb': 2.00, 'Lu': 0.31, 'Li': 24.00
        },
        "CC": {
            'Cs': 2.00, 'Rb': 49.00, 'Ba': 456.00, 'Th': 5.60, 'U': 1.30,
            'K': 15026, 'Nb': 8.00, 'Ta': 0.70, 'La': 20.00, 'Ce': 43.00,
            'Pb': 11.00, 'Pr': 4.90, 'Sr': 320.00, 'Nd': 20.00, 'Be': 1.90,
            'Zr': 132.00, 'Hf': 3.70, 'Sm': 3.90, 'Eu': 1.10, 'Ti': 4315,
            'Gd': 3.70, 'Tb': 0.60, 'Dy': 3.60, 'Ho': 0.77, 'Y': 19.00,
            'Er': 2.10, 'Tm': 0.28, 'Yb': 1.90, 'Lu': 0.30, 'Li': 16.00
        },
        "GLOSSII": {
            'Cs': 4.9, 'Rb': 83.7, 'Ba': 786, 'Th': 8.1, 'U': 1.73,
            'K': 18345, 'Nb': 9.42, 'Ta': 0.698, 'La': 29.1, 'Ce': 57.6,
            'Pb': 21.2, 'Pr': 7.15, 'Sr': 302, 'Nd': 27.6, 'Be': 1.99,
            'Zr': 129, 'Hf': 3.42, 'Sm': 6, 'Eu': 1.37, 'Ti': 3836,
            'Gd': 5.81, 'Tb': 0.92, 'Dy': 5.43, 'Ho': 1.1, 'Y': 33.3,
            'Er': 3.09, 'Tm': None, 'Yb': 3.01, 'Lu': 0.495, 'Li': 44.8
        }
    }

    # 标准化模式显示名称映射
    MODE_NAMES = {
        "CHON": "chondrite",
        "CHON2014": "chondrite",
        "PM": "primitive mantle",
        "PM2014": "primitive mantle",
        "MORB": "global MORB mean",
        "MORBLN": "global MORB LN-mean",
        "NMORB": "N-MORB",
        "NMORB1989": "N-MORB",
        "NASC": "North American Shale Composite",
        "UCC": "upper continental crust",
        "CC": "continental crust",
        "GLOSSII": "GLOSS II"
    }

    @classmethod
    def get_standard_series(cls, mode: str, elements: list = None) -> pd.Series:
        """获取指定模式的标准化值Series"""
        elements = elements or cls.DEFAULT_ELEMENTS
        standard_dict = cls.STANDARD_VALUES.get(mode.upper(), {})
        return pd.Series([standard_dict.get(el, np.nan) for el in elements],
                         index=elements)

    @classmethod
    def get_normalized_columns(cls, elements: list = None) -> list:
        """获取标准化后的列名"""
        elements = elements or cls.DEFAULT_ELEMENTS
        return [f"{el}_N" for el in elements]

def validate_input_parameters(
        data: pd.DataFrame,
        elements: list[str],
        sample: list[str] | None,
        mode: str
) -> Tuple[pd.DataFrame, str]:  # 修改返回类型提示
    """统一验证输入参数有效性"""
    missing_elements = set(elements) - set(data.columns)
    if missing_elements:
        raise ValueError(f"数据缺失必要元素: {', '.join(missing_elements)}")
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

    # 增强模式名称模糊匹配
    normalized_mode = mode.upper().replace(' ', '').replace('_', '').replace('-', '')
    available_modes = {k.upper().replace(' ', '').replace('_', '').replace('-', ''): k
                      for k in TraceElementConfig.STANDARD_VALUES.keys()}

    if normalized_mode not in available_modes:
        raise ValueError(f"无效标准化模式: {mode}，可用模式: {', '.join(TraceElementConfig.STANDARD_VALUES.keys())}")

    return data, available_modes[normalized_mode]  # 返回元组(data, actual_mode)

def normalize_trace_elements(
        data: pd.DataFrame,
        elements: list[str] | None = None,
        sample: list[str] | None = None,
        mode: str = 'CHON'
) -> pd.DataFrame:
    """标准化微量元素数据(支持自定义元素顺序)"""
    elements = elements or TraceElementConfig.DEFAULT_ELEMENTS
    data, actual_mode = validate_input_parameters(data, elements, sample, mode)  # 解包返回值

    print(f"[INFO] 正在标准化 {len(data)} 个数据点，标准化模式: {actual_mode}")
    normalized_values = TraceElementConfig.get_standard_series(actual_mode, elements)  # 使用actual_mode
    normalized_cols = TraceElementConfig.get_normalized_columns(elements)

    normalized_data = data.copy()
    normalized_data[normalized_cols] = data[elements].div(normalized_values)
    return normalized_data

def plot_trace_elements(
        data: pd.DataFrame,
        ax: plt.Axes = None,
        elements: list[str] | None = None,
        sample: list[str] | None = None,
        y_limits: Tuple[float, float] = (1, 10000),
        perform_normalization: bool = True,
        mode: str = 'CHON',
        **kwargs
) -> list[Line2D]:
    """绘制微量元素配分模式图(支持自定义元素顺序)"""
    elements = elements or TraceElementConfig.DEFAULT_ELEMENTS
    data, actual_mode = validate_input_parameters(data, elements, sample, mode)  # 解包返回值
    ax = ax if ax else plt.gca()

    if perform_normalization:
        data = normalize_trace_elements(data, elements, sample, actual_mode)  # 使用actual_mode
        data_plot = data[TraceElementConfig.get_normalized_columns(elements)]
    else:
        data_plot = data[elements]

    x_positions = np.arange(len(elements))
    lines: list[Line2D] = ax.plot(x_positions, data_plot.values.T, **kwargs)

    ax.set_yscale('log')
    ax.set_ylim(y_limits)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(elements, ha='center')
    ax.set_ylabel(f'Samples/{TraceElementConfig.MODE_NAMES.get(actual_mode, actual_mode)}')  # 使用actual_mode
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



if __name__ == "__main__":
    # 创建测试数据
    test_data = pd.DataFrame({
        'SampleID': ['Sample1', 'Sample2'],
        'La': [10.5, 15.2],
        'Ce': [25.3, 30.1],
        'Pr': [3.2, 4.5],
        'Nd': [12.8, 18.3],
        'Sm': [3.5, 5.1],
        'Eu': [1.2, 1.8],
        'Gd': [3.8, 5.5],
        'Tb': [0.6, 0.9],
        'Dy': [3.9, 5.7],
        'Ho': [0.8, 1.2],
        'Er': [2.3, 3.4],
        'Tm': [0.3, 0.5],
        'Yb': [2.1, 3.2],
        'Lu': [0.3, 0.5]
    })

    # 测试1: 使用默认稀土元素顺序
    print("\n测试1: 默认稀土元素标准化")
    norm_data = normalize_trace_elements(test_data, mode='CHON')
    print(norm_data.head())

    # 测试2: 自定义元素顺序
    print("\n测试2: 自定义元素顺序标准化")
    custom_elements = ['Gd', 'La', 'Ce', 'Nd', 'Sm', 'Eu']
    norm_data_custom = normalize_trace_elements(test_data, elements=custom_elements, mode='PM')
    print(norm_data_custom.head())

    # 测试3: 绘图功能
    print("\n测试3: 绘制配分模式图")
    plt.figure(figsize=(10, 6))
    plot_trace_elements(test_data, mode='GLOSS-II',elements=custom_elements, marker='o', linestyle='-')
    plt.show()

