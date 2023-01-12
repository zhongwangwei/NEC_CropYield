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


### Plot settings
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

if __name__ == '__main__':
    import glob, os, shutil

    path = "/tera04/zhwei/PCSE/data/output/sensitivity/"
    Figout = '/tera04/zhwei/PCSE/Fig/'
    maskfile_Crop = "/tera04/zhwei/PCSE/data/crop_distribution/crop.nc"
    crop = xr.open_dataset(maskfile_Crop).crop
    '''
    rice:0, maize:1, soybean:2
    -'''

    # Vars = ['DVS', 'LAI', 'RD', 'SM', 'TAGP', 'TRA', 'TWLV', 'TWRT', 'TWSO', 'TWST', 'WWLOW']
    # Co = ['', '', '(kg/ha)', '(kg/ha)', '(kg/ha)', '(kg/ha)', '(kg/ha)', '(cm/day)', '(cm)', '', '(cm)']
    # Vars = ['TAGP']
    # Co = ['(kg/ha)']
    #colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    names = ['rice', 'maize', 'soybean']
    idxs=[0,1,2]
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    #tests = ['default1','default2']
    #fnames = ['test1','test2']
    # tests = ['default3','default4']
    # fnames = ['test3', 'test4']
    scenarios=['default','temperature','precipitation','co2']
    #scenarios=['tas']
    for scenario in scenarios:
        for name,idx,colr in zip(names,idxs,colors):
            t0 = time.strftime('%H:%M:%S')
            VarFile = f'{path}/{scenario}/{name}_output_ssp126_{scenario}.nc'
            print(VarFile)
            with xr.open_dataset(VarFile) as ds1:  
                ds1 = ds1.where((ds1.time.dt.month==8)&(ds1.time.dt.day==23)&(ds1.time.dt.year > 2015)&(ds1.time.dt.year < 2100), drop=True)
                ds1 = ds1["TAGP"]
                ds_a1 = ds1.where(crop == idx, drop=True)
                ssp126 = ds_a1.groupby('time').mean(...)
                ssp126_land = (ssp126 - ssp126[0]) / ssp126[0] * 100

            VarFile = f'{path}/{scenario}/{name}_output_ssp245_{scenario}.nc'
            print(VarFile)
            with xr.open_dataset(VarFile) as ds2:
                ds2 = ds2.where((ds2.time.dt.month==8)&(ds2.time.dt.day==23)&(ds2.time.dt.year > 2015)&(ds2.time.dt.year < 2100), drop=True)
                ds2 = ds2["TAGP"]
                ds_a2 = ds2.where(crop == idx, drop=True)
                ssp245 = ds_a2.groupby('time').mean(...)
                ssp245_land = (ssp245 - ssp245[0]) / ssp245[0] * 100

            VarFile = f'{path}/{scenario}/{name}_output_ssp370_{scenario}.nc'
            print(VarFile)
            with xr.open_dataset(VarFile) as ds3:
                ds3 = ds3.where((ds3.time.dt.month==8)&(ds3.time.dt.day==23)&(ds3.time.dt.year > 2015)&(ds3.time.dt.year < 2100), drop=True)
                ds3 = ds3["TAGP"]
                ds_a3 = ds3.where(crop == idx, drop=True)
                ssp370 = ds_a3.groupby('time').mean(...)
                ssp370_land = (ssp370 - ssp370[0]) / ssp370[0] * 100

            VarFile = f'{path}/{scenario}/{name}_output_ssp585_{scenario}.nc'
            print(VarFile)
            with xr.open_dataset(VarFile) as ds4:
                ds4 = ds4.where((ds4.time.dt.month==8)&(ds4.time.dt.day==23)&(ds4.time.dt.year > 2015)&(ds4.time.dt.year < 2100), drop=True)
                ds4 = ds4["TAGP"]
                ds_a4 = ds4.where(crop == idx, drop=True)
                ssp585 = ds_a4.groupby('time').mean(...)
                ssp585_land = (ssp585 - ssp585[0]) / ssp585[0] * 100
            print('plotting now')
            # ds_line5 =np.zeros(86).to_array()
            markers = ['*', 'x', '+']
            lines = [1.5, 1.5, 1.5, 1.5]
            alphas = [1., 1., 1., 1.]
            linestyles = ['solid', 'solid', 'solid', 'solid', 'dotted', 'dashed', 'dashdot', 'solid', 'solid']
            fig, ax = plt.subplots(1, 1, figsize=(10, 5))
            ssp126_land.plot.line(x='time', label='ssp126', linewidth=lines[1], linestyle=linestyles[1],
                                  alpha=alphas[1], color=colors[0])  # ,color = 'blue'
            ssp245_land.plot.line(x='time', label='ssp245', linewidth=lines[2], linestyle=linestyles[2],
                                  alpha=alphas[2], color=colors[1])  # ,color = 'green
            ssp370_land.plot.line(x='time', label='ssp370', linewidth=lines[0], linestyle=linestyles[0],
                                  alpha=alphas[0], color=colors[2])  # ,color = 'orangered'
            ssp585_land.plot.line(x='time', label='ssp585', linewidth=lines[3], linestyle=linestyles[3],
                                  alpha=alphas[3], color=colors[3])  # ,color = 'red'

            ax.axhline(y=0, color='gray', linestyle='--')
            ax.set_ylabel('TAGP change (%)', fontsize=18)
            ax.set_xlabel('Year', fontsize=20)
            plt.yticks(np.arange(-80, 60, 20), np.arange(-80, 60, 20))
            # plt.yticks(np.arange(-10, 50, 10), np.arange(-10, 50, 10))
            ax.tick_params(axis='both', top='off', labelsize=16)
            ax.legend(loc='best', shadow=False, fontsize=12)
            #ax.set_title('%s_%s' % (name,fnames[i]))
            plt.tight_layout()
            plt.savefig(f'{Figout}/{name}_output_{scenario}.png', dpi=600)  # timeseries_lines
            plt.show()

            t1 = time.strftime('%H:%M:%S')
            start_date = t0
            end_date = t1
            start_time = datetime.datetime.strptime(start_date, '%H:%M:%S')
            end_time = datetime.datetime.strptime(end_date, '%H:%M:%S')
            during_time = end_time - start_time
            print(during_time)
        print(name)
    print('end')

