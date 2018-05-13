# coding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
from struct import iter_unpack

days = 14

# Read from binary
def read(path):
    with open(path, 'rb') as f:
        return [x for x in iter_unpack('<Lff', f.read())]
solar   = pd.DataFrame(read('./data/solar.data'),   columns=['datetime', 'voltage (V)', 'current (mA)'])
battery = pd.DataFrame(read('./data/battery.data'), columns=['datetime', 'voltage (V)', 'current (mA)'])
solar   = solar[solar['datetime']>0]
battery = battery[battery['datetime']>0]
solar = solar.set_index('datetime')
solar.index = pd.to_datetime(solar.index, unit='s')
solar['power (mW)'] = solar['voltage (V)'] * solar['current (mA)']
solar = solar.sort_index()
battery = battery.set_index('datetime')
battery.index = pd.to_datetime(battery.index, unit='s')
battery['power (mW)'] = battery['voltage (V)'] * battery['current (mA)']
battery = battery.sort_index()

fig, axes = plt.subplots(ncols=2, nrows=3, figsize=(16,9), sharex=True, sharey='row')

axes[0,1].get_shared_y_axes().remove(axes[0,0]) # decouple just this row
axes[0,0].set_ylim([3.2,4.2])
axes[0,1].set_ylim([0,6])
for i,x in enumerate([battery, solar]):
    for j in range(3):
        axes[j,i].set_title(['battery', 'solar'][i])
    axes[0,i].set_ylabel('voltage (V)')
    axes[1,i].set_ylabel('current (mA)')
    axes[2,i].set_ylabel('power (mW)')
    x.loc[x.last_valid_index()-pd.DateOffset(days, 'D'):, 'voltage (V)'].plot(ax=axes[0,i], style='.', markersize=1)
    x.loc[x.last_valid_index()-pd.DateOffset(days, 'D'):, 'current (mA)'].plot(ax=axes[1,i], style='.', markersize=1)
    x.loc[x.last_valid_index()-pd.DateOffset(days, 'D'):, 'power (mW)'].plot(ax=axes[2,i], style='.', markersize=1)

plt.tight_layout()
plt.show()
