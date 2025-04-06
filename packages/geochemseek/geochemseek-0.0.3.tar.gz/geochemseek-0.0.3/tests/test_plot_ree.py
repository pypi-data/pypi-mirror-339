from geochemseek.trace_element import ree
import numpy as np
import pandas as pd
import os
import sys
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
# 新增环境诊断代码
print("当前工作目录:", os.getcwd())
print("Python路径:", sys.executable)
print("文件绝对路径:", os.path.abspath('tests/Apatite_R.xlsx'))
print("环境变量:", os.environ.get('CONDA_DEFAULT_ENV') or os.environ.get('VIRTUAL_ENV'))


# 读取 excel文件
df= pd.read_excel('tests/Apatite_R.xlsx',sheet_name='Reorganized')
ree.plot_ree(df, sample_name = ['21JH171'], marker='o', color='k', markerfacecolor='r')
ree.add_Eu_anomaly_col(df)
print(df["Eu/Eu*"])

from geochemseek.geothermobarometry import calculate_zr_in_rutile_temperature

calculate_zr_in_rutile_temperature(np.array([500, 600]), mode='tomkins_alpha_quartz')
