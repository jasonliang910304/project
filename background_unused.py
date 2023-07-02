import cv2
import numpy as np

# 读取输入图像
image = cv2.imread("cropped.jpg")
height, width = image.shape[:2]

# 创建与图像大小相同的掩码
mask = np.zeros((height, width), dtype=np.uint8)

# 定义前景和背景模型
bgdModel = np.zeros((1, 65), dtype=np.float64)
fgdModel = np.zeros((1, 65), dtype=np.float64)

# 定义感兴趣区域（ROI）为整个图像
rect = (121, 159, 559, 483)

# 初始化背景和前景模型样本
bgdSamples = np.zeros((1, 65), dtype=np.float64)
fgdSamples = np.zeros((1, 65), dtype=np.float64)

# 使用GrabCut算法进行图像分割
cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

# 更新背景和前景模型样本
bgdModel = bgdSamples
fgdModel = fgdSamples

# 将掩码中的可能前景和可能背景设置为对应的前景和背景
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

# 将输入图像与掩码进行按位与操作，提取前景
foreground = cv2.bitwise_and(image, image, mask=mask2)

# 显示结果
cv2.imshow("Input Image", image)
cv2.imshow("GrabCut Foreground", foreground)
cv2.waitKey(0)
cv2.destroyAllWindows()
