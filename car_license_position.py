import os
from ultralytics import YOLO
import cv2

# 输入文件夹路径
input_folder = "image"
output_folder_car = "car"
output_folder= "car_license"
model = YOLO("car_license.pt")  # 载入模型
# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(output_folder_car):
    os.makedirs(output_folder_car)
# 遍历输入文件夹中的图像文件
for filename in os.listdir(input_folder):
    # 构建图像文件的完整路径
    input_path = os.path.join(input_folder, filename)
    print(filename)
    # 使用cv2.imread()加载图像
    results = model(input_path)  # 將所有image丟進result
    img = cv2.imread(input_path)
    crop = None  # 初始化用於保存邊界框的變量
    for result in results:
        boxes = result.boxes.cpu().numpy()  # 从GPU（如果存在）移动到CPU，并将其转换为NumPy数组。
        if len(boxes) > 0:  # 只保存一个边界框
            box = boxes[0]  # 从边界框数组中提取第一个边界框
            r = box.xyxy[0].astype(int)  # 并将边界框存储至r这个变量
            crop = img[
                r[1] : r[3], r[0] : r[2]
            ]  # 图片切割:r[1] 是矩形的上边界坐标，r[3]是矩形的下边界坐标，r[0] 是矩形的左边界坐标，r[2]是矩形的右边界坐标。
            crop = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)#先將車牌轉成灰階以利編輯
            #crop = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_AREA)
            # 在图像上绘制边界框和文本
            cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2)  # 画出矩形边界
            cv2.putText(
            img,
            f"Box: ({r[0]}, {r[1]}) ({r[2]}, {r[3]})",  # 文字信息
            (r[0], r[1] - 10),  # 绘制边框的起始位置
            cv2.FONT_HERSHEY_SIMPLEX,  # 字体
            0.9,  # 字体大小
            (0, 255, 0),  # 字体颜色
            2,  # 字体粗细
        )
    # 检查图像数据是否为空
    if img is None:
        print(f"Failed to load image: {filename}")
        continue
    output_path_car = os.path.join(output_folder_car, filename)
    output_path = os.path.join(output_folder, filename)
    cv2.imwrite(output_path_car, img)# 將定位好的車牌保存下來(包括車)
    cv2.imwrite(output_path, crop)# 將定位好的車牌保存下來(只有車牌)