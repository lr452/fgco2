
import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
from matplotlib.pyplot import *
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature

cube = iris.load_cube('/disk2/lr452/Downloads/fgco2_data/fgco2_Omon_GISS-E2-1-G_historical_r101i1p1f1_gn_199401-201412.rg.yr.so.fix.mask.nc','fgco2')

add_month_number(cube, 'time', name='month_number')
cube2 = cube[np.where((cube.coord('month_number').points == 12) | (cube.coord('month_number') == 1) | (cube.coord('month_number') == 2))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2, 'time', name='season_year')

#then average by the season year:
cube3 = cube2.aggregated_by(['season_year'], iris.analysis.MEAN)

cube4 = cube3.collapsed('time',iris.analysis.MEAN)

lons = cube4.coord('longitude').points
lats = cube4.coord('latitude').points
data = cube4.data

fig = plt.figure(figsize=[10, 10])
ax1 = fig.add_subplot(1, 1, 1, projection=ccrs.SouthPolarStereo(), frameon=False)
#ax1 = plt.axes([0,0,1,1], projection=ccrs.SouthPolarStereo(), frameon=False)

# Limit the map to -60 degrees latitude and below.
ax1.set_extent([-180, 180, -90, -40], ccrs.PlateCarree())

l=ax1.pcolormesh(lons, lats, data,
    transform=ccrs.PlateCarree(),
    cmap='bwr', vmin=-2e-09, vmax=2e-09)

ax1.add_feature(cfeature.LAND, facecolor='gray', edgecolor='dimgray')
ax1.gridlines()


ax1.set_title('GISS-E2-1-G')

#ax1.spines['top'].set_color('none')
#ax1.spines['right'].set_color('none')
#ax1.spines['bottom'].set_color('none')
#ax1.spines['left'].set_color('none')

cb =fig.colorbar(l, orientation='horizontal', extend='both', shrink=0.8)
cb.set_label(label='kg m-2 s-1', weight='bold')
font = {'weight': 'bold'}
cb.ax.set_xticklabels(["-2.0", "-1.5", "-1.0", "-0.5", "0.0", "0.5", "1.0", "1.5", "2.0"], fontsize=9, weight='bold')

plt.show()


