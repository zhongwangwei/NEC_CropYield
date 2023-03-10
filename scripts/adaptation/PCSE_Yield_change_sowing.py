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

    path = "/tera04/zhwei/PCSE/data/output/adaptation/sowing/"
    #path = '/tera01/xuqch3/PCSE/sensitivity/harvest_date/sowing'
    Figout = '/tera04/zhwei/PCSE/Fig'
    maskfile_Crop = "/tera01/xuqch3/PCSE/crop/crop.nc"
    crop = xr.open_dataset(maskfile_Crop).crop
    names = ['rice', 'maize', 'soybean']


    idxs=[0,1,2]
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    # scenarios=['default','co2','precipitation','temperature']
    scenarios=['default','final','strategy']
    scenarios=['default','final']
    # ssps=['ssp126','ssp245','ssp370','ssp585']
    ssps = ['ssp585']

    df = pd.DataFrame()
    veg=[]
    sspx=[]
    scenariox=[]
    Yieldmean=[]
    Yieldstd=[]

    for scenario in scenarios:
        for name,idx in zip(names,idxs):
            default_ssp585=xr.open_dataset(f'{path}/{name}_output_ssp585_sowing_Max_Yield_default.nc')["TAGP"] 
            default_ssp585 = default_ssp585.where(crop == idx, drop=True)
            default_ssp585 = default_ssp585.groupby('year').mean(...)[0]

            VarFile = f'{path}/{name}_output_ssp585_sowing_Max_Yield_{scenario}.nc'
            print(VarFile)
            with xr.open_dataset(VarFile) as ds1:
                # ds1 = ds1.where((ds1.year > 2015), drop=True)
                ds1 = ds1["TAGP"] 
                # ds1_strategy = (ds1[:,:,:] ) / ds1[0,:,:] 
                # ds1_strategy.to_netcdf(f'{path}/{name}_output_ssp585_sowing_Max_Yield_strategy.nc')
                ds_a4 = ds1.where(crop == idx, drop=True)
                ssp585 = ds_a4.groupby('year').mean(...)
                ssp585_land = (ssp585 - default_ssp585) / default_ssp585 * 100
                print(f'{scenario} '+f'{name}'+f' {idx} '+'SSP585 mean: '+str(ssp585_land.mean(...).values))
                print(f'{scenario} '+f'{name}'+f' {idx} '+'SSP585 std: '+str(ssp585_land.std(...).values))
                veg.append(str(name))
                scenariox.append(str(scenario))
                sspx.append('ssp585')
                Yieldmean.append(ssp585_land.mean(...).values)
                Yieldstd.append(ssp585_land.std(...).values)
                # print(veg,scenario,Yieldmean,Yieldstd)


    df['veg']           =  pd.Series(veg)
    df['scenario']      =  pd.Series(scenariox)
    df['sspx']          =  pd.Series(sspx)
    df['Yieldmean']     =  pd.Series(Yieldmean)
    df['Yieldstd']      =  pd.Series(Yieldstd)
    df.to_csv('Yield_sowing.csv')
    exit()



    # pathin = "/tera01/xuqch3/PCSE/sensitivity/harvest_date"
    # Figout = '/tera01/xuqch3/PCSE/sensitivity/Fig/Yield_change/'
    # maskfile_Crop = "/tera01/xuqch3/PCSE/crop/crop.nc"
    # crop = xr.open_dataset(maskfile_Crop).crop
    # names = ['rice', 'maize', 'soybean']


    # idxs=[0,1,2]
    # # colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    # colors = ['#82B0D2', '#FFBE7A', '#FA7F6F']
    # # scenarios=['default','co2','precipitation','temperature']
    # scenarios = ['sowing', 'strategy']

    # # ssps=['ssp126','ssp245','ssp370','ssp585']
    # ssps = ['ssp585']
    # df = pd.DataFrame()

    # veg=[]
    # sspx=[]
    # scenariox=[]
    # Yieldmean=[]
    # Yieldstd=[]
   



    # for scenario in scenarios:
    #     VarFile1 = f'{pathin}/{scenario}/rice_output_ssp585_{scenario}_max.nc'
    #     print(VarFile1)
    #     with xr.open_dataset(VarFile1) as ds1:
    #         ds1 = ds1["TAGP"] 
    #         ds_a1 = ds1.where(crop == 0, drop=True)
    #         rice = ds_a1.groupby('year').mean(...)
    #         rice_land = (rice - rice[0]) / rice[0] * 100
    #         print(f'{scenario} '+'rice mean: '+str(rice_land.mean(...).values))
    #         print(f'{scenario} '+'rice std: '+str(rice_land.std(...).values))

    #     VarFile2 = f'{pathin}/{scenario}/maize_output_ssp585_{scenario}_max.nc'
    #     print(VarFile2)
    #     with xr.open_dataset(VarFile2) as ds2:
    #         ds2 = ds2["TAGP"] 
    #         ds_a2 = ds2.where(crop == 0, drop=True)
    #         maize = ds_a2.groupby('year').mean(...)
    #         maize_land = (maize - maize[0]) / maize[0] * 100
    #         print(f'{scenario} '+'maize mean: '+str(maize_land.mean(...).values))
    #         print(f'{scenario} '+'maize std: '+str(maize_land.std(...).values))

    #     VarFile3 = f'{pathin}/{scenario}/soybean_output_ssp585_{scenario}_max.nc'
    #     print(VarFile3)
    #     with xr.open_dataset(VarFile3) as ds3:
    #         ds3 = ds3["TAGP"] 
    #         ds_a3 = ds3.where(crop == 0, drop=True)
    #         soybean = ds_a3.groupby('year').mean(...)
    #         soybean_land = (soybean - soybean[0]) / soybean[0] * 100
    #         print(f'{scenario} '+'soybean mean: '+str(soybean_land.mean(...).values))
    #         print(f'{scenario} '+'soybean std: '+str(soybean_land.std(...).values))

    #     print('plotting now')
    #     markers = ['*', 'x', '+']
    #     lines = [1.5, 1.5, 1.5, 1.5]
    #     alphas = [1., 1., 1., 1.]
    #     linestyles = ['solid', 'solid', 'solid', 'solid', 'dotted', 'dashed', 'dashdot', 'solid', 'solid']
    #     fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    #     rice_land.plot.line(x='year', label='Rice', linewidth=lines[1], linestyle=linestyles[1],
    #                           alpha=alphas[1], color=colors[0])  # ,color = 'blue'
    #     maize_land.plot.line(x='year', label='Maize', linewidth=lines[2], linestyle=linestyles[2],
    #                           alpha=alphas[2], color=colors[1])  # ,color = 'green
    #     soybean_land.plot.line(x='year', label='Soybean', linewidth=lines[0], linestyle=linestyles[0],
    #                           alpha=alphas[0], color=colors[2])  # ,color = 'orangered'


    #     ax.axhline(y=0, color='gray', linestyle='--')
    #     ax.set_ylabel('Yield change (%)', fontsize=18)
    #     ax.set_xlabel('Year', fontsize=20)
    #     ax.tick_params(axis='both', top='off', labelsize=16)
    #     ax.legend(loc='best', shadow=False, fontsize=12)
    #     #ax.set_title('%s_%s' % (name,fnames[i]))
    #     plt.tight_layout()
    #     plt.savefig(f'{Figout}/{scenario}_ssp585_output_Yield_change.eps', format='eps', dpi=600)  # timeseries_lines
    #     plt.savefig(f'{Figout}/{scenario}_ssp585_output_Yield_change.png', format='png', dpi=600)  # timeseries_lines
    #     # print(name)
    # print('plot end')