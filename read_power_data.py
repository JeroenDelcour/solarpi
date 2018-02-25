from os.path import getsize
from struct import unpack
import numpy as np

BATTERY_LOG = './data/battery'
SOLAR_LOG = './data/solar'

def read(path):
    data = np.fromfile(path, dtype=np.float32, sep='')
    return data.reshape(-1,3)

def main():
    print('time (epoch) - voltage (V) - current (mA)')
    print('Battery')
    print(read(BATTERY_LOG))
    print('Solar')
    print(read(SOLAR_LOG))

if __name__ == '__main__':
    main()
