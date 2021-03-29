
import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
from matplotlib.pyplot import *
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature


cube = iris.load_cube('/disk2/lr452/Downloads/fgco2_data/fgco2_Omon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_199401-201412.rg.yr.so.fix.mask.nc','fgco2')


add_month_number(cube, 'time', name='month_number')
cube2 = cube[np.where((cube.coord('month_number').points == 12) | (cube.coord('month_number') == 1) | (cube.coord('month_number') == 2))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2, 'time', name='season_year')

#then average by the season year:
cube3 = cube2.aggregated_by(['season_year'], iris.analysis.MEAN)


cube4 = cube3.collapsed('time',iris.analysis.MEAN)


fig = plt.figure(figsize=[10, 10])
ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.SouthPolarStereo(), frame_on=False)

    # Limit the map to -60 degrees latitude and below.
ax1.set_extent([-180, 180, -90, -40], ccrs.PlateCarree())


lons = cube4.coord('longitude').points
lats = cube4.coord('latitude').points
data = cube4.data

l = ax1.pcolormesh(lons, lats, data,
                transform=ccrs.PlateCarree(),
                cmap='bwr', vmin=-1.5e-09, vmax=1.5e-09)

ax1.add_feature(cfeature.LAND, facecolor='gray', edgecolor='dimgray')
ax1.gridlines()
ax1.spines
ax1.set_title('ACCESS-ESM1-5')
fig.colorbar(l, label='kg m-2 s-1', orientation='horizontal', extend='both', shrink=0.8)

plt.show()


