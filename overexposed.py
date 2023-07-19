import cv2

# 加載照片
overexposed_img = cv2.imread("1.jpg")

# 將照片轉為灰階
gray_img = cv2.cvtColor(overexposed_img, cv2.COLOR_BGR2GRAY)

# 使用直方圖均衡化来改善圖像的對比度和亮度
equalized_img = cv2.equalizeHist(gray_img)

# 顯示結果
cv2.imshow("Overexposed Image", overexposed_img)
cv2.imshow("Equalized Image", equalized_img)
cv2.imwrite("ssss.jpg", equalized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
