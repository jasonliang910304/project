from PIL import Image
from ultralytics import YOLO
import numpy as np
# Load a pretrained YOLOv8n model
model = YOLO("car_letter.pt")

# Run inference on 'bus.jpg'
results = model.predict("new.jpg")  # results list
platex = []
platenum = []
final = []
# Show the results
for r in results:
    #繪出格子
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image
    #len(r.boxes) 共有幾個框框
    #box = r.boxes[0] #第幾個框框
    #print(len(r.boxes))
    
    for num in range(len(r.boxes)):
        box = r.boxes[num]
        #r.names[box.cls[0].item()] 每個框的標籤
        #print("Object type:",r.names[box.cls[0].item()])
        #每個框之座標
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        #print("Coordinates:", cords[0])
        platex.append(cords[0])
        platenum.append(r.names[box.cls[0].item()])
    

a = platex
b = platenum
c = np.lexsort((b,a))

for n in c:
    final.append(platenum[n])
print(final)