# coding: utf-8
import pandas as pd
import termplot as tplot
from utils import read
from numpy import int64
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Plots battery, solar panel, CPU, and RAM data over time.')
    parser.add_argument('last_days', type=int, help='Last number of days to plot.')
    return parser.parse_args()

def main(last_days=1):
    solar   = pd.DataFrame(list(read('./data/solar.data', last_days=last_days)), columns=['datetime', 'voltage (V)', 'current (mA)'])
    battery = pd.DataFrame(list(read('./data/battery.data', last_days=last_days)), columns=['datetime', 'voltage (V)', 'current (mA)'])
    system  = pd.DataFrame(list(read('./data/system.data', last_days=last_days)), columns=['datetime', 'CPU', 'RAM'])

    def prep(df):
        df = df[df['datetime']>0]
        df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
        df = df.set_index('datetime')
        df = df.resample('T').median() # average per minute
        df = df.reset_index()
        df['datetime'] = df['datetime'].astype(int64) // 10 ** 9
        return df

    solar = prep(solar)
    battery = prep(battery)
    system = prep(system)

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

if __name__ == "__main__":
    args = parse_args()
    main(args.last_days)
