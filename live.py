#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from struct import unpack
from time import sleep
import argparse
from utils import tail

def parse_args():
    parser = argparse.ArgumentParser(description='Print tail of power readings. Readings are live if monitor script is running.')
    parser.add_argument('-battery', help='Show battery readings.', action='store_true')
    parser.add_argument('-solar', help='Show solar panel readings.', action='store_true')
    parser.add_argument('-system', help='Show CPU and memory usage', action='store_true')
    parser.add_argument('-temperate', help='Show CPU and GPU temperature.', action='store_true')
    parser.add_argument('-all', help='Show all', action='store_true')
    args = parser.parse_args()
    if not (args.battery or args.solar or args.system or args.all):
        raise argparse.ArgumentTypeError('At leat one of -battery, -solar, -system, or -all  must be set.')
    return args

BATTERY_LOG = './data/battery.data'
SOLAR_LOG = './data/solar.data'
SYSTEM_LOG = './data/system.data'
TEMP_LOG = './data/temperature.data'

def main(args):
    while True:
        out = []
        if args.all or args.battery:
            datetime, voltage, current = tail(BATTERY_LOG)
            out.append('Battery: {:6.3f}V {:7.1f}mA'.format(voltage, current))
        if args.all or args.solar:
            datetime, voltage, current = tail(SOLAR_LOG)
            out.append('Solar panel: {:6.3f}V {:7.1f}mA'.format(voltage, current))
        if args.all or args.system:
            datetime, cpu, memory = tail(SYSTEM_LOG)
            out.append('CPU: {:5.1f}% memory: {:5.1f}%'.format(cpu, memory))
        if args.all or args.temperature:
            datetime, cpu_temp, gpu_temp = tail(TEMP_LOG)
            out.append("CPU: {:6.1f}'C GPU: {:6.1f}'C".format(cpu_temp, gpu_temp))
        print('  |  '.join(out))
        sleep(1)

if __name__ == '__main__':
    args = parse_args()
    main(args)
