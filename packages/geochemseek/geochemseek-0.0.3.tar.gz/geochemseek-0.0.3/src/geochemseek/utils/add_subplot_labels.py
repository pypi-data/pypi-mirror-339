def add_subplot_labels(
    axes, positions="upper left", fontsize=8, color="black", bbox=None, **kwargs
):  # 修改默认值为None
    """
    为子图添加(a)/(b)/(c)格式的标签

    参数：
    axes - matplotlib的axes数组
    positions - 标签位置（支持 'upper left' 或 'upper right'）
    fontsize - 标签字体大小
    color - 标签文字颜色
    bbox - 文字背景框参数（默认使用透明无边框配置）
    **kwargs - 传递给text()的额外参数，如fontweight、fontstyle等
    """
    # 设置安全的默认配置
    if bbox is None:
        bbox = dict(facecolor="none", edgecolor="none", pad=0)  # 在函数内部创建字典

    loc_dict = {
        "upper left": {"x": 0.05, "y": 0.95, "ha": "left", "va": "top"},
        "upper right": {"x": 0.95, "y": 0.95, "ha": "right", "va": "top"},
        "lower left": {"x": 0.05, "y": 0.05, "ha": "left", "va": "bottom"},
        "lower right": {"x": 0.95, "y": 0.05, "ha": "right", "va": "bottom"},
    }

    for i, ax in enumerate(axes.flat):
        label = f"({chr(97 + i)})"
        pos = loc_dict.get(positions, loc_dict["upper left"])
        ax.text(
            pos["x"],
            pos["y"],
            label,
            transform=ax.transAxes,
            fontsize=fontsize,
            color=color,
            ha=pos["ha"],  # 新增水平对齐参数
            va=pos["va"],  # 新增垂直对齐参数
            bbox=bbox.copy() if bbox else None,
            **kwargs,
        )  # 添加保护性复制


# 测试代码
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # 创建测试数据
    x = np.linspace(0, 2 * np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 创建子图
    fig, axs = plt.subplots(1, 2, figsize=(7, 3))

    # 绘制数据
    axs[0].plot(x, y1)
    axs[0].set_title("Sine Wave")

    axs[1].plot(x, y2)
    axs[1].set_title("Cosine Wave")

    # 添加子图标签（带背景框的示例）
    add_subplot_labels(axs, fontweight="bold")

    plt.tight_layout()
    plt.show()
