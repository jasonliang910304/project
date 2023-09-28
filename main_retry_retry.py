from ultralytics import YOLO
import cv2
import numpy as np
import time
from flask import Flask, jsonify, current_app

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
        cars = []
        car_number_str = ""
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        for box in boxes:
                                car_number = []
                                xy = box.xyxy[0].astype(int)
                                car_mask = np.zeros((frame.shape[0], frame.shape[1]))
                                car_mask[xy[1] : xy[3], xy[0] : xy[2]] = 1
                                car_crop = frame[xy[1] : xy[3], xy[0] : xy[2]]
                                car_plate_crop = Car_plate_crop(car_crop)
                                if car_plate_crop is not None:
                                        car_number = Car_number(car_plate_crop)
                                        if car_number != []:
                                                car_number_str = "".join(car_number)
                                cars.append(car(car_number_str, car_mask, xy))
        return cars

def Car_plate_crop(car_crop):
        car_plate_model = YOLO("car_license_new.pt")
        results = car_plate_model.predict(car_crop, verbose = False)
        car_plate_crop = None
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:          #not using for because it's impossible to get multiple plate with a car in one photo
                        box = boxes[0]
                        xy = box.xyxy[0].astype(int)
                                                #  up   : down , left  : right
                        car_plate_crop = car_crop[xy[1] : xy[3], xy[0] : xy[2]]
                else:
                        car_plate_crop = None
        return car_plate_crop

def Car_number(car_plate_crop):
        number_model = YOLO("car_letter.pt")
        results = number_model.predict(car_plate_crop, verbose = False)
        platex = []
        platenum = []
        car_number = []
        for result in results:
                for num in range(len(result.boxes)):
                        box = result.boxes[num]
                        coordinates = box.xyxy[0].tolist()
                        coordinates = [round(x) for x in coordinates]
                        platex.append(coordinates[0])
                        platenum.append(result.names[box.cls[0].item()])
        temp = np.lexsort((platenum, platex))
        for i in temp:
                car_number.append(platenum[i])
        #print(car_number)
        return car_number

class parking_space:
        def __init__(self, space_number, car_number, state, area):
                self.space_number = space_number
                self.car_number = car_number
                self.state = state
                self.area = area

def Parking_space_area(frame):
        parking_space_model = YOLO("parking_space_mix_v6.pt")
        results = parking_space_model.predict(frame, verbose = False)
        parking_spaces = []
        for result in results:
                if result.masks is not None:
                        for i, mask in enumerate(result.masks.data):
                                mask = mask.cpu().numpy()
                                #I don't know why the mask size will be wrong without resize
                                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                                parking_spaces.append(parking_space(i, "", "green", mask))
        return parking_spaces

def Space_state(cars, parking_spaces):
        new_parking_spaces = []
        temp = 0
        car_number = []
        for parking_space in parking_spaces:
                for car in cars:
                        overlap = Calculate_overlap(car.mask, parking_space.area)*1.4
                        if overlap > temp:
                                temp = overlap
                                car_number = car.car_number
                        if temp > 0.5:       #means the space is occupied
                                parking_space.state = "red"
                                parking_space.car_number = car_number
                        elif temp < 0.2:     #means the space is avalible
                                parking_space.state = "green"
                                parking_space.car_number = None
                        else:
                                parking_space.state = "yellow"
                                parking_space.car_number = car_number
        return parking_spaces

def Calculate_overlap(car_mask, parking_space_mask):
        overlap = np.sum(np.logical_and(car_mask, parking_space_mask)) / np.sum(parking_space_mask)
        return overlap

def State_show(frame, parking_spaces, cars, overlay):
        for parking_space in parking_spaces:
                if(parking_space.state == "green"):
                        overlay[parking_space.area > 0] = [0, 255, 0]
                elif(parking_space.state == "yellow"):
                        overlay[parking_space.area > 0] = [0, 255, 255]
                elif(parking_space.state == "red"):
                        overlay[parking_space.area > 0] = [0, 0, 255]
                else:
                        overlay[parking_space.area > 0] = [255, 255, 255]
        for car in cars:
                cv2.rectangle(frame, (car.xy[0], car.xy[1]), (car.xy[2], car.xy[3]), (255, 0, 0), thickness=2)
                cv2.putText(frame, car.car_number, (car.xy[0], car.xy[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.addWeighted(overlay, 0.5, frame, 1, 0, frame)
        return frame

app = Flask(__name__)
@app.route('/get_status/<car_number>/<space_state>', methods = ['GET'])
def get_status(car_number, space_state):
        with current_app.app_context():
                status = {
                        "FeatureSetting" : car_number,
                        "Setting1" : space_state
                }
                return jsonify(status)

def main():
        video_path = 'video_real_v3.mp4'                #this is for video test
        #url = 'https://192.168.1.101:8080/video'       #this is for stream
        capture = cv2.VideoCapture(video_path)          #if use stream change to url
        not_detect_space = True
        parking_spaces = []
        overlay = []
        cars = []
        count = 0
        new_frame = None
        while True:
                ret, frame = capture.read()
                count = count + 1
                if not_detect_space:
                        overlay = np.zeros_like(frame, dtype = np.uint8)
                        parking_spaces = Parking_space_area(frame)
                        if parking_spaces != []:
                                not_detect_space = False
                        else:
                                print('Cannot find any parking_area')
                elif (not_detect_space == False):
                        if count % 10 == 0:
                                cars = Car_info(frame)
                                if cars != []:
                                        parking_spaces = Space_state(cars, parking_spaces)
                                        new_frame = State_show(frame, parking_spaces, cars, overlay)
                                else:
                                        print('?')
                                for parking_space in parking_spaces:
                                        print(parking_space.space_number, parking_space.car_number, parking_space.state)
                        elif count % 10 != 0:
                                continue
                                #new_frame = State_show(frame, parking_spaces, cars, overlay)
                        Display(ret, new_frame)

if __name__ == "__main__":
        app.run(host = '0.0.0.0', port = 5000)
        main()
