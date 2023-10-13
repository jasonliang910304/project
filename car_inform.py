from PyQt6 import QtWidgets, QtGui, QtCore
import sys


def create_car_inform_window(state):
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle("car_inform")
    Form.resize(400, 200)
    # 设置整个窗口的背景为白色
    Form.setStyleSheet("background-color: white;")

    # 創建lavel:車位資訊
    Label(625, 0, Form, word="車位資訊", size=50)

    # 創建lavel1:已停車
    Label(205, 100, Form, word="已停車", size=50)

    # 創建lavel2:停車中
    Label(730, 100, Form, word="停車中", size=50)
    # 創建車位資訊的文字大小字型

    # 創建lavel3:未停車
    Label(1205, 100, Form, word="未停車", size=50)

    # 創建lavel4:車牌號碼
    Label(480, 425, Form, word="車牌號碼", size=30)
    # 創建車位資訊的文字大小字型

    # 創建lavel_img:校徽
    label_img = QtWidgets.QLabel(Form)
    label_img.move(1250, 575)
    img = QtGui.QImage("school.png")  # 讀取圖片
    label_img.setPixmap(QtGui.QPixmap.fromImage(img))  # 加入圖片

    # 创建一个红色圆形
    Circle(100, 100, Form, "red")

    # 创建一个黄色圆形
    Circle(625, 100, Form, "yellow")

    # 创建一个绿色圆形
    Circle(1100, 100, Form, "green")

    # 创建一个車位狀態燈(初始為綠色)
    Circle(700, 625, Form, state)

    # 创建一个透明矩形
    rectangle = QtWidgets.QWidget(Form)
    rectangle.setGeometry(0, 0, 600, 300)
    rectangle.move(460, 300)
    rectangle.setStyleSheet(
        "background-color:  rgba(0, 0, 255, 0);border: 10px solid blue;"
    )

    Form.show()
    sys.exit(app.exec())


def Circle(x, y, Form, state):
    circle = QtWidgets.QWidget(Form)
    circle.setGeometry(50, 50, 100, 100)
    circle.move(x, y)
    circle.setStyleSheet("background-color: red; border-radius: 50px;")
    if state == "green":
        circle.setStyleSheet("background-color: green; border-radius: 50px;")
    elif state == "yellow":
        circle.setStyleSheet("background-color: yellow; border-radius: 50px;")
    else:
        circle.setStyleSheet("background-color: red; border-radius: 50px;")
    return circle


def Label(x, y, Form, word, size):
    label = QtWidgets.QLabel(Form)
    label.setText(word)
    label.move(x, y)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    font = Font(size)
    label.setFont(font)
    # 創建車位資訊的文字大小字型


0


def Font(size):
    font = QtGui.QFont()
    font.setPointSize(size)
    font.setBold(True)
    font.setItalic(True)
    return font


if __name__ == "__main__":
    state = "red"
    create_car_inform_window(state)
