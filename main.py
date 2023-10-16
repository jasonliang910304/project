from ultralytics import YOLO
import cv2
import numpy as np

class car:
        def __init__(self, car_number, mask, xy):
                self.car_number = car_number
                self.mask = mask
                self.xy = xy

def Display(ret, frame):
        if ret:
                cv2.imshow("hi", frame)
                cv2.waitKey(1)
        else:
                print("display error")

def Car_info(frame, history_detect_number):
        car_model = YOLO("car_v3_mix.pt")
        results = car_model.predict(frame, verbose = False)
        cars = []
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        for box in boxes:
                                final = []
                                xy = box.xyxy[0].astype(int)    #car position
                                car_mask = np.zeros((frame.shape[0], frame.shape[1]))
                                car_mask[xy[1] : xy[3], xy[0] : xy[2]] = 1
                                car_crop = frame[xy[1] : xy[3], xy[0] : xy[2]]
                                car_plate_crop = Car_plate_crop(car_crop)
                                if car_plate_crop is not None:
                                        car_number = Car_number_detect(car_plate_crop)
                                        history_detect_number = Check_length(car_number, history_detect_number)
                                        final = Choose_max(history_detect_number)
                                cars.append(car(final, car_mask, xy))
        return cars

def Car_plate_crop(car_crop):
        car_plate_model = YOLO("car_license_new.pt")
        results = car_plate_model.predict(car_crop, verbose = False)
        car_plate_crop = []
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) == 1: #to avoid the situation that get two car plate in one block(the block that bound the car)
                        box = boxes[0]
                        xy = box.xyxy[0].astype(int)
                                                #   up  : down, left : right
                        car_plate_crop = car_crop[xy[1] : xy[3], xy[0] : xy[2]]
                else:
                        car_plate_crop = None
        return car_plate_crop

def Car_number_detect(car_plate_crop):
        car_number_model = YOLO("car_letter.pt")
        results = car_number_model.predict(car_plate_crop, verbose = False)
        platex = []     #to save the coordinate of detect number(to rearrange the detect number)
        platenum = []   #to save detect number
        car_number = [] #to save the result
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
        return car_number

class each_number:
        def __init__(self, c, times):
                self.c = c
                self.times = times

def Check_length(car_number, history_detect_number):
        if len(car_number) == 6 or len(car_number) == 7:
                Length_correct(car_number, history_detect_number)
        elif len(car_number) == 8:
                if car_number[7].isalpha():
                        car_number.pop()
                        Length_correct(car_number, history_detect_number)
        else:
                car_number = None
        return history_detect_number

def Length_correct(car_number, history_detect_number):
        for i, c in enumerate(car_number):
                if history_detect_number[i] == []:
                        history_detect_number[i].append(each_number(c, 1))
                else:
                        for his_c in history_detect_number[i]:
                                if c == his_c.c:
                                        his_c.times += 1
                                else:
                                        history_detect_number[i].append(each_number(c, 1))
        return history_detect_number

def Choose_max(history_detect_number):
        final = []
        for his_c in history_detect_number:
                max = 0
                output = ""
                for c in his_c:
                        if c.times > max:
                                output = c.c
                final.append(output)
        return final

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
        for parking_space in parking_spaces:
                overlap, car_number = Calculate_overlap(cars, parking_space.area)
                if parking_space.state == "green":
                        if overlap > 0.1:
                                parking_space.state = "yellow"
                                parking_space.car_number = car_number
                        else:
                                parking_space.state = "green"
                                parking_space.car_number = None
                elif parking_space.state == "yellow":
                        if overlap > 0.5:
                                parking_space.state = "red"
                                parking_space.car_number = car_number
                        elif overlap < 0.1:
                                parking_space.state = "green"
                                parking_space.car_number = None
                elif parking_space.state == "red":
                        if overlap < 0.1:
                                parking_space.state = "green"
                                parking_space.car_number = None
                else:
                        print("what the fuck??")
        return parking_spaces

def Calculate_overlap(cars, parking_space_area):
        max = 0
        car_number = []
        for car in cars:
                overlap = np.sum(np.logical_and(car.mask, parking_space_area)) / np.sum(parking_space_area)
                if overlap > max:
                        max = overlap
                        car_number = car.car_number
        return max, car_number

def main():
        video_path = "video_demo_v3.mp4"        #this is for video testing
        #url =  #this is for streaming
        capture = cv2.VideoCapture(video_path)
        not_detect_space = True
        count = 0
        parking_spaces = []
        speed = 10
        history_detect_number = [[] for _ in range(7)]

        while True:
                ret, frame = capture.read()
                count = count + 1
                if not_detect_space:
                        parking_spaces = Parking_space_area(frame)
                        if parking_spaces != []:
                                not_detect_space = False
                        else:
                                print("Cannot find any parking area")
                else:
                        if count % speed == 0:
                                cars = Car_info(frame, history_detect_number)
                                if cars != []:
                                        parking_spaces = Space_state(cars, parking_spaces)
                                else:
                                        print("there's no car")
                                for parking_space in parking_spaces:
                                        print(parking_space.space_number, parking_space.car_number, parking_space.state)
                        elif count % speed != 0:
                                continue
                        Display(ret, frame)

if __name__ == "__main__":
        main()
