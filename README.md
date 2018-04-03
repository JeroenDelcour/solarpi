# SolarPi

Attempt to run a Raspberry Pi Zero completely on solar power, using an Arduino Nano to monitor and control power to the Pi.

## Dependencies

The stuff needed to compile the Arduino code:

`sudo apt-get install build-essential arduino arduino-core arduino-mk`

Arduino libraries need to be installed in `/usr/share/arduino/libraries/`:

```
cd /usr/share/arduino/libraries/
sudo git clone https://github.com/adafruit/Adafruit_INA219
sudo git clone https://github.com/PaulStoffregen/Time
```

## Compiling the Arduino code

This project uses [Sudar's Arduino Makefile](https://github.com/sudar/Arduino-Makefile). In `arduino/monitor/` there's a `Makefile`. You'll need to change some parameters to suit your situation (see the [list of useful variables](https://github.com/sudar/Arduino-Makefile#useful-variables) for more info:

- `BOARD_TAG`: What kind of board you have (e.g. `UNO` for Arduino Uno). For a list of boards it accepts, run `make show_boards`.
- `ARDUINO_PORT`: The port where your Arduino is plugged in, usually `/dev/ttyACM0` or `/dev/ttyUSB0` in Linux or Mac OS X. To find out, look at `dmesg | grep tty`.

Then run `make` in `arduino/monitor`. Hopefully there are no errors. To upload to the Arduino, run `sudo make upload`.

At this point, the Arduino will wait until it is given the current epoch time (seconds since January 1, 1970). This is because it stores the datetime alongside each measurement, and its clock is reset with every reset. To give it the current datetime, set up the Python environment and run `python sync_arduino_time.py -b 9600 -d /dev/ttyUSB0` (or whatever port your Arduino is connected to). The Arduino's internal clock will drift slightly over long periods of time. The `sync_arduino_time.py` can be rerun at any time to re-sync the Arduino.

To check the Arduino code is working, you can use `ttylog -b 9600 -d /dev/ttyUSB0` (again, change to your Arduino port). That should show you regularly updating measurements over the serial interface.

## Setting up the Python virtual environment

1. Set up fresh Python virtual environment: `python3 -m venv SolarPi-env`
2. Activate it: `source SolarPi-env/bin/activate`
3. Install Python dependencies: `pip install -r requirements.txt`

## Raspberry Pi power saving tricks

### Works

- Turn off HDMI with `/usr/bin/tvservice -o` (`/usr/bin/tvservice -p` to reenable). Set this automatically at boot by adding it to `/etc/rc.local`. Saves about 30mA on my setup. 
- [Turning off wifi interface tx](https://www.raspberrypi.org/forums/viewtopic.php?p=894671&sid=afd97b095bbe85c0a67b1d3d03822ce1#p894671) with `iwconfig wlan0 txpower off` saves about 30mA. You can turn it back on with `iwconfig wlan0 txpower auto`.
- [Turning off the ACT LED](https://raspberrypi.stackexchange.com/questions/697/how-do-i-control-the-system-leds-using-my-software) using `echo none | sudo tee /sys/class/leds/led0/trigger` saves about 2mA, which is hardly worth it imo since it makes it harder to know if the Pi is on or not. Turn the LED back on using `echo mmc0 | sudo tee /sys/class/leds/led1/trigger`.
- Instead of the default `deadline` I/O schedular, use `noop`, which has less CPU overhead. In `/boot/cmdline.txt`, set `elevator=noop`. This saves me about 5mA.

### Doesn't work

- Lower the swapiness setting so the system doesn't swap nearly as often, saving on I/O. In `/etc/sysctl.conf`, add `vm.swappiness = 1`.
- Disable bluetooth. In `/boot/config.txt`, add `dtoverlay=pi3-disable-bt`.
- [Turning off USB](https://www.raspberrypi.org/forums/viewtopic.php?p=894674&sid=afd97b095bbe85c0a67b1d3d03822ce1#p894674) using `echo 0 | sudo tee /sys/devices/platform/soc/20980000.usb/buspower >/dev/null`. Could be because I don't have anything connected to the USB port. (Turn it back on using `echo 1 | sudo tee /sys/devices/platform/soc/20980000.usb/buspower >/dev/null`)

## To-do

- [x] Use Arduino Nano to monitor power (uses MUCH less power, so better for continuous monitoring)
    - [x] wire up Arduino Nano to SD card module
    - [x] Wire up Arduino Nano to current sensors
    - [x] Write current and voltage to SD card 
        - [x] read current and voltage
        - [x] get current datetime
            - [x] It's easy to get the elapsed time, but to get the current time I'll need to sync system time with Arduino when it's initialized
        - [x] write to SD card in CSV format
- [ ] write to SD card more [efficiently](https://hackingmajenkoblog.wordpress.com/2016/03/25/fast-efficient-data-storage-on-an-arduino/)
- [ ] Be able to read logged data over WiFi
    - [ ] maybe have the Pi request the full data file from the Arduino on demand?
- [ ] Control Raspberry Pi with Arduino Nano
    - [ ] send shutdown signal to Pi when battery is almost empty
    - [ ] control power to the Pi using a relay controlled by the Arduino
- [ ] Try a different 5V (or 3V) converter. The current one using 600mW to get 375mW out (only 62.5% efficiency!). Maybe a buck boost converter?

### Sources

- http://www.raspberryvi.org/stories/arduino-cli.html
- https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy
- https://www.sudomod.com/forum/viewtopic.php?f=43&t=4258#p46032
