from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")  # 載入模型
results = model("car.jpg")  # 將car.jpg丟進result
img = cv2.imread("car.jpg")  # 將car.jpg載入cv2，並儲存為img
crop = None  # 初始化用于保存边界框的变量

for result in results:
    boxes = result.boxes.cpu().numpy()  # 從GPU（如果存在）移動到CPU，並將其轉換为NumPy數組。
    if len(boxes) > 0:  # 只保存一個邊界框
        box = boxes[0]  # 從邊界框数组中提取第一個邊界框
        r = box.xyxy[0].astype(int)  # 並將邊界框儲存至r這個變數
        crop = img[
            r[1] : r[3], r[0] : r[2]
        ]  # 圖片切割:r[1] 是矩形的上邊界座標，r[3]是矩形的下邊界座標，r[0] 是矩形的左邊界座標，r[2]是矩形的右邊界座標。
        cv2.imwrite("cropped.jpg", crop)  # 將CROP存為JPG檔的圖片
        # 打印邊界框座標
        print("Box Coordinates:", r)

        # 在圖像視窗顯示出座標值
        cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2)  # 畫出矩形邊界
        # cv2.putText() 函數將位於矩形框上方的文字繪製在圖片上，以顯示邊界框的座標。
        cv2.putText(
            img,
            f"Box: ({r[0]}, {r[1]}) ({r[2]}, {r[3]})",  # 文字信息
            (r[0], r[1] - 10),  # 繪製邊框的起始位置
            cv2.FONT_HERSHEY_SIMPLEX,  # 字體
            0.9,  # 字體大小
            (0, 255, 0),  # 字體顏色
            2,  # 字體粗細
        )

cv2.imshow("Image", img)  # 將IMG 顯示出來
cv2.waitKey(0)
cv2.destroyAllWindows()
