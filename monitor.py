#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
from struct import pack
from time import time, sleep
from psutil import cpu_percent, virtual_memory

SHUNT_OHMS = 0.1
#MAX_EXPECTED_AMPS = 0.4
BATTERY_LOG = '/home/pi/solarpi/data/battery.data'
SOLAR_LOG = '/home/pi/solarpi/data/solar.data'
SYSTEM_LOG = '/home/pi/solarpi/data/system.data'

def save_line(path, x, y):
    with open(path, 'ab') as f:
        # write as uint32 (unsigned long), float32, float32, in little-endian
        f.write(pack('<Lff', int(time()), x, y))

def main():
    battery = INA219(SHUNT_OHMS, address=0x41)
    solar = INA219(SHUNT_OHMS, address=0x40)
    battery.configure(battery.RANGE_16V)
    solar.configure(solar.RANGE_16V)

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
        battery.sleep()
        solar.sleep()

        save_line(SYSTEM_LOG, cpu_percent(), virtual_memory().percent)

        sleep(1)

if __name__ == "__main__":
    main()
