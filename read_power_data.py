from os.path import getsize
from struct import iter_unpack
import numpy as np

BATTERY_LOG = './data/battery'
SOLAR_LOG = './data/solar'

def read(path):
    with open(path, 'rb') as f:
        return [x for x in iter_unpack('<Lff', f.read())]

def main():
    print('datetime (epoch) - voltage (V) - current (mA)')
    print('Battery')
    print(read(BATTERY_LOG))
    print('Solar')
    print(read(SOLAR_LOG))

if __name__ == '__main__':
    main()
