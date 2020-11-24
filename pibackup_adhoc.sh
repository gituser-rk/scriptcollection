#!/bin/bash
# Adhoc version - pass RasPi system hostname(s) to script as commandline argument
# (c) Ronny Kröhnert - gituser_rk 2020

DEST='/mnt/diskstation1-Daten/Backup/PiBackup'

if test "$#" -lt 1; then
        echo "Illegal number of parameters. At least one hostname must be provided."
else
        DATE=`date +%Y-%m-%d`
        for i in "$@"; do
                ssh root@${i} "sudo dd if=/dev/mmcblk0 bs=1M | gzip -" | dd of=${DEST}/pibackup_${i}_${DATE}.gz
                echo $i 
        done

fi
