#!/bin/bash
# Make running hot image backup of RaspberryPi
# The resulting image can be restored to SD Card using Etcher or so
# I use it for automated backups using cron

DEST="/mnt/diskstation1-Daten/Backup/PiBackup"

DATE=`date +%Y-%m-%d`
for i in hostname1 hostname2; do
        ssh root@${i} "sudo dd if=/dev/mmcblk0 bs=1M | gzip -" | dd of=${DEST}/pibackup_${i}_${DATE}.gz
done

