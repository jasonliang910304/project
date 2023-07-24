import cv2

# 读取图像，确保图像是没有透明通道的RGB图像
img = cv2.imread("parking.png")

# 获取图像的高度和宽度
height, width = img.shape[:2]

# 创建一个全新的RGBA图像，其中A通道初始化为全不透明（255）
rgba_img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

# 将A通道初始化为全不透明（255）
rgba_img[:, :, 3] = 255
height, width, channels = rgba_img.shape
# 将图像保存为PNG文件，确保文件扩展名是".png"
cv2.imwrite("parking_with_alpha.png", rgba_img)
print("圖片通道數:", channels)
