#!/bin/bash

adduser bbb-rec-starter
apt install python3 python3-pip chromium
python3 -m pip install -r requirements.txt

cp bbb-rec-starter.service /usr/lib/systemd/system/
ln -s /usr/lib/systemd/system/bbb-rec-starter.service /etc/systemd/system/multi-user.target.wants/
systemctl daemon-reload
systemctl enable bbb-rec-starter

cp -r bbb_rec_starter /home/bbb-rec-starter/
chown -R bbb-rec-starter:bbb-rec-starter /home/bbb-rec-starter/bbb_rec_starter

