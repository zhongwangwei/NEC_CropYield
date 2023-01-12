from ast import IsNot
from cmath import isnan
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

    path = "/tera04/zhwei/PCSE/data/output/adaptation/sowing"
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
    #names = ['soybean']

    idxs=[0,1,2]
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    #tests = ['default1','default2']
    #fnames = ['test1','test2']
    # tests = ['default3','default4']
    # fnames = ['test3', 'test4']
    #scenarios=[]
    scenarios=['default','co2','precipitation','temperature']
    scenarios=['default']
    ssps=['ssp585']
    df = pd.DataFrame()

    veg=[]
    sspx=[]
    scenariox=[]
    Yieldmean=[]
    Yieldstd=[]
    # Apr 15-->105

    default_ssp585_rice      = xr.open_dataset(f'{path}/rice_output_ssp585_sowing_Max_Yield_default.nc')["TAGP"].where(crop>-1)[0,:,:]
    default_ssp585_maize     = xr.open_dataset(f'{path}/maize_output_ssp585_sowing_Max_Yield_default.nc')["TAGP"].where(crop >-1)[0,:,:] 
    default_ssp585_soybean   = xr.open_dataset(f'{path}/soybean_output_ssp585_sowing_Max_Yield_default.nc')["TAGP"].where(crop >-1)[0,:,:] 

    rice_sowing_Max_Yield    = xr.open_dataset(f'{path}/rice_output_ssp585_sowing_Max_Yield_final.nc')["TAGP"].where(crop >-1)   / default_ssp585_rice*100.0
    maize_sowing_Max_Yield   = xr.open_dataset(f'{path}/maize_output_ssp585_sowing_Max_Yield_final.nc')["TAGP"].where(crop >-1) / default_ssp585_maize*100.0
    soybean_sowing_Max_Yield = xr.open_dataset(f'{path}/soybean_output_ssp585_sowing_Max_Yield_final.nc')["TAGP"].where(crop >-1) / default_ssp585_soybean*100.0
    Max_Yield                = rice_sowing_Max_Yield 
    crop_dis                 = rice_sowing_Max_Yield*0.0

    Max_Yield = xr.where(rice_sowing_Max_Yield<=maize_sowing_Max_Yield,maize_sowing_Max_Yield,rice_sowing_Max_Yield)
    Max_Yield = xr.where(Max_Yield<=soybean_sowing_Max_Yield,soybean_sowing_Max_Yield,Max_Yield)

    crop_dis  = xr.where(rice_sowing_Max_Yield<=maize_sowing_Max_Yield,1.0,0.0)
    crop_dis  = xr.where(Max_Yield<=soybean_sowing_Max_Yield,2.0,crop_dis)

    #crop_dis  = crop_dis['TAGP']
    #print(crop_dis)
    
    #ll=crop_dis.values

    Max_Yield = xr.where(crop_dis==0.,Max_Yield*default_ssp585_rice/100.0,Max_Yield)
    Max_Yield = xr.where(crop_dis==1.,Max_Yield*default_ssp585_maize/100.0,Max_Yield)
    Max_Yield = xr.where(crop_dis==2.,Max_Yield*default_ssp585_soybean/100.0,Max_Yield)
    Max_Yield = xr.where(Max_Yield>100.0,Max_Yield,np.nan)

    crop_dis = xr.where(Max_Yield>100.0,crop_dis,np.nan)
    Max_Yield.to_netcdf(f"{path}/../optimized/optimized_Yield.nc")
    crop_dis.to_netcdf(f"{path}/../optimized/optimized_distribution.nc")
