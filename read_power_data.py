from os import SEEK_END
from struct import unpack
from time import sleep

BATTERY_LOG = './data/battery'
SOLAR_LOG = './data/solar'

def tail(path):
    with open(path, 'rb') as f:
        f.seek(-12, SEEK_END) # last 12 bytes
        return unpack('<Lff', f.read())

def main():
    while True:
        datetime, voltage, current = tail(BATTERY_LOG)
        print('{:.3f}V {:.1f}mA'.format(voltage, current))
        sleep(1)

if __name__ == '__main__':
    main()
