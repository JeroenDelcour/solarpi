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

## Setting up the Python virtual environment

1. Set up fresh Python virtual environment: `python3 -m venv SolarPi-env`
2. Activate it: `source SolarPi-env/bin/activate`
3. Install Python dependencies: `pip install -r requirements.txt`

## Power saving tricks

### Works

- Turn off HDMI with `/usr/bin/tvservice -o` (`/usr/bin/tvservice -p` to reenable). Set this automatically at boot by adding it to `/etc/rc.local`. Saves about 30mA on my setup. 
- Instead of the default `deadline` I/O schedular, use `noop`, which has less CPU overhead. In `/boot/cmdline.txt`, set `elevator=noop`. This saves me about 5mA.

### Doesn't work

- Lower the swapiness setting so the system doesn't swap nearly as often, saving on I/O. In `/etc/sysctl.conf`, add `vm.swappiness = 1`.
- Disable bluetooth. In `/boot/config.txt`, add `dtoverlay=pi3-disable-bt`.
- The USB port on the Raspberry Pi Zero can't be powered off because it's directly wired to the 5V powerline.

## To-do

- [-] Use Arduino Nano to monitor power (uses MUCH less power, so better for continuous monitoring)
    - [x] wire up Arduino Nano to SD card module
    - [-] Wire up Arduino Nano to current sensors
    - [ ] Write current and voltage to SD card 
        - [ ] read current and voltage
        - [ ] get current datetime
        - [ ] write to SD card [efficiently](https://hackingmajenkoblog.wordpress.com/2016/03/25/fast-efficient-data-storage-on-an-arduino/)
    - [ ] Be able to read logged data over WiFi
        - [ ] maybe have the Pi request the full data file from the Arduino on demand?
    - [ ] Control Raspberry Pi with Arduino Nano
        - [ ] send shutdown signal to Pi when battery is almost empty
        - [ ] control power to the Pi using a relay controlled by the Arduino

### Sources

- http://www.raspberryvi.org/stories/arduino-cli.html
- https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy
- https://www.sudomod.com/forum/viewtopic.php?f=43&t=4258#p46032
