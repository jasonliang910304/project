import cv2
import numpy as np
from ultralytics import YOLO
from rembg import remove
from multiprocessing import Process, Queue

model = YOLO("best.pt") #import yolo model
crop = None #avoid error if there no target in camera

def display(taskqueue):
        cv2.namedWindow('output', cv2.WINDOW_AUTOSIZE)

        while True:
                img = taskqueue.get()   #from taskqueue get the img

                #display
                cv2.imshow('output', img)
                cv2.waitKey(100)
#use YOLO to crop the input to make the backgroun remove precisely
def background_remove(frame, crop):
        results = model.predict(frame, device='cpu')
        img = frame.copy()
        for result in results:
                boxes = result.boxes.cpu().numpy()
                if len(boxes) > 0:
                        box = boxes[0]
                        r = box.xyxy[0].astype(int)
                        crop = img[
                        #       up   : down, left : right
                                r[1] : r[3], r[0] : r[2]
                         ]

        if crop is not None:
                bgremoved = remove(crop)

                binary_img = bgremoved[:, :, 3]

                output = np.zeros((img.shape[0], img.shape[1]))
                output[r[1] : r[3], r[0] : r[2]] = binary_img
                return output

        else:
                return np.zeros((img.shape[0], img.shape[1]))
if __name__ == "__main__":
        #for stream webcam
        url = 'https://172.16.0.20:8080/video'  #IP Webcam stream url!! Check they are same before using
        capture = cv2.VideoCapture(url)  # get the video from IP Webcam
        taskqueue = Queue() # creat taskqueue
        #create and run the process
        proc = Process(target=display, args=(taskqueue,))
        proc.start()

        count = 0
        while True:
                if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

                ret, frame = capture.read()
                count += 1
                if count % 30 == 0:
                        taskqueue.put(background_remove(frame, crop))

        capture.release()
        taskqueue.put(None)  # 發送結束信號
        proc.join()
        cv2.destroyAllWindows()
