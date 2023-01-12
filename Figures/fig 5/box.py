import matplotlib.pyplot as plt
from email.policy import default
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

import cartopy.crs as ccrs
from pylab import rcParams
import time
import datetime

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


def box():
    # data是acc中三个箱型图的参数
    data = []
    # data2 是F1 score中三个箱型图的参数
    data2 = []
    # data3 是IoU中三个箱型图的参数
    data3 = []
    # 箱型图名称
    labels = ["default", "co2", "percipitation", "temperature"]
    # 三个箱型图的颜色 RGB （均为0~1的数据）
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    # 绘制箱型图
    # patch_artist=True-->箱型可以更换颜色，positions=(1,1.4,1.8)-->将同一组的三个箱间隔设置为0.4，widths=0.3-->每个箱宽度为0.3
    bplot = plt.boxplot(data, patch_artist=True, labels=labels, positions=(1, 1.4, 1.8, 2.2), widths=0.3)
    # 将三个箱分别上色
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    bplot2 = plt.boxplot(data2, patch_artist=True, labels=labels, positions=(2.5, 2.9, 3.3, 3.7), widths=0.3)

    for patch, color in zip(bplot2['boxes'], colors):
        patch.set_facecolor(color)

    bplot3 = plt.boxplot(data3, patch_artist=True, labels=labels, positions=(4, 4.4, 4.8, 5.2), widths=0.3)

    for patch, color in zip(bplot3['boxes'], colors):
        patch.set_facecolor(color)

    x_position = [1, 2.5, 4]
    x_position_fmt = ["acc", "F1 score", "IoU"]
    plt.xticks([i + 0.8 / 2 for i in x_position], x_position_fmt)

    plt.ylabel('percent (%)')
    plt.grid(linestyle="--", alpha=0.3)  # 绘制图中虚线 透明度0.3
    plt.legend(bplot['boxes'], labels, loc='lower right')  # 绘制表示框，右下角绘制
    plt.savefig(fname="pic.png", figsize=[10, 10])
    plt.show()


if __name__ == '__main__':
    import glob, os, shutil

    path = '/tera01/xuqch3/PCSE/sensitivity/harvest_date'
    Figout = '/tera01/xuqch3/PCSE/sensitivity/Fig/Yield_change'
    maskfile_Crop = "/tera01/xuqch3/PCSE/crop/crop.nc"  # 'F:/PCSE/crop/crop.nc'
    crop = xr.open_dataset(maskfile_Crop).crop
    '''
    rice:0, maize:1, soybean:2
    -'''
    names = ['rice', 'maize', 'soybean']
    idxs = [0, 1, 2]

    scenarios = ['default', 'co2', 'precipitation', 'temperature']
    data_crop = []
    for name, idx in zip(names, idxs):
        VarFile = f'{path}/default/{name}_output_ssp585_default.nc'
        print(VarFile)
        with xr.open_dataset(VarFile) as ds1:
            ds1 = ds1.where((ds1.time.dt.year > 2015) & (ds1.time.dt.year < 2100), drop=True)
            ds1 = ds1["TAGP"]
            ds_a1 = ds1.where(crop == idx, drop=True)
            ssp126 = ds_a1.groupby('time').mean(...)
            ssp126_land = (ssp126 - ssp126[0]) / ssp126[0] * 100
            print(f'default ' + f'{name}' + f' {idx} ' + 'SSP126 mean: ' + str(ssp126_land.mean(...).values))
            print(f'default ' + f'{name}' + f' {idx} ' + 'SSP126 std: ' + str(ssp126_land.std(...).values))

        VarFile = f'{path}/co2/{name}_output_ssp585_co2.nc'
        print(VarFile)
        with xr.open_dataset(VarFile) as ds2:
            ds2 = ds2.where((ds2.time.dt.year > 2015) & (ds2.time.dt.year < 2100), drop=True)
            ds2 = ds2["TAGP"]
            ds_a2 = ds2.where(crop == idx, drop=True)
            ssp245 = ds_a2.groupby('time').mean(...)
            ssp245_land = (ssp245 - ssp245[0]) / ssp245[0] * 100
            print(f'co2 ' + f'{name}' + f' {idx} ' + 'SSP245 mean: ' + str(ssp245_land.mean(...).values))
            print(f'co2 ' + f'{name}' + f' {idx} ' + 'SSP245 std: ' + str(ssp245_land.std(...).values))

        VarFile = f'{path}/precipitation/{name}_output_ssp585_precipitation.nc'
        print(VarFile)
        with xr.open_dataset(VarFile) as ds3:
            ds3 = ds3.where((ds3.time.dt.year > 2015) & (ds3.time.dt.year < 2100), drop=True)
            ds3 = ds3["TAGP"]
            ds_a3 = ds3.where(crop == idx, drop=True)
            ssp370 = ds_a3.groupby('time').mean(...)
            ssp370_land = (ssp370 - ssp370[0]) / ssp370[0] * 100
            print(f'precipitation ' + f'{name}' + f' {idx} ' + 'SSP370 mean: ' + str(ssp370_land.mean(...).values))
            print(f'precipitation ' + f'{name}' + f' {idx} ' + 'SSP370 std: ' + str(ssp370_land.std(...).values))

        VarFile = f'{path}/temperature/{name}_output_ssp585_temperature.nc'
        print(VarFile)
        with xr.open_dataset(VarFile) as ds4:
            ds4 = ds4.where((ds4.time.dt.year > 2015) & (ds4.time.dt.year < 2100), drop=True)
            ds4 = ds4["TAGP"]
            ds_a4 = ds4.where(crop == idx, drop=True)
            ssp585 = ds_a4.groupby('time').mean(...)
            ssp585_land = (ssp585 - ssp585[0]) / ssp585[0] * 100
            print(f'temperature ' + f'{name}' + f' {idx} ' + 'SSP585 mean: ' + str(ssp585_land.mean(...).values))
            print(f'temperature ' + f'{name}' + f' {idx} ' + 'SSP585 std: ' + str(ssp585_land.std(...).values))
            print('plotting now')

            data_crop[idx] = [[ssp126_land], [ssp245_land], [ssp370_land], [ssp585_land]]
            print(data_crop)
            exit(0)
        box()

        # ax.axhline(y=0, color='gray', linestyle='--')
        # ax.set_ylabel('Yield change (%)', fontsize=18)
        # ax.set_xlabel('Year', fontsize=20)
        # # plt.yticks(np.arange(-20, 120, 20), np.arange(-20, 120, 20))
        # # plt.yticks(np.arange(-10, 50, 10), np.arange(-10, 50, 10))
        # ax.tick_params(axis='both', top='off', labelsize=16)
        # ax.legend(loc='best', shadow=False, fontsize=12)
        # # ax.set_title('%s_%s' % (name,fnames[i]))
        # plt.tight_layout()
        # plt.savefig(f'{Figout}/{name}_output_{scenario}.eps', format='eps', dpi=800)  # timeseries_lines
        # plt.savefig(f'{Figout}/{name}_output_{scenario}.png', format='png', dpi=800)  # timeseries_lines
        # plt.show()
    #
    #     print(name)
    # print('end')
