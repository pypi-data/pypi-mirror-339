import numpy as np


def calculate_zr_in_rutile_temperature(
    zr_ppm: np.ndarray, pressure_kbar: float = 10, mode: str = "tomkins_alpha_quartz"
) -> np.ndarray:
    """根据金红石中Zr含量计算形成温度（压力校正版）

    Args:
        zr_ppm (np.ndarray): 金红石中Zr含量(ppm)，支持标量或数组输入
        pressure_kbar (float): 压力值(单位kbar)，范围建议0-30kbar
        mode (str, optional): 温度计模型，可选模型包括：
            - 'tomkins_alpha_quartz': α石英稳定域模型（默认）
            - 'tomkins_beta_quartz': β石英稳定域模型
            - 'tomkins_coesite': 柯石英稳定域模型
            - 'watson': Watson et al. (2006)公式
            - 'zack': Zack et al. (2004)经验公式

    Returns:
        np.ndarray: 温度值数组(单位°C)，与输入zr_ppm维度一致

    Raises:
        ValueError: 当输入参数不合法时抛出
        TypeError: 当输入类型错误时抛出

    References:
        - Tomkins模型采用反温度计公式 T(℃) = [(a + b·P) / (c - R·ln(Zr))] - 273
          其中，P为压力值，单位为kbar，T为温度值，单位为℃，Zr为金红石含量，单位为ppm，
          R为气体常数，单位为kJ/mol/K。 (Tomkins et al., 2007)
          alpha石英域参数：a=83.9, b=0.410, c=0.1428
          beta石英域参数：a=85.7, b=0.473, c=0.1453
          柯石英域参数：a=88.1, b=0.206, c=0.1412
        - Watson模型：T(℃) = 4470/(7.36 - log10(Zr)) - 273 (Watson et al., 2006)
        - Zack模型：T(℃) = 134.7·ln(Zr) - 25 (Zack et al., 2004)

    Examples:
        >>> calculate_zr_in_rutile_temperature(np.array([20, 50]), 10)
        array([...])
    """
    # 参数校验
    if not isinstance(zr_ppm, np.ndarray):
        raise TypeError("输入必须为numpy数组，请使用np.array()转换")
    if np.any(zr_ppm <= 0):
        raise ValueError("Zr含量必须为正值，检测到非正值输入")
    if pressure_kbar <= 0:
        raise ValueError("压力值必须大于0（单位：kbar）")

    valid_modes = (
        "tomkins_alpha_quartz",
        "tomkins_beta_quartz",
        "tomkins_coesite",
        "watson",
        "zack",
    )
    if mode.lower() not in valid_modes:
        raise ValueError(f"无效模型选择，可选: {', '.join(valid_modes)}")

    gas_constant = 0.0083144  # 气体常数 (kJ/mol/K)

    # 根据不同模型选择计算公式（优化判断顺序）
    if mode.lower() == "tomkins_alpha_quartz":  # 高频场景优先判断
        constant_a, constant_b, constant_c = 83.9, 0.410, 0.1428
    elif mode.lower() == "tomkins_beta_quartz":
        constant_a, constant_b, constant_c = 85.7, 0.473, 0.1453
    elif mode.lower() == "tomkins_coesite":
        constant_a, constant_b, constant_c = 88.1, 0.206, 0.1412
    elif mode.lower() == "watson":
        temperature = 4470 / (7.36 - np.log10(zr_ppm)) - 273
        return temperature
    elif mode.lower() == "zack":
        temperature = 134.7 * np.log(zr_ppm) - 25
        return temperature
    # 合并Tomkins系列的温度计算
    temperature = (constant_a + constant_b * pressure_kbar) / (
        constant_c - gas_constant * np.log(zr_ppm)) - 273

    return temperature
