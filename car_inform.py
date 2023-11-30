import cv2
import numpy as np


def create_car_inform_window(state, car_number):
    # 创建一个空白画布
    image = np.ones((720, 720, 3), np.uint8) * 255

    # 创建綠色圆形
    cv2.circle(image, (70, 125), 45, (0, 255, 0), -1)

    # 创建黄色圆形
    cv2.circle(image, (290, 125), 45, (0, 255, 255), -1)
    # 创建紅色圆形
    cv2.circle(image, (525, 125), 45, (0, 0, 255), -1)
    # 创建车位状态灯
    if state == "green":
        cv2.rectangle(image, (130, 300), (600, 560), (0, 255, 0), -1)  # 绿色圆形
    elif state == "yellow":
        cv2.rectangle(image, (130, 300), (600, 560), (0, 255, 255), -1)  # 黄色圆形
    else:
        cv2.rectangle(image, (130, 300), (600, 560), (0, 0, 255), -1)  # 红色圆形

    # 添加文字
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(image, "Car Information", (100, 50), font, 2, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(image, "Empty", (130, 130), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, "Parking", (340, 130), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(image, "Ocuppied", (575, 130), font, 0.9, (0, 0, 0), 2, cv2.LINE_AA)
    if car_number is not None:
        cv2.putText(
            image,
            "Car_number:" + " " + car_number,
            (180, 430),
            font,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            image,
            "Car_number:",
            (180, 430),
            font,
            1,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )
    # 显示图像
    cv2.imshow("car_inform", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    state = "red"
    car_number = "gg8888"
    create_car_inform_window(state, car_number)
