import cv2
import numpy as np
import matplotlib.pyplot as plt

# 讀取圖像
img = cv2.imread("combined_image.png")

# 定義拉普拉斯核心（銳利化濾波器）
kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)

# 使用cv2.filter2D進行卷積，實現銳利化
sharpened_img = cv2.filter2D(img, -1, kernel)

# 顯示銳利化前後的圖像
plt.subplot(1, 2, 1)
plt.imshow(img, cmap="gray")
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(sharpened_img, cmap="gray")
plt.title("Sharpened Image")
plt.axis("off")

plt.show()
cv2.imwrite("store.png", sharpened_img)
