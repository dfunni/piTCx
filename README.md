# TCx
TCx is a Raspberry Pi based roaster control system for Artisan Roasterscope
as front-end UI. A standalone Raspberry Pi can interface with any TCx board 
(original TC4, TCsolo, or TCduo) to record temperatures from up to four
thermocouples as well as the temperature sensor (MCP9800) on the TCx board. 
For roaster control, the Raspberry pi can perform temperature control using
slow PWM (1 Hz).

Additionally, the Raspberry Pi can interface with an Arduino (3.3 V variant)
using serial over GPIO pins 14 and 15 (Broadcom pins 8 and 10). This can be
used for fast PWM control of heater as well as phase angle control of an AC
fan. For PAC fan control, the arduino hardware interrupt (DIO2) must be used to
monitor zero cross detecting circuitry to control a random fire SSR on the TCx
OT2 pin.

# Raspberry Pi Setup
- Ensure hardware serial is enabled in raspi-config
- Stop the getty service for /dev/ttyAMA0
```
sudo systemctl disable serial-getty@ttyAMA0.service
```
- Add the following line to the end of /boot/config.txt
```
dtoverlay=pi3-miniuart-bt
```

# Artisan Setup

# Testing TCx on standalone Raspberry Pi
- Ensure Raspberry Pi setup is completed per instructions in Raspberry Pi Setup
  section.
- Open two terminals.
- In the first terminal, navigate to the TCx directory and run:
```
./start_test.sh
```
- In the second termial, navigate the the TCx directory and run:
```
./test/test.sh
```
to initiate a default test of the full functionality of the TCx software.
Alternately, a single Artisan command can be executed with:
```
./test/ArtisonCMD.sh <command> [<value>]
```
with a command value pair from the following:
| command | value | notes |
| ------- | ----- | ----- |
| CHAN    | 1234  | Initializes the TCx and sets order of ADC channels |
| READ    |       | No value for READ command |
| UNITS   | F/C   | Temperature units to be read |
| OT1     | 0-100 | Sets OT1 duty cycle |
| OT2     | 0-100 | Sets OT2 duty cycle |
| IO2     | 0-100 | Sets IO2 duty cycle | 

