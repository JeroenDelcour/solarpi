# coding: utf-8
import pandas as pd
import termplot as tplot
from utils import read

last_days = 1

solar   = pd.DataFrame(list(read('./data/solar.data', last_days=last_days)),   columns=['datetime', 'voltage (V)', 'current (mA)'])
battery = pd.DataFrame(list(read('./data/battery.data', last_days=last_days)), columns=['datetime', 'voltage (V)', 'current (mA)'])
system  = pd.DataFrame(list(read('./data/system.data', last_days=last_days)), columns=['datetime', 'CPU', 'RAM'])
solar   = solar[solar['datetime']>0]
battery = battery[battery['datetime']>0]
system  = system[system['datetime']>0]
solar['power (mW)']   = solar['voltage (V)']   * solar['current (mA)']
battery['power (mW)'] = battery['voltage (V)'] * battery['current (mA)']

print('Battery voltage (V)')
tplot.scatter(battery['datetime'], battery['voltage (V)'], ylim=(3,4.2))
print()
print('Power consumption (red) and solar generation (yellow) (mW)')
tplot.scatter([battery['datetime'], solar['datetime']], [battery['power (mW)'], solar['power (mW)']],
              color=('red','yellow'),
              ylim=(0, max(battery['power (mW)'].max(), solar['power (mW)'].max())))
print()
print('CPU (cyan) and RAM (magenta) utilization (%)')
tplot.scatter([system['datetime'], system['datetime']], [system['CPU'], system['RAM']],
              color=('cyan', 'magenta'),
              ylim=(0,100))
