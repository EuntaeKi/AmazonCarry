#!/bin/bash

#source /usr/local/bin/virtualenvwrapper.sh
FILE1=/home/pi/Scripts/xavg.pkl
FILE2=/home/pi/Scripts/is_detection.pkl
FILE3=/home/pi/Scripts/detectPress.pkl
FILE4=/home/pi/Scripts/remote.pkl
rm -f $FILE1 $FILE2 $FILE3

workon cv
#python3 /home/pi/Scripts/camera/test.py
python /home/pi/Scripts/camera/detection.py &
#sudo python3 /home/pi/Scripts/setup2.py
sudo node /home/pi/Scripts/webserver.js
