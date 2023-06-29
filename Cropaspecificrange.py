from ultralytics import YOLO
import cv2
from matplotlib import pyplot as plt

model = YOLO("yolov8n.pt")  # 载入模型
results = model("car5.jpg")  # 将car.jpg丢进result
img = cv2.imread("car5.jpg")  # 将car.jpg载入cv2，并存储为img
crop = None  # 初始化用于保存边界框的变量

for result in results:
    boxes = result.boxes.cpu().numpy()  # 从GPU（如果存在）移动到CPU，并将其转换为NumPy数组。
    if len(boxes) > 0:  # 只保存一个边界框
        box = boxes[0]  # 从边界框数组中提取第一个边界框
        r = box.xyxy[0].astype(int)  # 并将边界框存储至r这个变量
        crop = img[
            r[1] : r[3], r[0] : r[2]
        ]  # 图片切割:r[1] 是矩形的上边界坐标，r[3]是矩形的下边界坐标，r[0] 是矩形的左边界坐标，r[2]是矩形的右边界坐标。
        cv2.imwrite("cropped.jpg", crop)  # 将CROP存为JPG文件的图像
        # 打印边界框坐标
        print("Box Coordinates:", r)

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

# 保存绘制了边界框的图像
cv2.imwrite("annotated_image.jpg", img)

# 使用matplotlib打开保存的图像
annotated_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将图像从BGR转换为RGB
plt.imshow(annotated_img)
plt.axis("off")
plt.show()
