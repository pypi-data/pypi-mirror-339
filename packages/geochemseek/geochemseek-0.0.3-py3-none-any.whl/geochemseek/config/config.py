import matplotlib.pyplot as plt

def set_matplotlib_config():
    """应用 Matplotlib 全局配置"""
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica"],
        "font.size": 8,
    })

