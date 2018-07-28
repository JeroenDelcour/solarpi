#!/usr/bin/env python3
from ina219 import INA219, DeviceRangeError
from struct import pack
from time import time, sleep
from psutil import cpu_percent, virtual_memory
from os import system
import logging

logging.basicConfig(filename='/home/pi/solarpi/monitor.log', level=logging.ERROR, format='%(asctime)s %(message)s')

SHUNT_OHMS = 0.1
#MAX_EXPECTED_AMPS = 0.4
BATTERY_LOG = '/home/pi/solarpi/data/battery.data'
SOLAR_LOG = '/home/pi/solarpi/data/solar.data'
SYSTEM_LOG = '/home/pi/solarpi/data/system.data'
MIN_BATTERY_VOLTAGE = 3.0

def save_line(path, x, y):
    with open(path, 'ab') as f:
        # write as uint32 (unsigned long), float32, float32, in little-endian
        f.write(pack('<Lff', int(time()), x, y))

def main():
    battery = INA219(SHUNT_OHMS, address=0x41)
    solar = INA219(SHUNT_OHMS, address=0x40)
    battery.configure(battery.RANGE_16V)
    solar.configure(solar.RANGE_16V)
    shutting_down = False

    while True:
        try:
            battery.wake()
            try:
                battery_voltage = battery.voltage()
                save_line(BATTERY_LOG, battery_voltage, battery.current()) 
            except (DeviceRangeError, OSError) as e:
                logging.error(e)
            battery.sleep()

            solar.wake()
            try:
                save_line(SOLAR_LOG, solar.voltage(), solar.current())
            except (DeviceRangeError, OSError) as e:
                logging.error(e)
            solar.sleep()

            save_line(SYSTEM_LOG, cpu_percent(), virtual_memory().percent)

            if not shutting_down and battery_voltage < MIN_BATTERY_VOLTAGE:
                logging.warning('Battery voltage ({}) below safe minimum ({})! Shutting down soon...'.format(battery_voltage, MIN_BATTERY_VOLTAGE))
                system("sudo shutdown -h +5 'Battery voltage below safe minimum! Shutting down soon.'")
                shutting_down = True
        except Exception as e:
            logging.error(e)

        sleep(1)

if __name__ == "__main__":
    main()
