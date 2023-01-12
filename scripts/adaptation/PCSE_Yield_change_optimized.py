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
    df = pd.DataFrame()

    veg=[]
    sspx=[]
    scenariox=[]
    Yieldmean=[]
    Yieldstd=[]

    #===================================
    # optimized_Yield change
    optimized_distribution = "/tera04/zhwei/PCSE/data/output/adaptation/optimized/optimized_distribution.nc"
    names = ['rice', 'maize', 'soybean']
    idxs=[0.0,1.0,2.0]
    
    path = "/tera04/zhwei/PCSE/data/output/adaptation/sowing"
    maskfile_Crop = "/tera04/zhwei/PCSE/data/crop_distribution/crop.nc"
    crop = xr.open_dataset(maskfile_Crop).crop

    for name,idx in zip(names,idxs):
   
        #print(default_ssp585)
        scenario='optimized'

        VarFile = f"/tera04/zhwei/PCSE/data/output/adaptation/optimized/optimized_Yield.nc"
        distribution = xr.open_dataset(optimized_distribution).TAGP

        default_ssp585 = xr.open_dataset(f'{path}/{name}_output_ssp585_sowing_Max_Yield_default.nc')["TAGP"] 
        default_ssp585 = default_ssp585.where(distribution == idx)[0,:,:]
        default_ssp585 = default_ssp585.mean(...)

        with xr.open_dataset(VarFile) as ds1:
            ds1 = ds1["TAGP"] 
            ds_a4 = ds1.where(distribution == idx)
            ssp585 = ds_a4.groupby('year').mean(...)

            ssp585_land = (ssp585 - default_ssp585) / default_ssp585 * 100
            #print(ssp585_land)
            print(f'{scenario} '+f'{name}'+f' {idx} '+'SSP585 mean: '+ str(ssp585_land.mean(...).values))
            print(f'{scenario} '+f'{name}'+f' {idx} '+'SSP585 std: ' + str(ssp585_land.std(...).values))
            veg.append(str(name))
            scenariox.append(str(scenario))
            sspx.append('ssp585')
            Yieldmean.append(ssp585_land.mean(...).values)
            Yieldstd.append(ssp585_land.std(...).values)
            #print(veg,scenario,Yieldmean,Yieldstd)


    df['veg']           =  pd.Series(veg)
    df['scenario']      =  pd.Series(scenariox)
    df['sspx']          =  pd.Series(sspx)
    df['Yieldmean']     =  pd.Series(Yieldmean)
    df['Yieldstd']      =  pd.Series(Yieldstd)
    df.to_csv('Yield_sowing.csv')
    exit()




   



