from ultralytics import YOLO
import cv2
import numpy as np
from collections import Counter

class car:
        def __init__(self, car_number, mask, xy):
                self.car_number = car_number
                self.mask = mask
                self.xy = xy

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
                        car_number = Car_number_detect(car_plate_crop) # 生成車牌號碼
                        temp = car(car_number, car_mask, r)
                        cars.append(temp)

        return car_number

def Car_mask(frame):
        car_model = YOLO("car_v3_mix.pt")
        results = car_model.predict(frame, verbose = False)
        img = frame.copy()
        r = []
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        box = boxes[0]
                        r = box.xyxy[0].astype(int)
                        car_mask = np.zeros((img.shape[0], img.shape[1]))
                        car_mask[r[1] : r[3], r[0] : r[2]] = 1
                        
                        cv2.namedWindow('car',0)
                        cv2.resizeWindow('car', 800, 450)
                        cv2.imshow('car',car_mask)
                        
                        return car_mask


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


def Parking_area(frame):
        img = frame.copy()
        parking_space_model = YOLO("parking_space_mix_v6.pt")
        results = parking_space_model.predict(img, verbose = False)
        for result in results:
                if result.masks is not None:
                        for j, mask in enumerate(result.masks.data):
                                mask = mask.cpu().numpy()
                                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
                                
                                cv2.namedWindow('test',0)
                                cv2.resizeWindow('test', 800, 450)
                                cv2.imshow('test', mask)
                                
                                return mask
                                

def Space_state(overlap , img):        #車位狀態
        if overlap > 0.65:
                state = "red"
                car_number = Car_info(img)
                
        elif overlap > 0.4 and overlap < 0.65:
                state = "yellow"
                car_number = []
        else:
                state = "green"
                car_number = []
        return state,car_number

def Calculate_overlap(car_mask, area):    #計算覆蓋率
        if area is None:
                overlap = 0
        elif car_mask is None:
                overlap = 0
        else:
                overlap = np.sum(np.logical_and(car_mask, area)) / np.sum(area)
        return overlap

def write_to_txt(data, file_path):
    try:
        # 確保 data 是字符串
        data_str = str(data)
        with open(file_path, "w") as file:
            file.write(data_str)
        print(f"Data written to {file_path} successfully.")
    except Exception as e:
        print(f"Error writing data to {file_path}: {e}")


file_path = "httpd-2.4.58-win64-VS17/Apache24/htdocs/output.txt"
file_path1 = "httpd-2.4.58-win64-VS17/Apache24/htdocs/output1.txt"

number6=[]
number7=[]


def counter_max(array):
        if not array:
                print("原始列表为空")
        else:
                counter = Counter(map(tuple, array))
                most_common_list = max(counter, key=counter.get)
                print("出现最多次的子列表:", most_common_list)
                return  most_common_list

def remove(arr):
        if not arr:
                print("原始列表为空")
        else:
                result_string = ''.join(arr)
                print(result_string)
                return result_string 

def state_read(state,final):
        if state == "red":
                final = final
        else:
                final = None
        return final 

def main():
        not_detect_space = True
        video_path = 'video_real_v3.mp4'
#       url = 'https://192.168.1.101:8080/video'
        capture = cv2.VideoCapture(video_path)
        
        final=[]
        idx = 0
        freq = 5
        if not capture.isOpened():
                print("Can't open camera !")
                exit()
        while True:
                #ret, frame = capture.read()
                idx += 1
                ret = capture.grab()
                if idx % freq == 1:
                        ret, frame = capture.retrieve()
                        cv2.namedWindow('frame',0)
                        cv2.resizeWindow('frame',800,450)
                        cv2.imshow('frame', frame)    #播放影片
                        img = frame.copy()
                        car_area = Car_mask(img)
                        park_area = Parking_area(img)
                        area = Calculate_overlap(car_area, park_area)
                        print(area)
                        state,car_number = Space_state(area,img)
                        final = decide_number(car_number)
                        ans = counter_max(final)
                        real_final = remove(ans)
                        print( state , real_final)

                        real_ans = state_read(state,real_final)
                        #create_car_inform_window(state, real_final)
                        
                        example_data = state
                        example_data1 = real_ans
                        # 调用函数写入数据
                        write_to_txt(example_data, file_path)
                        write_to_txt(example_data1, file_path1)
                        
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
        capture.release()
        cv2.destroyAllWindows()

        

if __name__ == "__main__":
        main()

