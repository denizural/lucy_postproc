"""
    lucy_postproc module contains the basic data structures and functions to read
    and analyze the LUCY (Large scale Urban Consumption of energY) model outputs
    in ESRI ASCII raster format and time series format.
    
    Deniz Ural, 13/03/2019, PIK Potsdam, RD-2: Climate Resilience
"""
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class SpatialData:
    """
    File structure for the spatial (lat, lon) model output in ESRI ASCII format.
    Object is initiated with the file path string 'fname'. 
    Eg.
    import lucy_postproc as lp
    ahf_data = lp.SpatialData('AHF_Germany_0_6_1_48_0.8.asc')
    """
    def __init__(self, fname):
        self.fname = fname  # LUCY model output file
        self.coords = {}    # holds the coordinates
        self.read_header()  # read the file header
    
    def read_header(self):
        """ 
        read the header information and get the variables 
        number of the header lines to read in the LUCY output file. They describe 
        the ASCII raster file. Here is a sample header:
        
        ncols         67 
        nrows         32 
        xllcorner     13.1167 
        yllcorner     52.3667 
        cellsize       0.0083333 
        NODATA_value  -9999 
        """
        self.header_nlines = 6    # number of lines in the header
        
        # read the header lines as an unformatted list of strings
        with open(self.fname, 'r') as ahf_file:
            ahf_header = ahf_file.readlines()[:self.header_nlines]

        # ===
        # Extract each item in the list, remove the newline and extract the 
        # second item that is the numeric value.
        # ===
        ahf_header = [item.strip().split()[-1] for item in ahf_header]
        
        # fill up the coordinate dictionary
        self.coords['ncols']     = int(ahf_header[0])  # numbers of columns and rows
        self.coords['nrows']     = int(ahf_header[1])  
        self.coords['xllcorner'] = float(ahf_header[2]) # lower left corner coordinates
        self.coords['yllcorner'] = float(ahf_header[3])
        self.coords['cellsize']  = float(ahf_header[4]) # size of the cell
        self.coords['nodata_value'] = float(ahf_header[5])  # missing value
    
    def get_coords(self):
        """
        Return the coordinate dictionary
        """
        return self.coords
    
    def get_data(self):
        """ 
        Read the model output data into 2D array and mask the missing values.

        Returns
        -------
        output_masked : NumPy array
            2D array that is masked with the nodata_value
        """
        
        output = np.loadtxt(self.fname, dtype = np.float, skiprows = self.header_nlines)
        
        # flip the data upside down so that it matches the map coordinates
        output = np.flipud(output)

        # Mask the missing values with NaN and return it
        output_masked = np.ma.masked_equal(output, self.coords['nodata_value'])
        return output_masked

    def plot(self, masked_array):
        """
        plot(masked_array)
        
        Plots the raster image of the anthropogenic heat flux data using Matplotlib.
        
        Parameters
        ----------
        masked_array : NumPy array
            Output of the SpatialData.load() method which contains the masked numerical data     

        Returns
        -------
        fig : Matplotlib figure object
            Output of the Matplotlib plot function
        """
        # Borders of the data
        cellsize = self.coords['cellsize']
        lon_min  = self.coords['xllcorner']
        lon_max  = self.coords['xllcorner'] + cellsize * self.coords['ncols']
        lat_min  = self.coords['yllcorner']   
        lat_max  = self.coords['yllcorner'] + cellsize * self.coords['nrows']
        
        lons = np.arange(lon_min, lon_max, cellsize)
        lats = np.arange(lat_min, lat_max, cellsize)
        lons, lats = np.meshgrid(lons, lats)
        
        # Build the figure and ax objects
        fig, ax = plt.subplots()
        ax.set_title('anthropogenic heat flux [w / m2]')
        
        # Built-in map boundaries
        m = Basemap(projection='merc', llcrnrlat=lat_min, urcrnrlat=lat_max, \
            llcrnrlon=lon_min, urcrnrlon=lon_max, resolution='l', ax=ax)
        
        m.drawcoastlines()
        # m.drawlsmask(land_color='white', ocean_color='0.8', lakes=False)
        m.drawcountries()
        # m.drawstates()

        minval = 0   # minimum and maximum values of AHF for the contour plot [w/m2]
        maxval = 30
        im = m.pcolormesh(lons, lats, masked_array, cmap=plt.cm.viridis, latlon=True, vmin=minval, vmax=maxval)
         
        # Build the colorbar on the right
        cbar = m.colorbar(im, 'right', size='5%', pad='5%')
        # cbar.set_label('W / m2')
         
        # ===
        # draw parallels and meridians.
        # ===
        dlat = 1.
        dlon = 1.
        m.drawparallels(np.arange(math.floor(lat_min), math.ceil(lat_max), dlat),labels=[1,0,0,0])
        m.drawmeridians(np.arange(math.floor(lon_min), math.ceil(lon_max), dlon),labels=[0,0,0,1])
                
        return fig


class TemporalData:
    """
    File structure for the temporal (statistical) model output. This is similar 
    to a data frame where each column contain a field that is defined on the 
    same time instance. Data is read into a Pandas DataFrame df.
    
    Object is initiated with the file path string 'fname'. 
    Eg.
    import lucy_postproc as lp
    time_series = lp.TemporalData('Statistics_AHF_2005_1_Germany_48_0.8.txt')
    """
    def __init__(self, fname):
        self.fname = fname 
        # read the statistics data into a Pandas DataFrame
        self.df = pd.read_csv(fname, delim_whitespace=True, header=0, skiprows=0)
           
    def columns(self):
        """
        Prints the column names (fields) in the LUCY statistics file.
        """
        print(self.df.columns.values)
    
    def get_column(self, col_name):
        """
        Extracts the requested column into a NumPy array.
        
        Parameters
        ----------
        col_name : string
            name of the column. Eg. 'AHFMean' (mean anthropogenic heat flux values)
        
        Returns
        -------
        out : NumPy array
            requested data field
        """
        return self.df[col_name].to_numpy()
    
    def get_data(self):
        """
        Get the statistics as a NumPy matrix.
        
        Returns
        --------
        out : Numpy array
            Pandas DataFrame converted to a NumPy matrix        
        """
        return self.df.to_numpy()
        
    def get_dataframe(self):
        """
        Get the statistics as a Pandas DataFrame    
        """
        return self.df
        
    def plot(self, field):
        """
        Makes xy plot of the given field
        
        Parameters
        ----------
        field : numpy array
            1-D array of time series data. Eg. output of get_column() method.
        
        Returns
        -------
        fig : Matplotlib figure object
            Output of the Matplotlib plot function        
        """
        # Build the figure and ax objects
        fig, ax = plt.subplots()

        ax.plot(field, 'o-')
        
        plt.grid(True)
        ax.set_xlabel('Time')        
        ax.set_title('Time Series')
        
        return fig


def savefig(fig, fig_name):
    """
    savefig(fig_name)
    
    Saves the plot created by plot functions to the hard disk.
    
    Parameters
    ----------
    fig : Matplotlib Figure object
        Output of the plot() function
    fig_name : string
        output name including the file extension. Eg. ahf_2005_01_30.png
    """ 
    fig.savefig(fig_name)
      
