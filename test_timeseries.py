"""
A demo code to show how temporal data from LUCY model outputs are analyzed
and visualized with the lucy_postproc module
"""
import lucy_postproc as lp
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

fname = 'Statistics_AHF_2005_1_Berlin_48_0.8.txt'
start_date = '2005-01-01'

# Initialize the Anthropogenic Heat Flux (AHF) time series data and assign
# it to a Pandas data frame
time_series = lp.TemporalData(fname)

# Print the list of columns in the file
print('fields found the file: ')
time_series.columns()

# Extract a column from the 
ahf_mean = time_series.get_column('AHFMean')

# Convert the data into a Pandas data frame
df = time_series.get_dataframe()

# Convert the data into a 2-D Numpy array
data = time_series.get_data()

# Plot time series using the built-in method or you can also your own
# Matplotlib commands
fig = time_series.plot(ahf_mean)
plt.show()

# Save the figure
fig_name = 'test_timeseries.png'
lp.savefig(fig, fig_name)
print(f"plot has been saved as {fig_name}")