#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
from struct import pack
from time import time, sleep

SHUNT_OHMS = 0.1
BATTERY_LOG = './data/battery'
SOLAR_LOG = './data/solar'

def save_line(path, voltage, current):
    with open(path, 'ab') as f:
        f.write(pack('fff', time(), voltage, current))

def main():
    battery = INA219(SHUNT_OHMS, address=0x41)
    solar = INA219(SHUNT_OHMS, address=0x40)
    battery.configure()
    solar.configure()

    print('Monitoring power...')

    while True:
       battery.wake()
       save_line(BATTERY_LOG, battery.voltage(), battery.current()) 
       battery.sleep()
       solar.wake()
       save_line(SOLAR_LOG, solar.voltage(), solar.current())
       solar.sleep()
       sleep(1)

if __name__ == "__main__":
    main()
