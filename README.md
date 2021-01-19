# Purpose
Create a Raspberry Pi based roaster control system for Artisan Roasterscope
as front-end UI.

# Method
Using components of the TC4 (MCP3424, MCP9800, 24LC512, k-type thermocouple,
etc.), interface with Raspberry Pi over I2C bus to collect temperature data.

Create interface between temperature data collected and Artisan software to
log and visualize temperature vs time.

Interface with Artisan commands for roaster control to control roaster over 
Raspberry Pi GPIO through a solid state relay(s).

# Milestones
1) Temperature data read over I2C
2) Communication interface between thermocouple system and Artisan
3) Communication interface between Artisan and roaster

# Raspberry Pi Setup
- Ensure hardware serial is enabled in raspi-config
- Stop the getty service for /dev/ttyAMA0

    sudo systemctl disable serial-getty@ttyAMA0.service

- Add the following line to the end of /boot/config.txt

    dtoverlay=pi3-miniuart-bt


