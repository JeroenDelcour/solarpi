from os import SEEK_END
from struct import unpack
from time import sleep
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Print tail of power readings. Readings are live if monitor script is running.')
    parser.add_argument('-battery', help='Show battery readings.', action='store_true')
    parser.add_argument('-solar', help='Show solar panel readings.', action='store_true')
    args = parser.parse_args()
    if not (args.battery or args.solar):
        raise argparse.ArgumentTypeError('At leat one of -battery and -solar must be provided.')
    return args

BATTERY_LOG = './data/battery'
SOLAR_LOG = './data/solar'

def tail(path):
    with open(path, 'rb') as f:
        f.seek(-12, SEEK_END) # last 12 bytes
        return unpack('<Lff', f.read())

def main(args):
    while True:
        out = []
        if args.battery:
            datetime, voltage, current = tail(BATTERY_LOG)
            out.append('Battery: {:.3f}V {:.1f}mA    '.format(voltage, current))
        if args.solar:
            datetime, voltage, current = tail(SOLAR_LOG)
            out.append('Solar panel: {:.3f}V {:.1f}mA'.format(voltage, current))
        print('    '.join(out))
        sleep(1)

if __name__ == '__main__':
    args = parse_args()
    main(args)
