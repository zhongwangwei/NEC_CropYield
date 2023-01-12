import matplotlib.pylab as plt
import matplotlib
import numpy as np
from pylab import rcParams
import pandas as pd

font = {'family': 'Times New Roman'}
# font = {'family' : 'Myriad Pro'}
matplotlib.rc('font', **font)

params = {'backend': 'ps',
          'axes.labelsize': 12,
          'grid.linewidth': 0.2,
          'font.size': 15,
          'legend.fontsize': 12,
          'legend.frameon': False,
          'xtick.labelsize': 8,
          'xtick.direction': 'out',
          'ytick.labelsize': 12,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          'text.usetex': False}
rcParams.update(params)
# 绘制误差棒图


df = pd.read_excel("F:/PCSE/code/scripts/analysis_plotting/Yield.xlsx", sheet_name='soybean')
mean = np.array(df['Yieldmean'])
error = np.array(df['Yieldstd'])
# x_label = np.array(df['sspx'])
crop = np.array(df['veg'])
scenario = np.array(df['scenario'])
print(crop[0], scenario[0])
# print(x_label)
# exit(0)
x_label = ['', 'ssp126', '', 'ssp245', '', 'ssp370', '', 'ssp585', '']
x_position = [1, 2, 3, 4, 5, 6, 7, 8, 9]
colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
fig = plt.figure(figsize=(6, 4))
plt.errorbar(x_position[1], mean[0], yerr=error[0], ecolor="k", elinewidth=2.5, marker="s", mfc=colors[0],
             mec=colors[0], mew=2.5, ms=20, alpha=1, capsize=5, capthick=5, linestyle="none")  # , label="Observation"
plt.errorbar(x_position[3], mean[1], yerr=error[1], ecolor="k", elinewidth=2.5, marker="s", mfc=colors[1],
             mec=colors[1], mew=2.5, ms=20, alpha=1, capsize=5, capthick=3, linestyle="none")  # , label="Observation"
plt.errorbar(x_position[5], mean[2], yerr=error[2], ecolor="k", elinewidth=2.5, marker="s", mfc=colors[2],
             mec=colors[2], mew=2.5, ms=20, alpha=1, capsize=5, capthick=3, linestyle="none")  # , label="Observation"
plt.errorbar(x_position[7], mean[3], yerr=error[3], ecolor="k", elinewidth=2.5, marker="s", mfc=colors[3],
             mec=colors[3], mew=2.5, ms=20, alpha=1, capsize=5, capthick=3, linestyle="none")  # , label="Observation"
# plt.errorbar(x_position[7], mean[3], yerr=error[3], ecolor="k", elinewidth=2.5, marker="s", mfc=colors[3],
#              mec="k", mew=2.5, ms=20, alpha=1, capsize=5, capthick=3, linestyle="none")  # , label="Observation"
plt.yticks(np.arange(-10, 50, 10), np.arange(-10, 50, 10), fontsize=20)  # soybean
# plt.yticks(np.arange(0, 80, 20), np.arange(0, 80, 20), fontsize=20)  # rice
# plt.yticks(np.arange(-30, 60, 20), np.arange(-30, 60, 20), fontsize=20)  # maize
plt.xticks([i for i in x_position], x_label, fontsize=22)
# plt.ylabel('%s' % (crop[0]), fontsize=18)
# plt.grid(linestyle="--")  # 绘制图中虚线 透明度0.3
# fig = plt.gcf()
plt.savefig('%s_%s.eps' % (scenario[0], crop[0]), format='eps', dpi=800)
plt.savefig('%s_%s.png' % (scenario[0], crop[0]), format='png', dpi=800)
plt.show()
plt.close()
