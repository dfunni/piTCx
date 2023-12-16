# TCx
TCx is a Raspberry Pi based roaster control system using Artisan Roasterscope as front-end UI. A standalone Raspberry Pi can interface with any TCx board (original TC4, TCsolo, TCduo, or TC4 HAT+) to record temperatures from up to four thermocouples as well as the temperature sensor (MCP9800) on the TCx board. For roaster control, the Raspberry Pi can perform heater control using slow PWM (1 Hz) with the Artisan software providing PID control.

## Raspberry Pi Setup
Starting with a fresh install of the latest raspbian OS (tested with Bookworm):

1. configure the raspi with
    
    sudo raspi-config
    
In the "Advanced" menu, select expand filesystem.

In the "Interfaces" menu enable ssh, I2C, Serial Port, and Remote GPIO.

Reboot to finish the configuration.

2. Install required tools
    ```
    sudo apt install socat
    ```
3. Ensure gpiod is running
    ```
    sudo systemctl start gpiod
    ```
4. Install Artisan
    ```
    curl -L -O https://github.com/artisan-roaster-scope/artisan/releases/download/<vx.xx.x>/<artisan-linux-x.xx.x.deb>
    sudo dpkg -i <artisan-linux-x.x.x.deb>
    ```
5. Download and setup the TCx code
    ```
    git clone https://github.com/dfunni/TCx.git
    cd TCx
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```
From here everything is setup and ready. The next steps are to configure Artisan for communication with the TCx board.

## Launch start.sh on boot
Edit crontab with:

    crontab -e

and add the following line:

    @reboot $HOME/TCx/start.sh

## Launch Artisan on boot
Copy `start_artisan.sh` to `/etc/profile.d/` with:

    sudo cp $HOME/TCx/start_artisan.sh /etc/profile.d/

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

