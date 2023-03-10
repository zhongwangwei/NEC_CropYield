import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import xarray as xr
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from pylab import rcParams
import matplotlib
import matplotlib as mpl
from cmcrameri import cm
# import cmaps
import math

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
fname = 'F:/Dongbei/plot/crop_trend/NEshp/NE.shp'
maskfile_Crop = "F:/PCSE/crop/crop.nc"
crop = xr.open_dataset(maskfile_Crop).crop



def plot_trend(varpath, Varout, tittle, i, name):
    fig = plt.figure()  # figsize=(5, 5)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                   ccrs.PlateCarree(), facecolor='none')
    ds1 = xr.open_dataset('%s' % (varpath))
    ds1['trend'] = ds1.Esd
    lats = ds1.variables['lat'][:]
    lons = ds1.variables['lon'][:]
    ds_a1 = ds1.where(crop == i).squeeze()
    m = ds_a1.trend.values.reshape(-1)[~np.isnan(ds_a1.trend.values.reshape(-1))]
    print(math.floor(min(m)), math.ceil(max(m)))
    lons2d, lats2d = np.meshgrid(lons, lats)
    p1 = plt.scatter(lons2d[0, 0], lats2d[0, 0], marker='o', color='w', label=f'{name}', s=10)
    plt.legend(loc='upper right', fontsize=20)

    # bins = np.arange(-3, 3.1, 0.2)
    # bins = np.arange(math.ceil(max(m)) * -1, math.ceil(max(m)) + 1, 0.1)
    # print(min(m),max(m))
    # bins = np.arange(-0.4, -0.3+0.00025, 0.00025)
    bins = np.arange(-0.4, -0.28+0.0005, 0.0005)
    nbin = len(bins) - 1
    mmap=cm.davos
    cmap4 = mpl.cm.get_cmap(mmap, nbin)  # coolwarm/twilight_shifted???cm.batlow,davos,bamko,broc
    norm4 = mpl.colors.BoundaryNorm(bins, nbin)
    locator = mpl.ticker.MultipleLocator(0.02)
    im2 = mpl.cm.ScalarMappable(norm=norm4, cmap=cmap4)
    im1 = ax.scatter(lons2d, lats2d, c=ds_a1['trend'].values, s=10.0, alpha=1.0, zorder=2, marker='o',
                     transform=ccrs.PlateCarree(), cmap=cmap4, norm=norm4)  # Paired/magma/plasma/GnBu/YlGn

    ax.set_extent([118, 136, 38, 55])
    ax.set_xticks([120, 125, 130, 135], crs=ccrs.PlateCarree())
    ax.set_yticks([40, 45, 50, 55], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.tick_params(labelsize=18)
    # cbar = fig.colorbar(im1, ax=ax,ticks=locator)
    # cbar.ax.tick_params(labelsize=20)
    # ax.set_title('%s' % (tittle), fontsize=12)
    ax.add_feature(shape_feature)
    plt.tight_layout()
    # plt.savefig('%s.eps' % (Varout), format='eps', dpi=800)
    plt.savefig('%s.png' % (Varout), format='png', dpi=800)
    plt.show()
    plt.close()



if __name__ == '__main__':
    import glob, os, shutil

    pathin = "C:/Users/Administrator/Desktop/PCSE/fig S2/"
    pathout = 'C:/Users/Administrator/Desktop/PCSE/fig S2/'

    names = ['Rice', 'Maize', 'Soybean']

    for i, name in enumerate(names):
        print('>>', name)
        VarFile = f'{pathin}/Esd_trend.nc'
        Varout = f'{pathout}/Esd_Trend_{name}'
        tittle = f'{name}'
        plot_trend(VarFile, Varout, tittle, i, name)
