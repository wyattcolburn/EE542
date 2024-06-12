#!/bin/bash
# download opencv and pip
sudo apt-get update
sudo apt-get upgrade
sudo apt install python3-opencv # download openCV for python
sudo apt install python3-pip
# Clone Yolo repo
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
# Install requirements
pip install -r requirements.txt

#copy files into yolov5
cd ..
cp -r yolov5_additions/* yolov5
