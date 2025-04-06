import pandas as pd
def annotate_samples(ax, points, sample_labels, fontsize=4, ha="left", va="bottom", xytext=(2, 2), **kwargs):
    """
    通用样本标注函数（支持x-y图和三元图）

    参数:
        ax: 坐标系对象 (matplotlib axes 或 ternary 坐标系)
        points: 数据点坐标列表，格式根据坐标系类型确定：
                - 三元图: [(a1,b1,c1), (a2,b2,c2), ...]
                - x-y图: [(x1,y1), (x2,y2), ...]
        sample_labels: 样本标签列表
        fontsize: 标签字体大小，默认4
        ha: 水平对齐方式，默认'left'
        va: 垂直对齐方式，默认'bottom'
        xytext: 文本偏移量，默认(2, 2)
    """
    # 类型校验
    if not isinstance(sample_labels, (list, pd.Series)):
        raise TypeError("labels 必须是 list 或 pandas Series")

    # 统一转换为list
    label_list = sample_labels.tolist() if isinstance(sample_labels, pd.Series) else sample_labels

    # 长度校验
    if len(label_list) != len(points):
        raise ValueError(
            f"标签数量({len(label_list)})与数据点数量({len(points)})不匹配"
        )

    # 添加标注
    for i, point in enumerate(points):
        ax.annotate(
            label_list[i],
            point,
            fontsize=fontsize,
            ha=ha,
            va=va,
            xytext=xytext,
            textcoords="offset points",
            **kwargs
        )
