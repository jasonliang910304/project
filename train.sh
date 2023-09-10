#!/bin/zsh

yolo task=detect \
mode=train \
model=yolov8n.pt \
data=/mnt/hello/parking_manager/sya-car-1/data.yaml \
epochs=100 \
batch=16 \
imgsz=640 \
workers=8 \
device=0
imgsz=640
