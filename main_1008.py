from ultralytics import YOLO
import cv2
import numpy as np
import torch
from flask import Flask

class car:
        def __init__(self, car_number, mask, xy):
                self.car_number = car_number
                self.mask = mask
                self.xy = xy

def Display(ret, frame):
        if ret:
                cv2.imshow('hi', frame)
                cv2.waitKey(1)
        else:
                print('error')

def Car_info(frame):
        car_model = YOLO("car_v3_mix.pt")
        results = car_model.predict(frame, verbose = False)
        img = frame.copy()
        cars = []
        r = []
        car_number=[]
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        box = boxes[0]
                        r = box.xyxy[0].astype(int)
                        car_mask = np.zeros((img.shape[0], img.shape[1]))
                        car_mask[r[1] : r[3], r[0] : r[2]] = 1
                        car_crop = img[r[1] : r[3], r[0] : r[2]]
                        car_plate_crop = Car_plate_crop(car_crop)
                        car_number = Car_number(car_plate_crop) # 生成車牌號碼
                        #realnum = decide_number(car_number)
                        #print(realnum)
                        temp = car(car_number, car_mask, r)
                        cars.append(temp)

        return cars,car_number

def Car_plate_crop(car_crop):
        #print('car_plate_crop')
        car_plate_model = YOLO("car_license_new.pt")
        results = car_plate_model.predict(car_crop, verbose = False)
        car_plate_crop = None
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        box = result.boxes.cpu().numpy()
                        r = box.xyxy[0].astype(int)
                        car_plate_crop = car_crop[r[1] : r[3], r[0] : r[2]]
                else:
                        car_plate_crop = None
        return car_plate_crop

def Car_number(car_plate_crop):
        number_model = YOLO("car_letter.pt")
        platex = []
        platenum = []
        car_number = []
        if car_plate_crop is not None:
                results = number_model.predict(car_plate_crop, verbose = False)
                for result in results:
                        for num in range(len(result.boxes)):
                                box = result.boxes[num]
                                coordinates = box.xyxy[0].tolist()
                                coordinates = [round(x) for x in coordinates]
                                platex.append(coordinates[0])
                                platenum.append(result.names[box.cls[0].item()])
                temp = np.lexsort((platenum, platex))
                arr = np.array(temp)
                arr_num = np.array(platenum)
                car_number = arr_num[arr]
        else:
                car_number = []
        return car_number

def decide_number(car_number):#決定車牌是6或7碼
        if len(car_number) > 5 and len(car_number) < 8 :
                if len(car_number) == 6 :  #若為6碼車牌，皆加入6陣列
                        number6.append(car_number)
                else:   #若為7碼車牌，皆加入7陣列
                        number7.append(car_number)
        if len(number6) > len(number7):
                return number6
        else:
                return number7

def check_num (num):
        first_num = [sublist[0] for sublist in num]
        second_num = [sublist[1] for sublist in num]
        third_num = [sublist[2] for sublist in num]
        forth_num = [sublist[3] for sublist in num]
        fifth_num = [sublist[4] for sublist in num]
        sixth_num = [sublist[5] for sublist in num]
        num1 = max(set(first_num) , key=first_num.count)
        num2 = max(set(second_num) , key=second_num.count)
        num3 = max(set(third_num) , key=third_num.count)
        num4 = max(set(forth_num) , key=forth_num.count)
        num5 = max(set(fifth_num) , key=fifth_num.count)
        num6 = max(set(sixth_num) , key=sixth_num.count)
        if len(num[0])==7:
                seventh_num = [sublist[6] for sublist in num]
                num7 = max(set(seventh_num) , key=seventh_num.count)
                final=[num1,num2,num3,num4,num5,num6,num7]
        else:
                final=[num1,num2,num3,num4,num5,num6]
        return final

class parking_space:
        def __init__(self, space_number, car_number, state, area):
                self.space_number = space_number
                self.car_number = car_number
                self.state = state
                self.area = area

def Parking_space_area(frame):
        img = frame.copy()
        parking_space_model = YOLO("parking_space_mix_v5.pt")
        results = parking_space_model.predict(img, verbose = False)
        parking_spaces = []

        for i, result in enumerate(results):
                if result.masks is not None:
                        for j, mask in enumerate(result.masks.data):
                                mask = mask.cpu().numpy()
                                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                                temp = parking_space(j, "", "Empty", mask)
                                parking_spaces.append(temp)
                                #cv2.imshow('test', mask)        #space mask
        return parking_spaces

def Space_state(cars, parking_spaces):
        for car in cars:
                for i, parking_space in enumerate(parking_spaces):
                        overlap = Calculate_overlap(car.mask, parking_space.area)
                        if overlap > 0.7:
                                parking_spaces[i].state = "red"
                                parking_spaces[i].car_number = car.car_number
                                #print(parking_spaces[i].space_number,parking_spaces[i].car_number,parking_spaces[i].state)
                        elif overlap > 0.4 and overlap < 0.7:
                                parking_spaces[i].state = "yellow"
                                parking_spaces[i].car_number = car.car_number
                        else:
                                parking_spaces[i].state = "green"
                                parking_spaces[i].car_number = None
                                #print(parking_spaces[i].space_number,parking_spaces[i].car_number,parking_spaces[i].state)
        return parking_spaces

def Calculate_overlap(car_mask, area):
        overlap = np.sum(np.logical_and(car_mask, area)) / np.sum(area)
        print(overlap)
        return overlap

number6=['xxxxxx']
number7=['xxxxxxx']

def main():
        not_detect_space = True
        video_path = 'video_demo_v4.mp4'
#       url = 'https://192.168.1.101:8080/video'
        capture = cv2.VideoCapture(video_path)
        parking_spaces = []
        overlay = []
        while True:
                ret, frame = capture.read()
                Display(ret, frame)
                cars,car_number= Car_info(frame)  #開始生成車牌號碼
                ans = decide_number(car_number)
                final = check_num(ans)
                print(final)


if __name__ == "__main__":
        main()
'''
if not_detect_space:
                        overlay = np.zeros_like(frame, dtype = np.uint8)
                        parking_spaces = Parking_space_area(frame)
                        if parking_spaces != []:
                                not_detect_space = False
                                overlay[parking_spaces[0].area > 0] = [255, 255, 255]
                                #for parking_space in parking_spaces:
                                #        print(parking_space.space_number,parking_space.car_number,parking_space.state)
                        else:
                                print('please retry')
                else:
                        cars = Car_info(frame)
                        if cars != []:
                                parking_spaces = Space_state(cars, parking_spaces)
                                #state show
                                for i, parking_space in enumerate(parking_spaces):
                                        if(parking_spaces[i].state == "green"):
                                                overlay[parking_spaces[i].area > 0] = [0, 255, 0]
                                        elif(parking_spaces[i].state == "yellow"):
                                                overlay[parking_spaces[i].area > 0] = [0, 255, 255]
                                        elif(parking_spaces[i].state == "red"):
                                                overlay[parking_spaces[i].area > 0] = [0, 0, 255]
                                for j, car in enumerate(cars):
                                        cv2.rectangle(frame, (cars[j].xy[0], cars[j].xy[1]), (cars[j].xy[2], cars[j].xy[3]), (255, 0, 0), thickness=2)
                        else:
                                print('?')
                        for parking_space in parking_spaces:
                                print(parking_space.space_number,parking_space.car_number,parking_space.state)
                cv2.addWeighted(overlay, 0.5, frame, 1, 0, frame)
'''
