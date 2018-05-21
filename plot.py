# coding: utf-8
import pandas as pd
import termplot.plot as tplot
from helpers import read

solar   = pd.DataFrame(list(read('./data/solar.data')),   columns=['datetime', 'voltage (V)', 'current (mA)'])
battery = pd.DataFrame(list(read('./data/battery.data')), columns=['datetime', 'voltage (V)', 'current (mA)'])
solar   = solar[solar['datetime']>0]
battery = battery[battery['datetime']>0]
solar['power (mW)']   = solar['voltage (V)']   * solar['current (mA)']
battery['power (mW)'] = battery['voltage (V)'] * battery['current (mA)']

print('BATTERY VOLTAGE (V)')
tplot(battery['datetime'], battery['voltage (V)'], ylim=(3,4.2))
print()
print('POWER CONSUMPTION (mW) versus SOLAR POWER (mW)')
tplot([battery['datetime'], solar['datetime']], [battery['power (mW)'], solar['power (mW)']], marker=('-','+'), color=('yellow','red'))
