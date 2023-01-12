import math
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import xarray as xr
import matplotlib
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from pylab import rcParams
import matplotlib as mpl
import pymannkendall as mk

## Plot settings
font = {'family': 'Times New Roman'}
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


#


#
# ds = xr.open_dataset('F:/PCSE/pcse/pr_ssp126.nc').time
# x = xr.DataArray(np.arange(len(ds['time'])) + 1, dims='time', coords={'time': ds['time']})
# time = xr.where((ds.time.dt.month == 1) & (ds.time.dt.day == 1), x, np.nan)
# x = x.where(time > 0, drop=True)
# print(x)
# day = xr.open_dataset("C:/Users/Administrator/Desktop/pr_t_Growthday_ssp585.nc")
# day["day"] = day.strat
# # print(day)
# for i, a in enumerate(day.time):
#     day["day"][i, :, :] = x[i]
# # print(day)
# maskfile_Dongbei = 'F:/PCSE/mask_Dongbei.nc'
# mf = xr.open_dataset(maskfile_Dongbei)
# day = day.where(mf.mask_array > 0.0, drop=True)
# day.to_netcdf('C:/Users/Administrator/Desktop/day.nc', engine='netcdf4')
#
def plot_trend(ds, Varout, scenario):
    fig = plt.figure(figsize=(5, 5))  #
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    fname = 'F:/Dongbei/plot/crop_trend/NEshp/NE.shp'
    shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                   ccrs.PlateCarree(), facecolor='none')

    maskfile_Crop = "F:/PCSE/crop/crop.nc"
    crop = xr.open_dataset(maskfile_Crop)
    ds1 = crop
    ds1['trend'] = ds
    ds1 = ds1.where(crop.crop >= 0, drop=True)
    lats = ds1.variables['lat'][:]
    lons = ds1.variables['lon'][:]
    ds_a1 = ds1.where(crop >= 0).squeeze()
    lons2d, lats2d = np.meshgrid(lons, lats)
    p1 = plt.scatter(lons2d[0, 0], lats2d[0, 0], marker='o', color='w', label=f'Sowing year: {scenario}', s=18)
    plt.legend(loc='upper right', fontsize=16)
    bins = np.arange(70, 152, 2)
    # bins = np.arange(math.ceil(max(m))*-1,math.ceil(max(m))+1,1)
    nbin = len(bins) - 1
    cmap4 = mpl.cm.get_cmap('twilight_shifted', nbin)  # coolwarm/bwr/twilight_shifted
    norm4 = mpl.colors.BoundaryNorm(bins, nbin)
    locator = mpl.ticker.MultipleLocator(10)
    im2 = mpl.cm.ScalarMappable(norm=norm4, cmap=cmap4)
    im1 = ax.scatter(lons2d, lats2d, c=ds_a1['trend'].values, s=10.0, alpha=1.0, zorder=2, marker='o',
                     transform=ccrs.PlateCarree(), cmap=cmap4, norm=norm4)  # Paired/magma/plasma/GnBu/YlGn

    ax.set_extent([118, 135, 38, 55])
    ax.set_xticks([120, 125, 130, 135], crs=ccrs.PlateCarree())
    ax.set_yticks([40, 45, 50, 55], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter()
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # fig.colorbar(im1, ax=ax, ticks=locator)
    ax.add_feature(shape_feature)
    plt.tight_layout()
    # plt.savefig('%s.eps' % (Varout), format='eps', dpi=800)
    plt.savefig('%s%s.png' % (Varout, scenario), format='png', dpi=800)
    plt.show()
    plt.close()

def calc_trend(x, y):
    co = np.count_nonzero(~np.isnan(x))
    if co < 4:
        return -9999.0
    slope = mk.original_test(x, alpha=0.01).slope
    return slope  # *100. #,p_value


def trend(x, y, dim='time'):
    return xr.apply_ufunc(
        calc_trend, x, y,
        input_core_dims=[[dim], [dim]],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[float]
    )


def save_xarray(outpath, arr, rid):
    """
    Save output
    """
    arr["lat"].attrs["units"] = "degrees_north"
    arr["lon"].attrs["units"] = "degrees_east"
    arr.to_netcdf(os.path.join(outpath, '%s.nc' % (rid)),
                  encoding={'Esd': {'dtype': 'float32',
                                     'zlib': True,
                                     'complevel': 6,
                                     '_FillValue': -9999.0}})


if __name__ == '__main__':
    import glob, os, shutil

    colors = ['#4B66AD', '#62BEA6', '#FDBA6B', '#EB6046']

    maskfile_Crop = "F:/PCSE/crop/crop.nc"
    Crop = xr.open_dataset(maskfile_Crop)
    Crop_all = Crop.crop

    pathin = "F:/Dongbei/plot/crop_trend/"
    pathout = 'C:/Users/Administrator/Desktop/PCSE/Fig S2/'
    # pathin = ('/tera01/xuqch3/Dongbei/pr_t/')
    GrowthFile = ('%s/pr_t_Growthday_ssp585.nc' % (pathin))
    date = xr.open_dataset(GrowthFile)
    day = xr.open_dataset("F:/Dongbei/plot/crop_trend/day.nc")
    start_date = date.strat - day.day
    start_date = start_date.where(Crop_all >= 0, drop=True)
    print(start_date)
    # date["days"] = start_date
    # for i, year in enumerate(date.time):
    #     plot_trend(start_date[i, :, :], pathout, year.values)

    maskfile =xr.open_dataset("F:/PCSE/mask_Dongbei.nc")
    # names = ['rice', 'maize', 'soybean']

    ds2 = start_date.pipe(lambda x: x).where(start_date > -9999, drop=True)
    x = xr.DataArray(np.arange(len(ds2['time'])) + 1, dims='time', coords={'time': ds2['time']})
    r2 = trend(ds2, x, 'time').compute()
    r2 = r2.to_dataset(name="Esd")  # Convert to dataset
    r2 = r2.where(maskfile.mask_array > 0.0, drop=True)
    save_xarray(f'{pathout}', r2, f'Esd_trend')
