#!/bin/bash
(sudo socat pty,rawer,echo=0,link=/dev/ttyS90,group=dialout pty,rawer,echo=0,link=/dev/ttyS91,group=dialout) &
PTYs="readlink -f /dev/ttyS90"
PTYc="readlink -f /dev/ttyS91"
sleep 1
sudo chmod 660 $PTYs
sudo chmod 660 $PTYc 
date >> tcx.log
cat fig.txt >> tcx.log
source $HOME/TCx/env/bin/activate
python $HOME/TCx/TCx.py &>> tcx.log

