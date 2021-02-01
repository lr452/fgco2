import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
import matplotlib as mpl
#from matplotlib import cm
#from colorspacious import *
#from collections import *




cube = iris.load_cube('/disk2/lr452/Downloads/fgco2_data/fgco2_Omon_BCC-ESM1_historical_r1i1p1f1_gn_199401-201412.rg.yr.so.fix.mask.nc','fgco2')

print(cube)
print(cube.shape)

add_month_number(cube, 'time', name='month_number')
cube2 = cube[np.where((cube.coord('month_number').points == 12) | (cube.coord('month_number') == 1) | (cube.coord('month_number') == 2))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2, 'time', name='season_year')

#then average by the season year:
cube3 = cube2.aggregated_by(['season_year'], iris.analysis.MEAN)


cube4 = cube3.collapsed('time',iris.analysis.MEAN)


qplt.pcolormesh(cube4, cmap='PRGn')
#cmaps=[('Diverging', ['PRGn'])]
#plt.xlim(40,120)
#plt.ylim()
plt.show()
