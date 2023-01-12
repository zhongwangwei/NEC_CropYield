from scipy import stats
import numpy as np
import pandas as pd
import os, sys
import xarray as xr
import dask.array as da
# from dask.diagnostics import ProgressBar
from scipy.stats import linregress
from pylab import rcParams

# Syear=2015
# Eyear=2030

def first(ds,ds0):
    outputshape=(len(ds.lat),len(ds.lon))
    time={}
    time['time7']=np.full(outputshape, np.nan)
    time['time10']=np.full(outputshape, np.nan)
    time['time_10']=np.full(outputshape, np.nan)
    for i,lat in enumerate(ds.lat):
        for j,lon in enumerate(ds.lon):
            da = ds.sel(lon=[lon], lat=[lat], method="nearest")
            dm =da.where(da > 7.0, drop=True)
            Sdate = str("20150101")
            if len(dm.time) != 0:
                m0 = dm.time[0]
                a = str(m0.dt.day.values)
                if m0.dt.day.values <10:
                    a = '0'+str(m0.dt.day.values)
                Edate = str(str(m0.dt.year.values)+"0"+str(m0.dt.month.values)+a)
                # print(ds.sel(time=slice(Sdate, Edate)))
                time['time7'][i,j] = len(  ds0.sel(time=slice(Sdate, Edate)).time  )
                # print(time['time7'][i,j])
                
            dt = da.where(da > 10.0, drop=True)
            if len(dt.time) != 0:
                m1 = dt.time[0]
                b = str(m1.dt.day.values)
                if m1.dt.day.values <10:
                    b = '0'+str(m1.dt.day.values)
                Edate1 = str(str(m1.dt.year.values)+"0"+str(m1.dt.month.values)+b)
                # print(Edate1)
                time['time10'][i,j] = len(  ds0.sel(time=slice(Sdate, Edate1)).time  )
    
                m2 = dt.time[-1]
                # print(m2)
                if m2.dt.day.values <10:
                    d = '0'+str(m2.dt.day.values)
                else:
                    d = str(m2.dt.day.values)
                # print(d)
                if m2.dt.month.values <10:
                    c = '0'+str(m2.dt.month.values)
                else:
                    c = str(m2.dt.month.values)
                # print(c)
                Edate2 = str(str(m2.dt.year.values)+c+d)
                # print(Edate2)
                time['time_10'][i,j] = len( ds0.sel(time=slice(Sdate, Edate2)).time  )
    return time






if __name__=='__main__':
    import glob, os, shutil

    Pathout='/tera01/xuqch3/Dongbei/acctas/'
    ssps = ['ssp126','ssp245','ssp370','ssp585']
    # ssps = ['ssp126']
    for ssp in ssps:
        VarFile=("/tera01/xuqch3/Dongbei/%s/tas_ensmean.nc"%(ssp))
        print('>>>>',VarFile)
        with xr.open_dataset(VarFile) as ds:
            ds = ds["tas"]
            ds0=ds-273.15
            ds0 = ds0.to_dataframe()
            ds0.rolling(5,min_periods=4,center=True,axis=0,).mean()
            ds0 = ds0.to_xarray()
            ds0.to_netcdf( os.path.join(Pathout,'tas_5_ensmean_%s.nc' %(ssp) ))
            print('>> Prepared----')
            # time1 = np.arange(2016,2017)
            time1 = np.arange(2015,2101)
            # print(time1)
            outputshape=(len(time1),len(ds.lat),len(ds.lon))
            ta = xr.Dataset({
                      'ta7': (('time','lat','lon'), np.full(outputshape, np.nan)),
                      'ta10': (('time','lat','lon'), np.full(outputshape, np.nan)),
                      'te10': (('time','lat','lon'), np.full(outputshape, np.nan))
                      },
                      coords={'time': (('time'), time1),
                              'lat':(('lat'),ds.lat.values), 
                              'lon':(('lon'),ds.lon.values),
                                  })
            #-----------------------------------
            for i,year in enumerate(time1):
                print('>>>>',year)
                Sdate=str(str(year)+"0101")
                Edate=str(str(year)+"1231")
                ds1 = ds0.sel(time=slice(Sdate, Edate))
                time = first(ds1,ds0)
                # print('>>>>',time)
                ta["ta7"][i,:,:] = time['time7'][:,:]
                ta["ta10"][i,:,:] = time['time10'][:,:]
                ta["te10"][i,:,:] = time['time_10'][:,:]
                # print(ta7.time.values)
            print('------------------%s---------------------'%(ssp))
            ta.to_netcdf( os.path.join(Pathout,'Growthday_ensmean_%s.nc' %(ssp) ))
            # ta10.to_netcdf( os.path.join(Pathout,'tas_ta10_%s.nc' %(ssp) ))
            # te10.to_netcdf( os.path.join(Pathout,'tas_te10_%s.nc' %(ssp) ))
        
    print('end')
            
            
            
            
            
