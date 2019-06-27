"""
Usage: 
    python test_spatial_custom.py <lucy_file>  

Plots LUCY spatial output file using more customized plotting options.
File name is given from the command line. Both relative and absolute 
paths are supported.
"""
import argparse
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import math
import lucy_postproc as lp
plt.style.use('seaborn-whitegrid')
import os
import sys


### Initialize the command-line argument parser.
parser = argparse.ArgumentParser(description = 'plot the anthropogenic heat flux (AHF) from the LUCY model outputs')
parser.add_argument('file_name', help='name of the LUCY output file')
args = parser.parse_args() 

if os.path.isfile(args.file_name):
    print(f"Opening file : {args.file_name}")
else:
    print(f"ERROR: {args.file_name} does not exist. Exiting")
    sys.exit()

### Spatial AHF data file. Eg. AHF_Berlin_0_6_1_48_0.8.asc, AHF_Germany_12_7_2_48_0.8.asc
ahf_data = lp.SpatialData(args.file_name)

### Get the coordinate dictionary
# Keys are: ncols, nrows, xllcorner, yllcorner, cellsize, nodata_value
coords = ahf_data.get_coords()

### Load the AHF into a Numpy array and mask the missing values
data = ahf_data.get_data()

### Borders of the datas
cellsize = coords['cellsize']
lon_min  = coords['xllcorner']
lon_max  = coords['xllcorner'] + cellsize * coords['ncols']
lat_min  = coords['yllcorner']   
lat_max  = coords['yllcorner'] + cellsize * coords['nrows']

### create the grid
lons = np.arange(lon_min, lon_max, cellsize)
lats = np.arange(lat_min, lat_max, cellsize)
lons, lats = np.meshgrid(lons, lats)

### Build the figure and ax objects
fig, ax = plt.subplots(figsize=(18,9))
# fig, ax = plt.subplots()
ax.set_title('anthropogenic heat flux [w / m2]', fontsize=18)

### Built-in map boundaries
m = Basemap(projection='merc', llcrnrlat=lat_min, urcrnrlat=lat_max, \
    llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='l', ax=ax)

m.drawcoastlines()
# m.drawlsmask(land_color='white', ocean_color='0.8', lakes=False)
m.drawcountries()
# m.drawstates()

### minimum and maximum values of AHF for the contour plot [w/m2]
minval = 0   
maxval = 30

plot = m.pcolormesh(lons, lats, data, cmap=plt.cm.viridis, latlon=True, vmin=minval, vmax=maxval)
 
cbar = m.colorbar(plot, 'right', size='5%', pad='5%')
# cbar.set_label('W / m2')
 
### draw parallels and meridians.
dlat = 1.
dlon = 1.
m.drawparallels(np.arange(math.floor(lat_min), math.ceil(lat_max), dlat), labels=[1,0,0,0])
m.drawmeridians(np.arange(math.floor(lon_min), math.ceil(lon_max), dlon), labels=[0,0,0,1])

plt.show()

### Save the figure
figname = 'plot_spatial_custom.png'
lp.savefig(fig, figname)
print(f"plot has been saved as {figname}")
