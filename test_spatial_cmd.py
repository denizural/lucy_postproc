"""
Usage: 
    python test_spatial_germany.py <lucy_file>  

A sample script to plot data for Germany. File name is given from the
command line. Both relative and absolute paths are supported.
"""
import argparse
import matplotlib.pyplot as plt
import os
import sys
import lucy_postproc as lp
plt.style.use('seaborn-whitegrid')

### Initialize the command-line argument parser
parser = argparse.ArgumentParser(description = 'plot the anthropogenic heat flux (AHF) from the LUCY model outputs')
parser.add_argument('file_name', help='name of the LUCY output file')
args = parser.parse_args() 

if os.path.isfile(args.file_name):
    print(f"Opening file : {args.file_name}")
else:
    print(f"ERROR: {args.file_name} does not exist. Exiting")
    sys.exit()

### Spatial AHF data file. 
# Eg. AHF_Berlin_0_6_1_48_0.8.asc
#     AHF_Germany_1_6_1_48_0.8.asc
ahf_data = lp.SpatialData(args.file_name)


### Initialize the spatial AHF object
ahf_data = lp.SpatialData(args.file_name)

### Load the AHF data into a 2-D array
arr2D = ahf_data.get_data()

### Plot the AHF
fig = ahf_data.plot(arr2D)
plt.show()

### save the figure
# lp.savefig(fig, 'plot_spatial_germany.png')
