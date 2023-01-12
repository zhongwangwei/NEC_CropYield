import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from joblib import Parallel, delayed
import multiprocessing
from pylab import rcParams

font = {'family': 'DejaVu Sans'}
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


def density(default, co2, precipitation, temperature, Figout, name):
    fig = plt.figure(figsize=(10, 10))

    labels = ["default", "co2", "precipitation", "temperature"]
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']

    # sns.kdeplot(default, bw=.2, label=labels[0])
    # sns.kdeplot(data=tips, x="total_bill")
    sns.kdeplot(default, hue=f'{name}', label=labels[0], shade=True, colors=colors[0])
    sns.kdeplot(co2, label=labels[1], shade=True, colors=colors[1])
    sns.kdeplot(precipitation, label=labels[2], shade=True, colors=colors[2])
    sns.kdeplot(temperature, label=labels[3], shade=True, colors=colors[3])

    plt.ylabel('Density', fontsize=14)
    plt.xlabel('TAGP Change (%)', fontsize=14)
    plt.legend(loc='best')  # 绘制表示框，右下角绘制
    plt.savefig(f'{Figout}/TAGP_change_density.eps', format='eps', dpi=800)  # timeseries_lines
    plt.savefig(f'{Figout}/TAGP_change_density.png', format='png', dpi=800)  # timeseries_lines
    # plt.show()


def save_data(path, name, ssp, i, scenario):
    print(scenario)
    VarFile = f'{path}/{scenario}/{name}_output_{ssp}_{scenario}.nc'
    print(VarFile)
    with xr.open_dataset(VarFile) as ds1:
        ds1 = ds1.where(
            (ds1.time.dt.month > 4) & (ds1.time.dt.month < 12) & (ds1.time.dt.year > 2015) & (ds1.time.dt.year < 2100),
            drop=True)
        ds1 = ds1["Yield change (%)"]
        ds_a1 = ds1.where(crop == i, drop=True)
        ssp126 = ds_a1.groupby("time.year").max("time")
        default_land = (ssp126 - ssp126[0]) / ssp126[0] * 100

    return default_land


if __name__ == '__main__':
    import glob, os, shutil

    # path = '/tera01/xuqch3/PCSE/sensitivity/harvest_date'
    path = "/tera04/zhwei/PCSE/data/output/sensitivity"
    Figout = '/tera01/xuqch3/PCSE/sensitivity/Fig'
    maskfile_Crop = "/tera01/xuqch3/PCSE/crop/crop.nc"  # 'F:/PCSE/crop/crop.nc'
    crop = xr.open_dataset(maskfile_Crop).crop
    # ssps = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    ssps = ['ssp585']
    names = ['rice', 'maize', 'soybean']
    idx = [0, 1, 2]

    scenarios = ['default', 'co2', 'precipitation', 'temperature']
    # data_crop = np.empty((3, 4, 84))

    max_cpu = os.cpu_count()  ##用来计算现在可以获得多少cpu核心。 也可以用multipocessing.cpu_count()
    num_cores = multiprocessing.cpu_count()
    for i, name in enumerate(names):
        default = Parallel(n_jobs=num_cores)(delayed(save_data)(path, name, ssp, i, "default") for ssp in ssps)
        co2 = Parallel(n_jobs=num_cores)(delayed(save_data)(path, name, ssp, i, "co2") for ssp in ssps)
        precipitation = Parallel(n_jobs=num_cores)(
            delayed(save_data)(path, name, ssp, i, "precipitation") for ssp in ssps)
        temperature = Parallel(n_jobs=num_cores)(delayed(save_data)(path, name, ssp, i, "temperature") for ssp in ssps)
        print("ploting now")
        density(default[0], co2[0], precipitation[0], temperature[0], Figout, name)
