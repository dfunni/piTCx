#!/bin/bash
./ArtisanCMD.sh CHAN 1200
for ((i=0; i<10; i++))
do
    ./ArtisanCMD.sh READ &
    sleep 1
done

tail -n 11 /var/log/tcx.log