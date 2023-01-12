import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from pylab import rcParams
import pandas as pd

## Plot settings
font = {'family': 'Times New Roman'}
matplotlib.rc('font', **font)

params = {'backend': 'ps',
          'axes.labelsize': 12,
          'grid.linewidth': 0.2,
          'font.size': 15,
          'legend.fontsize': 12,
          'legend.frameon': False,
          'xtick.labelsize': 10,
          'xtick.direction': 'out',
          'ytick.labelsize': 10,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          'text.usetex': False}
rcParams.update(params)

Figout = "./"
df_default = pd.read_excel("F:/PCSE/code/scripts/analysis_plotting/Yield_sowing.xlsx", sheet_name='Sheet1')
default_mean = np.array(df_default['Yieldmean'])
default_error = np.array(df_default['Yieldstd'])
x_label = np.array(df_default['sspx'])
crop = np.array(df_default['veg'])
scenario_d = np.array(df_default['scenario'])[0]
print(scenario_d)

df_sowing = pd.read_excel("F:/PCSE/code/scripts/analysis_plotting/Yield_sowing.xlsx", sheet_name='Sheet2')
sowing_mean = np.array(df_sowing['Yieldmean'])
sowing_error = np.array(df_sowing['Yieldstd'])
scenario_s = np.array(df_sowing['scenario'])[0]
print(scenario_s)

df_strategy = pd.read_excel("F:/PCSE/code/scripts/analysis_plotting/Yield_sowing.xlsx", sheet_name='Sheet3')
strategy_mean = np.array(df_strategy['Yieldmean'])
strategy_error = np.array(df_strategy['Yieldstd'])
scenario_o = np.array(df_strategy['scenario'])[0]
print(scenario_o)

labels = ['Rice', 'Maize', 'Soybean']
x = np.arange(len(labels)) * 1.5  # 标签位置
width = 0.35
# colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']  ##蓝，绿，黄，红
colors = ['#82B0D2', '#FFBE7A', '#FA7F6F']
fig, ax = plt.subplots(1, 1, figsize=(9, 5))

rects1 = ax.bar(x - width * 1.1, default_mean, width, label=scenario_d, yerr=default_error, edgecolor='k',
                error_kw={'ecolor': 'k', 'capsize': 8}, color=colors[0])
rects2 = ax.bar(x, sowing_mean, width, label='Sowing date optimize', yerr=sowing_error, edgecolor='k',
                error_kw={'ecolor': 'k', 'capsize': 8}, color=colors[1])
rects3 = ax.bar(x + width * 1.1, strategy_mean, width, label='Sowing date optimize \n and crop relocation', yerr=strategy_error, edgecolor='k',
                error_kw={'ecolor': 'k', 'capsize': 8}, color=colors[2])

# plt.figure(figsize=(10, 5))
ax.set_ylabel('Yield Change (%)', fontsize=20)
# ax.set_xlabel('Area', fontsize=12)
# ax.set_title('这里是标题')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=18)
ax.set_yticks(np.arange(-20,100,20))
ax.set_yticklabels(np.arange(-20,100,20),fontsize=16)
ax.legend(loc='best', shadow=False, fontsize=17)
fig.tight_layout()
plt.savefig('%sYield_change_barplot.eps' % (Figout), dpi=800)
plt.savefig('%sYield_change_barplot.png' % (Figout), dpi=800)
plt.show()
