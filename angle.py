import cv2
import numpy as np
'''
from PIL import Image

# 打开图像
image = Image.open("img2gray.jpg")

# 将图像转换为灰度图像
gray_image = image.convert("L")

# 显示灰度图像
gray_image.show()

# 保存灰度图像
gray_image.save("gray_img2.jpg")

import easyocr
reader = easyocr.Reader(["ch_sim","en"])

result = reader.readtext("car2.jpg")
print(result)

import cv2
img = cv2.imread('cropped1.jpg')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); # 轉換前，都先將圖片轉換成灰階色彩
ret, output1 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
output2 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
output3 = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#cv2.imshow('oxxostudio', img)
#cv2.imshow('oxxostudio1', output1)
#cv2.imshow('oxxostudio2', output2)
#cv2.imshow('oxxostudio3', output3)
cv2.imwrite("cropped.jpg", output2)
cv2.waitKey(0)
cv2.destroyAllWindows
'''
#读取图像,做二值化处理
img = cv2.imread ("cropped1.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)
#像素取反, 变成白字黑底 
gray = cv2.bitwise_not(gray) 
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) 
cv2.imshow('thresh', thresh)
#
coords = np.column_stack(np.where(thresh > 0))
print(coords)
#
angle = cv2.minAreaRect(coords)[-1]
print(angle)
#
if angle < -45:
    angle= -(angle)
else:
    angle = (90 - angle)
#
h,w = img.shape[:2]
center = (h//2 , w//2)
print(angle)

M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(img, M, (h, w), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)
cv2.imwrite("rotated.jpg" , rotated)
cv2.putText(rotated, 'Angle: {:.2f} degrees'.format(angle),(10,30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#print('[INFO] angle :{:.3f}'.format(angle))
cv2.imshow('Input', img)
cv2.imshow('Rotated', rotated)

cv2.waitKey(0)
cv2.destroyAllWindows
