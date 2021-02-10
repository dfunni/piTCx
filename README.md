# TCx
TCx is a Raspberry Pi based roaster control system using Artisan Roasterscope
as front-end UI. A standalone Raspberry Pi can interface with any TCx board 
(original TC4, TCsolo, or TCduo) to record temperatures from up to four
thermocouples as well as the ambient temperature sensor (MCP9800) on the TCx board. 
For roaster control, the Raspberry pi can perform heater control using slow PWM (1 Hz).

Additionally, the Raspberry Pi can interface with an Arduino (3.3 V variant)
using serial commands over GPIO pins 14 and 15 (Broadcom pins 8 and 10). This allows 
for fast PWM control of heater as well as phase angle control of an AC
fan. For PAC fan control, the Arduino hardware interrupt (DIO2) must be used to
monitor zero cross detecting circuitry and control a random fire SSR on the TCx
OT2 pin.

# Raspberry Pi Setup
## Serial communication setup
1. Ensure hardware serial is enabled in raspi-config
2. Stop the getty service for /dev/ttyAMA0
```
sudo systemctl disable serial-getty@ttyAMA0.service
```
3. Add the following line to the end of /boot/config.txt
```
dtoverlay=pi3-miniuart-bt
```
## Launch TCx on boot
Create systemd unit file at `/lib/systemd/system/TCx.service` with the
following:
```
[Unit]
Desciption=Initialize TCx
After=multi-user.target

[Service]
Type=idle
ExecStart=$HOME/TCx/start.sh &>> $HOME/tcx.log 2>&1

[Install]
WantedBy=multi-user.target
```
After creating the file run
```
sudo chmod 644 /lib/systemd/system/TCx.service
```

## Launch Artisan on boot
Create systemd unit file at `/lib/systemd/system/artisan.service` with the
following:
```
[Unit]
Desciption=Initialize TCx
After=graphical.target

[Service]
Type=idle
ExecStart=artisan &

[Install]
WantedBy=graphical.target
```
After creating the file run
```
sudo chmod 644 /lib/systemd/system/artisan.service
```

# Artisan Setup

# Testing TCx on standalone Raspberry Pi
1. Ensure Raspberry Pi setup is completed per instructions in Raspberry Pi Setup
  section.
2. Open two terminals.
3. In the first terminal, navigate to the .../TCx/test/ directory and run:
```
./start_test.sh
```
4. In the second termial, navigate the the .../TCx/test/ directory and run:
```
./test.sh
```
to initiate a default test of the full functionality of the TCx software.
Alternately, a single Artisan command can be executed with:
```
./ArtisonCMD.sh <command> [<value>]
```
 using a command value pair from the following:
| command | value | notes |
| ------- | ----- | ----- |
| CHAN    | 1234  | Initializes the TCx and sets order of ADC channels |
| READ    |       | No value for READ command |
| UNITS   | F/C   | Temperature units to be read |
| OT1     | 0-100 | Sets OT1 duty cycle |
| OT2     | 0-100 | Sets OT2 duty cycle |
| IO2     | 0-100 | Sets IO2 duty cycle | 

