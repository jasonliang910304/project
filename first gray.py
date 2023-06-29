from PIL import Image

# 打开图像
image = Image.open("img2.png")

# 将图像转换为灰度图像
gray_image = image.convert("L")

# 显示灰度图像
gray_image.show()

# 保存灰度图像
gray_image.save("gray_img2.png")
