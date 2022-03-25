#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip apt-offline libatlas3-base i2c-tools
sudo pip3 install -r requirements.txt
sudo cp logger.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable logger.service
echo 'Reboot? (y/n)'
read ans
echo $ans
if [ $ans == 'y' ]; then
  sudo reboot
fi
