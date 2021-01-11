activate
(sudo socat pty,rawer,echo=0,link=/dev/ttyS90,group=dialout pty,rawer,echo=0,link=/dev/ttyS91,group=dialout) &
PTYs="readlink -f /dev/ttyS90"
PTYc="readlink -f /dev/ttyS91"
sleep 1
sudo chmod 660 $PTYs
sudo chmod 660 $PTYc 
sudo pigpiod -s 10
artisan &
python piTC4.py

