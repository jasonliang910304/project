from ultralytics import YOLO
import cv2
import numpy as np
from flask import Flask, jsonify, current_app

class car:
        def __init__(self, car_number, mask):
                self.car_number = car_number
                self.mask = mask

def Display(ret, frame):
        if ret:
                cv2.imshow('hi', frame)
                cv2.waitKey(1)
        else:
                print('error')

def Car_info(frame):
        #print('car_info')
        car_model = YOLO("car_v3_mix.pt")
        results = car_model.predict(frame, verbose = False)
        img = frame.copy()
        cars = []
        r = []
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        box = boxes[0]
                        r = box.xyxy[0].astype(int)
                        car_mask = np.zeros((img.shape[0], img.shape[1]))
                        car_mask[r[1] : r[3], r[0] : r[2]] = 1
                        car_crop = img[r[1] : r[3], r[0] : r[2]]
                        car_plate_crop = Car_plate_crop(car_crop)
                        car_number = Car_number(car_plate_crop)
                        temp = car(car_number, car_mask)
                        cars.append(temp)

        return cars, r

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
        #print('car_number')
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
                for i in temp:
                        car_number.append(platenum[i])
                print(car_number)
        else:
                car_number = []
                print('no_car_number')
        return car_number

class parking_space:
        def __init__(self, space_number, car_number, state, area):
                self.space_number = space_number
                self.car_number = car_number
                self.state = state
                self.area = area

def Parking_space_area(frame):
        img = frame.copy()
        parking_space_model = YOLO("parking_space_mix_v2.pt")
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
        not_detect_space = True
        video_path = 'video_demo_v2.mp4'
#       url = 'https://192.168.1.101:8080/video'
        capture = cv2.VideoCapture(video_path)
        parking_spaces = []

        while True:
                ret, frame = capture.read()
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
                        cars, r = Car_info(frame)
                        if cars != []:
                                parking_spaces = Space_state(cars, parking_spaces)
                                get_status(parking_spaces[0].car_number, parking_spaces[0].state)
                                #for rectangle
                                if(parking_spaces[0].state == "green"):
                                        cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), thickness=2)
                                elif(parking_spaces[0].state == "yellow"):
                                        cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 255, 255), thickness=2)
                                elif(parking_spaces[0].state == "red"):
                                        cv2.rectangle(frame, (r[0], r[1]), (r[2], r[3]), (0, 0, 255), thickness=2)
                        else:
                                print('?')
                        for parking_space in parking_spaces:
                                print(parking_space.space_number,parking_space.car_number,parking_space.state)
                cv2.addWeighted(overlay, 0.5, frame, 1, 0, frame)
                Display(ret, frame)
if __name__ == "__main__":
        app.run(host = '0.0.0.0', port = 5000)
        main()
