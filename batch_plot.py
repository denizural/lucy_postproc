"""
A demo code to make batch plots and combine them into an animation using ImageMagick.
"""
import lucy_postproc as lp
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import argparse
import os
import sys

### Initialize the command-line argument parser
parser = argparse.ArgumentParser(description = 'Batch plot animation of LUCY files')
parser.add_argument('dir_name', help='Directory where LUCY files are stored')
args = parser.parse_args() 

if not os.path.isdir(args.dir_name):
    print(f"ERROR: {args.dir_name} does not exist. Exiting")
    sys.exit()


# file names:
#   AHF_Germany_0_6_1_48_0.8.asc
#   AHF_Germany_1_6_1_48_0.8.asc
#   AHF_Germany_2_6_1_48_0.8.asc
#   ...
#   AHF_Germany_23_6_1_48_0.8.asc
indices = np.arange(0, 24)

# ===
# Animation loop: construct the file name and use the built-in plot
# methods to plot and save the figure. Alternatively, you can also
# provide a custom script to make the plots.
# ===
for index in indices:
    infile = args.dir_name + os.path.sep + 'AHF_Germany_' + str(index) + '_6_1_48_0.8.asc'
    
    print(f"index: {index}\t {os.path.basename(infile)}")
    
    # Spatial AHF data
    ahf_data = lp.SpatialData(infile)
    
    # Load the AHF
    arr2D = ahf_data.get_data()

    # Plot the AHF
    fig = ahf_data.plot(arr2D)

    # save the figure
    fig_name = 'germany_' + str(index) + '.png'
    lp.savefig(fig, fig_name)
    
    plt.close(fig)

### Use ImageMagick to combine the figures into a gif animation
# magick convert -delay 20 "germany_%d.png[0-23]" -loop 0 germany_anim.gif
