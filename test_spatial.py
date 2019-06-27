"""
A demo code to show how spatial data from LUCY model output are analyzed
and visualized with the lucy_postproc module
"""
import lucy_postproc as lp
import matplotlib.pyplot as plt

# Initialize the spatial Anthropogenic Heat Flux (AHF) data
ahf_data = lp.SpatialData('AHF_Germany_12_7_2_48_0.8.asc')

# Load the AHF into a Numpy array and mask the missing values
data = ahf_data.get_data()

# Plot the AHF using the provided plot function or you can also your own
# Matplotlib commands
fig = ahf_data.plot(data)
plt.show()

# Save the figure
fig_name = 'test_spatial.png'
lp.savefig(fig, fig_name)
print(f"plot has been saved as {fig_name}")
