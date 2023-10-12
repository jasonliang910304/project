from PyQt6 import QtWidgets, QtGui, QtCore
import sys


def create_car_inform_window():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.setWindowTitle("car_inform")
    Form.resize(400, 200)
    # 设置整个窗口的背景为白色
    Form.setStyleSheet("background-color: white;")

    # 創建lavel:車位資訊
    label = QtWidgets.QLabel(Form)
    label.setText("車位資訊")
    label.move(625, 0)
    label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    # 創建車位資訊的文字大小字型
    font = QtGui.QFont()
    font.setPointSize(50)
    font.setBold(True)
    font.setItalic(True)
    label.setFont(font)

    # 創建lavel1:已停車
    label1 = QtWidgets.QLabel(Form)
    label1.setText("已停車")
    label1.move(205, 100)
    label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    # 創建車位資訊的文字大小字型
    font = QtGui.QFont()
    font.setPointSize(50)
    font.setBold(True)
    font.setItalic(True)
    label1.setFont(font)

    # 創建lavel2:停車中
    label2 = QtWidgets.QLabel(Form)
    label2.setText("停車中")
    label2.move(730, 100)
    label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    # 創建車位資訊的文字大小字型
    font = QtGui.QFont()
    font.setPointSize(50)
    font.setBold(True)
    font.setItalic(True)
    label2.setFont(font)

    # 創建lavel3:未停車
    label3 = QtWidgets.QLabel(Form)
    label3.setText("未停車")
    label3.move(1205, 100)
    label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    # 創建車位資訊的文字大小字型
    font = QtGui.QFont()
    font.setPointSize(50)
    font.setBold(True)
    font.setItalic(True)
    label3.setFont(font)

    # 創建lavel4:車牌號碼
    label4 = QtWidgets.QLabel(Form)
    label4.setText("車牌號碼:")
    label4.move(480, 425)
    label4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    # 創建車位資訊的文字大小字型
    font = QtGui.QFont()
    font.setPointSize(30)
    font.setBold(True)
    font.setItalic(True)
    label4.setFont(font)

    # 創建lavel_img:校徽
    label_img = QtWidgets.QLabel(Form)
    label_img.move(1250, 575)
    img = QtGui.QImage("school.png")  # 讀取圖片
    label_img.setPixmap(QtGui.QPixmap.fromImage(img))  # 加入圖片

    # 创建一个红色圆形
    circle1 = QtWidgets.QWidget(Form)
    circle1.setGeometry(50, 50, 100, 100)
    circle1.move(100, 100)
    circle1.setStyleSheet("background-color: red; border-radius: 50px;")

    # 创建一个黄色圆形
    circle2 = QtWidgets.QWidget(Form)
    circle2.setGeometry(50, 50, 100, 100)
    circle2.move(625, 100)
    circle2.setStyleSheet("background-color: yellow; border-radius: 50px;")

    # 创建一个绿色圆形
    circle3 = QtWidgets.QWidget(Form)
    circle3.setGeometry(50, 50, 100, 100)
    circle3.move(1100, 100)
    circle3.setStyleSheet("background-color: green; border-radius: 50px;")

    # 创建一个車位狀態燈(初始為綠色)
    car_circle = QtWidgets.QWidget(Form)
    car_circle.setGeometry(50, 50, 100, 100)
    car_circle.move(700, 625)
    car_circle.setStyleSheet("background-color: green; border-radius: 50px;")

    # 创建一个透明矩形
    rectangle = QtWidgets.QWidget(Form)
    rectangle.setGeometry(0, 0, 600, 300)
    rectangle.move(460, 300)
    rectangle.setStyleSheet(
        "background-color:  rgba(0, 0, 255, 0);border: 10px solid blue;"
    )

    Form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    create_car_inform_window()
