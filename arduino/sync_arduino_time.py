import serial
import argparse
from time import time

def parse_args():
    parser = argparse.ArgumentParser(description='Send current Unix epoch (seconds since January 1 1970) to serial device (e.g. Arduino) to sync its clock.')
    parser.add_argument('--baud', type=int, default=9600,
                    help='Baud rate of the device.')
    parser.add_argument('--device', type=str, default='/dev/ttyUSB0',
                    help='The serial device port. Usually "dev/ttyUSB0/" or "dev/ttyACM0".')
    return parser.parse_args()

def main():
    args = parse_args()
    message = 'T'
    message += str(int(time()))
    message += 'n'
    message = message.encode('ASCII')
    print('Sending message: {}'.format(message))
    with serial.Serial(args.device, args.baud) as ser:
        ser.write(message)
    print('Succesfully sent.')

if __name__ == "__main__":
    main()
