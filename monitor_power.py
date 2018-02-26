#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
from struct import pack
from time import time, sleep

SHUNT_OHMS = 0.1
BATTERY_LOG = '/home/pi/solarpi/data/battery'
SOLAR_LOG = '/home/pi/solarpi/data/solar'

def save_line(path, voltage, current):
    with open(path, 'ab') as f:
        f.write(pack('Lff', int(time()), voltage, current)) # write as uint32 (unsigned long), float32, float32

def main():
    battery = INA219(SHUNT_OHMS, address=0x41)
    solar = INA219(SHUNT_OHMS, address=0x40)
    battery.configure()
    solar.configure()

    print('Monitoring power...')

    while True:
        battery.wake()
        try:
            save_line(BATTERY_LOG, battery.voltage(), battery.current()) 
        except DeviceRangeError as e:
            print(e)
        battery.sleep()

        solar.wake()
        try:
            save_line(SOLAR_LOG, solar.voltage(), solar.current())
        except DeviceRangeError as e:
            print(e)
        solar.sleep()

        sleep(1)

if __name__ == "__main__":
    main()
