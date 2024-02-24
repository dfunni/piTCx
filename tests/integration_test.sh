#!/bin/bash
./ArtisanCMD.sh CHAN 1200
./ArtisanCMD.sh CHAN 1000
./ArtisanCMD.sh OT1 50
./ArtisanCMD.sh OT2 50
./ArtisanCMD.sh IO2 50
./ArtisanCMD.sh READ
./ArtisanCMD.sh UNITS F
./ArtisanCMD.sh READ 
./ArtisanCMD.sh UNITS C 
./ArtisanCMD.sh READ 
sleep 5
./ArtisanCMD.sh OT1 100
./ArtisanCMD.sh OT2 100 
./ArtisanCMD.sh IO2 100 
sleep 5
./ArtisanCMD.sh OT1 0
./ArtisanCMD.sh OT2 0 
./ArtisanCMD.sh IO2 0

tail -n 22 /var/log/tcx.log
