# SolarPi

Attempt to run a Raspberry Pi Zero completely on solar power. Mostly code to monitor power usage and solar panel performance.

## Power saving tricks

- Turn off HDMI with `/usr/bin/tvservice -o` (`/usr/bin/tvservice -p` to reenable). Set this automatically at boot by adding it to `/etc/rc.local`. Saves about 30mA on my setup. 
- Instead of the default `deadline` I/O schedular, use `noop`, which has less CPU overhead. In `/boot/cmdline.txt`, set `elevator=noop`. This saves me about 5mA.

### Attempts with no noticable effect

- Lower the swapiness setting so the system doesn't swap nearly as often, saving on I/O. In `/etc/sysctl.conf`, add `vm.swappiness = 1`.
- Disable bluetooth. In `/boot/config.txt`, add `dtoverlay=pi3-disable-bt`.
- The USB port on the Raspberry Pi Zero can't be powered off because it's directly wired to the 5V powerline.

### Sources

- https://www.jeffgeerling.com/blogs/jeff-geerling/raspberry-pi-zero-conserve-energy
- https://www.sudomod.com/forum/viewtopic.php?f=43&t=4258#p46032
