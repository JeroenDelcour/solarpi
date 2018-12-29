# SolarPi

Attempt to run a Raspberry Pi Zero completely on solar power. Uses an Arduino (Pro Mini) to shutdown/bootup Pi based on battery voltage.

## Shutdown and poweroff GPIO

Add to `/boot/config.txt`:

```
dtoverlay=gpio-poweroff,gpiopin=21,active_low="y" # GPIO pin 21 (physical pin 40) will go high when the Pi is on and low when off.
dtoverlay=gpio-shutdown,gpio_pin=20 # Pull GPIO pin 20 (physical pin 38) low to shut down Pi.
```

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

### Sources

- http://www.raspberryvi.org/stories/arduino-cli.html
- https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy
- https://www.sudomod.com/forum/viewtopic.php?f=43&t=4258#p46032
