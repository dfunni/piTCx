#!/bin/bash
(socat pty,rawer,echo=0,link=/dev/ttyS90,group=dialout pty,rawer,echo=0,link=/dev/ttyS91,group=dialout) &
PTYs="readlink -f /dev/ttyS90"
PTYc="readlink -f /dev/ttyS91"
sleep 1
chmod 660 $PTYs
chmod 660 $PTYc 
date > /var/log/tcx.log
cat /home/$1/piTCx/fig.txt >> /var/log/tcx.log
source /home/$1/piTCx/env/bin/activate
python /home/$1/piTCx/src/TCx.py $1
