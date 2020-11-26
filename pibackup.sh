#!/bin/bash
# Make running hot image backup of RaspberryPi
# The resulting image can be restored to SD Card using Etcher or so
# I use it for automated backups using cron
# (c) Ronny Kröhnert - gituser_rk 2020

DEST=/mnt/path/to/backup/directory # Backup destination path. No trailing slash!
KEEP=3 # Cleanup: how many versions to keep

DATE=`date +%Y-%m-%d`
for i in hostname1 hostname2 another-hostname; do
        # make hot backup of a pi(e)
        ssh root@${i} "sudo dd if=/dev/mmcblk0 bs=1M | gzip -" | dd of=${DEST}/pibackup_${i}_${DATE}.gz
        # cleanup of old backups, only keep the recent 3 versions
        find ${DEST}/pibackup_${i}_*.gz -mtime +${KEEP} -exec rm -f {} \;
done

