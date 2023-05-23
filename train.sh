#!/bin/zsh

yolo task=detect \
mode=train \
model=yolov8s.pt \
data=/mnt/hello/parking_manager/car_bound_dection-1/data.yaml \
epochs=100 \
imgsz=640
