import os
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
# 输入文件夹路径
input_folder = "images"
output_folder_car = "car"
output_folder_no= "no_detect_car"
output_folder_license= "license"
model = YOLO("car.pt")  # 载入車子辨識模型
model1 = YOLO("car_license.pt")  # 载入車牌位置辨識模型
# 创建输出文件夹
if not os.path.exists(output_folder_no):
    os.makedirs(output_folder_no)
if not os.path.exists(output_folder_car):
    os.makedirs(output_folder_car)
if not os.path.exists(output_folder_license):
    os.makedirs(output_folder_license)
#先將輸入圖銳利化

#車子分割
for filename in os.listdir(input_folder):
    # 构建图像文件的完整路径
    input_path = os.path.join(input_folder, filename)
    results = model(input_path)  # 將所有image丟進result
    img = cv2.imread(input_path)
    crop = None  # 初始化用於保存邊界框的變量
    for result in results:
        boxes = result.boxes.cpu().numpy()  # 从GPU（如果存在）移动到CPU，并将其转换为NumPy数组。
        if len(boxes) > 0:  # 只保存一个边界框
            box = boxes[0]  # 从边界框数组中提取第一个边界框
            r = box.xyxy[0].astype(int)  # 并将边界框存储至r这个变量
            crop = img[r[1] : r[3], r[0] : r[2]]  
            cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2)  # 画出矩形边界
            output_path_car = os.path.join(output_folder_car, filename)
            cv2.imwrite(output_path_car, crop)# 將定位好的車牌保存下來(只有車牌)
        else:
            #print("no detection",filename)
            output_path_no = os.path.join(output_folder_no, filename)
            cv2.imwrite(output_path_no, img)
            #os.rename(output_path_car,'err' + filename)
    # 检查图像数据是否为空
    if img is None:
        print(f"Failed to load image: {filename}")
        continue
#車牌分割
for file in os.listdir(output_folder_car):
    car = os.path.join(output_folder_car, file)
    rs = model1(car)  # 將所有image丟進result
    image = cv2.imread(car)
    license = None  # 初始化用於保存邊界框的變量
    for result in rs:
        boxes = result.boxes.cpu().numpy()  # 从GPU（如果存在）移动到CPU，并将其转换为NumPy数组。
        if len(boxes) > 0:  # 只保存一个边界框
            box = boxes[0]  # 从边界框数组中提取第一个边界框
            r = box.xyxy[0].astype(int)  # 并将边界框存储至r这个变量
            license = image[
                r[1] : r[3], r[0] : r[2]
            ]  # 图片切割:r[1] 是矩形的上边界坐标，r[3]是矩形的下边界坐标，r[0] 是矩形的左边界坐标，r[2]是矩形的右边界坐标。
            license = cv2.cvtColor(license,cv2.COLOR_BGR2GRAY)#先將車牌轉成灰階以利編輯
            license = cv2.resize(license, (128, 128), interpolation=cv2.INTER_CUBIC)
            output_license = os.path.join(output_folder_license, file)
            cv2.imwrite(output_license, license)# 將定位好的車牌保存下來(只有車牌)
        else:
            #print("no detection",file)
            output_license = os.path.join(output_folder_no, file)
            cv2.imwrite(output_license, image)# 將定位好的車牌保存下來(只有車牌)
    # 检查图像数据是否为空
    if image is None:
        print(f"Failed to load image: {file}")
        continue
#先增強圖片後旋轉

for filename in os.listdir(output_folder_license):
    output_path = os.path.join(output_folder_license, filename)
    img = cv2.imread(output_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2)
    clahe_img = clahe.apply(gray)
    blurred = cv2.GaussianBlur(clahe_img, (9, 9), 0)
    sharpened = cv2.addWeighted(clahe_img, 1.5, blurred, -0.5, 0)
    image = cv2.copyMakeBorder(sharpened, 5, 5, 5, 5, cv2.BORDER_CONSTANT,value=[255,255,255]) # 添加边框
    #image = cv2.copyMakeBorder(image, 5, 5, 5, 5, cv2.BORDER_CONSTANT) # 添加边框
    cv2.imwrite(output_path, image)

for filename in os.listdir(output_folder_license):
    output_path = os.path.join(output_folder_license, filename)
    img = cv2.imread(output_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray) 
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    ret, thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    clone = img.copy()
    cv2.drawContours(clone, cnts, -1, (0, 255, 0), 2)
    for c in cnts:        
        mask = np.zeros(thresh.shape, dtype="uint8")  #依Contours圖形建立mask
        cv2.drawContours(mask, [c], -1, 255, -1) #255        →白色, -1→塗滿
        final = cv2.bitwise_and(thresh, thresh, mask = mask)

        final = cv2.bitwise_not(final)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        img = cv2.erode(final, kernel)     # 先侵蝕，將白色小圓點移除
        #cv2.imshow('oxxostudio2', thresh)   # 侵蝕後的影像
        img = cv2.bitwise_not(img)
        cv2.imwrite(output_path, img)
    

model2 = YOLO("car_letter.pt")

for filename in os.listdir(output_folder_license):
    output_path = os.path.join(output_folder_license, filename)
    results = model2.predict(output_path)  # results list
    platex = []
    platenum = []
    final = []
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

