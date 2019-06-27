"""
Times series plot of all components of anthropogenic heat flux and statistics
"""
import lucy_postproc as lp
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd

fname = 'Statistics_AHF_2005_1_Berlin_48_0.8.txt'
start_date = '2005-01-01'   # simulation start time [yyyy-mm-dd]

### Time series data
time_series = lp.TemporalData(fname)


### Extract the columns into NumPy arrays
ahf_mean = time_series.get_column('AHFMean')
qb_mean  = time_series.get_column('QbMean')
qv_mean  = time_series.get_column('QvMean')
qm_mean  = time_series.get_column('QmMean')

ahf_min  = time_series.get_column('AHFMin')
ahf_max  = time_series.get_column('AHFMax')
ahf_std  = time_series.get_column('AHFStd')

qb_min   = time_series.get_column('QbMin')
qb_max   = time_series.get_column('QbMax')
qb_std   = time_series.get_column('QbStd')

qv_min   = time_series.get_column('QvMin')
qv_max   = time_series.get_column('QvMax')
qv_std   = time_series.get_column('QvStd')

qm_min   = time_series.get_column('QmMin')
qm_max   = time_series.get_column('QmMax')
qm_std   = time_series.get_column('QmStd')


# ===
# create the Pandas time series. Hourly data with start data = start_date 
# ===
idx = pd.date_range(start_date, periods=len(ahf_mean), freq='H')

ahf_series = pd.Series(ahf_mean, index=idx)
qb_series = pd.Series(qb_mean, index=idx)
qv_series = pd.Series(qv_mean, index=idx)
qm_series = pd.Series(qm_mean, index=idx)

# ===
# set up the graphics
# ===
fig = plt.figure()
ax = plt.axes()

# ===
# 1st: plot the time series
# ===
ahf_series.plot(label='mean AHF')
qb_series.plot(label='mean building')
qv_series.plot(label='mean vehicle')
qm_series.plot(label='mean metabolism')


# ===
# labels, legends, axis limits, ...
# ===
plt.xlabel('Time')
plt.ylabel('W/m2')
plt.legend()

#####################################################################

# ===
# 2nd Plot: minimum, mean, and maximum
# ===
fig2 = plt.figure()

ax_2_1 = fig2.add_subplot(221)
ax_2_2 = fig2.add_subplot(222)
ax_2_3 = fig2.add_subplot(223)
ax_2_4 = fig2.add_subplot(224)

ahf_series.plot(ax=ax_2_1, color='blue')
ax_2_1.fill_between(idx, ahf_min, ahf_max, alpha=0.3, color='blue')
ax_2_1.set_xticklabels([])
# ax_2_1.get_xaxis().set_visible(False)
ax_2_1.set_ylim((0, 55))
ax_2_1.set_title('min, mean, max AHF')

qb_series.plot(ax=ax_2_2, color='orange')
ax_2_2.fill_between(idx, qb_min, qb_max, alpha=0.3, color='orange')
# ax_2_2.get_xaxis().set_visible(False)
ax_2_2.set_xticklabels([])
ax_2_2.set_ylim((0, 55))
ax_2_2.set_title('min, mean, max building')

qv_series.plot(ax=ax_2_3, color='green')
ax_2_3.fill_between(idx, qv_min, qv_max, alpha=0.3, color='green')
ax_2_3.set_ylim((0, 1))
ax_2_3.set_title('min, mean, max vehicle')

qm_series.plot(ax=ax_2_4, color='red')
ax_2_4.fill_between(idx, qm_min, qm_max, alpha=0.3, color='red')
ax_2_4.set_ylim((0, 1))
ax_2_4.set_title('min, mean, max metabolism')

#####################################################################

# ===
# 3rd Plot: mean and standard deviations
# ===
fig2 = plt.figure()

ax_3_1 = fig2.add_subplot(221)
ax_3_2 = fig2.add_subplot(222)
ax_3_3 = fig2.add_subplot(223)
ax_3_4 = fig2.add_subplot(224)

ahf_series.plot(ax=ax_3_1, color='blue')
ax_3_1.fill_between(idx, ahf_mean-ahf_std, ahf_mean+ahf_std, alpha=0.3, color='blue')
ax_3_1.set_xticklabels([])
# ax_3_1.get_xaxis().set_visible(False)
ax_3_1.set_ylim((0, 70))
ax_3_1.set_title('mean & stddev AHF')

qb_series.plot(ax=ax_3_2, color='orange')
ax_3_2.fill_between(idx, qb_mean-qb_std, qb_max+qb_std, alpha=0.3, color='orange')
# ax_3_2.get_xaxis().set_visible(False)
ax_3_2.set_xticklabels([])
ax_3_2.set_ylim((0, 70))
ax_3_2.set_title('mean & stddev building')

qv_series.plot(ax=ax_3_3, color='green')
ax_3_3.fill_between(idx, qv_mean-qv_std, qv_mean+qv_std, alpha=0.3, color='green')
ax_3_3.set_ylim((0, 1))
ax_3_3.set_title('mean & stddev vehicle')

qm_series.plot(ax=ax_3_4, color='red')
ax_3_4.fill_between(idx, qm_mean-qm_std, qm_mean+qm_std, alpha=0.3, color='red')
ax_3_4.set_ylim((0, 1))
ax_3_4.set_title('mean & stddev metabolism')

plt.show()