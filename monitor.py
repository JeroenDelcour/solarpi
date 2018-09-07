#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ina219 import INA219, DeviceRangeError
from struct import pack
from time import time, sleep
from psutil import cpu_percent, virtual_memory
from os import system
from subprocess import check_output, run
import logging

logging.basicConfig(filename='/home/pi/solarpi/monitor.log', level=logging.WARNING, format='%(asctime)s %(message)s')

SHUNT_OHMS = 0.1
#MAX_EXPECTED_AMPS = 0.4
BATTERY_LOG = '/home/pi/solarpi/data/battery.data'
SOLAR_LOG = '/home/pi/solarpi/data/solar.data'
SYSTEM_LOG = '/home/pi/solarpi/data/system.data'
TEMP_LOG = '/home/pi/solarpi/data/temperature.data'
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
            except (DeviceRangeError, OSError):
                pass
            battery.sleep()
        except Exception as e:
            logging.error(e)
        try:
            solar.wake()
            try:
                save_line(SOLAR_LOG, solar.voltage(), solar.current())
            except (DeviceRangeError, OSError):
                pass
            solar.sleep()
        except Exception as e:
            logging.error(e)

        try:
            save_line(SYSTEM_LOG, cpu_percent(), virtual_memory().percent)
        except Exception as e:
            logging.error(e)

        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                cpu_temp = float(f.read().strip())/1000
            gpu_temp = float(check_output(['vcgencmd', 'measure_temp']).decode().strip()[5:9])
            save_line(TEMP_LOG, cpu_temp, gpu_temp)
        except Exception as e:
            logging.error(e)

        if not shutting_down and battery_voltage < MIN_BATTERY_VOLTAGE:
            logging.warning('Battery voltage below safe minimum ({} < {})! Shutting down soon.'.format(battery_voltage, MIN_BATTERY_VOLTAGE))
            run(["sudo", "shutdown", "-h", "+5", "'Battery voltage below safe minimum ({} < {})! Shutting down soon.'".format(battery_voltage, MIN_BATTERY_VOLTAGE)])
            shutting_down = True

        sleep(1)

if __name__ == "__main__":
    main()
