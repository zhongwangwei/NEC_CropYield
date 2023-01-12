import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import os, sys
import xarray as xr
import dask.array as da
from dask.diagnostics import ProgressBar
from scipy.stats import linregress
# from numba import jit #  Speedup for python functions
from matplotlib import colors
import cartopy.crs as ccrs
from pylab import rcParams
import matplotlib
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import date as dt

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
          'xtick.labelsize': 12,
          'xtick.direction': 'out',
          'ytick.labelsize': 12,
          'ytick.direction': 'out',
          'savefig.bbox': 'tight',
          'axes.unicode_minus': False,
          'text.usetex': False}
rcParams.update(params)


def settime(area, ds):
    m = area
    time = ds.time
    dates = []
    for i, year in enumerate(area.time):
        t = int(area.values[i])
        Sdate = str("%s0101" % (year.values))
        a = (str(time[t].values)[0:10])
        # print(a)
        Edate = (str(year.values) + a[5:7] + a[8:10])
        # print(Edate)
        m[i] = len(time.sel(time=slice(str(Sdate), str(Edate))))  # ['time']
        # print(m[i])
        # exit(0)
    return m


if __name__ == '__main__':
    import glob, os, shutil

    ssps = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    lines = [1.5, 1.5, 1.5]
    alphas = [1., 1., 1.]
    linestyles = ['solid', 'dotted', 'dashed']
    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    time = xr.open_dataset('F:/PCSE/pcse/pr_ssp126.nc')

    maskfile_Crop = "F:/PCSE/crop/crop.nc"
    Crop = xr.open_dataset(maskfile_Crop)
    Crop_all = Crop.crop

    '''
    rice:0, maize:1, soybean:2
    '''

    pathin = 'F:/Dongbei/Growthday/'
    pathout = 'F:/Dongbei/plot/growthday/'
    # pathin = ('/tera01/xuqch3/Dongbei/pr_t/')
    for i, ssp in enumerate(ssps):
        GrowthFile = ('%s/pr_t_Growthday_%s.nc' % (pathin, ssp))
        date = xr.open_dataset(GrowthFile)
        start_date = date.strat
        crop = start_date.where(Crop_all >= 0, drop=True)

        crop_area = crop.groupby('time').mean(...)
        crop_line = settime(crop_area, time)  # translate time to length between 0101 and sowing date
        crop_line.plot.line(x='time', label=ssp, linewidth=lines[0], linestyle=linestyles[0], alpha=alphas[0],
                            color=colors[i])

    # plt.title('Crop', fontsize=18)  # , fontsize=18
    ax.legend(fontsize=18, loc=1)
    ax.legend(loc='upper right', shadow=False, fontsize=14)
    ax.set_ylabel('Sowing date (DOY) ', fontsize=18)
    ax.set_xlabel('Year', fontsize=18)
    plt.tight_layout()
    # plt.savefig('%s/crop.eps' % (pathin))
    plt.savefig('%s/Esd.png' % (pathout), dpi=900)
    plt.show()
