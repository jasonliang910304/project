import cv2
import os

# 输入文件夹路径
input_folder = "images"
output_folder = "bound"

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的图像文件
for filename in os.listdir(input_folder):
    # 构建图像文件的完整路径
    input_path = os.path.join(input_folder, filename)

    # 使用cv2.imread()加载图像
    img = cv2.imread(input_path)

    # 检查图像数据是否为空
    if img is None:
        print(f"Failed to load image: {filename}")
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 轉成灰階
    img = cv2.bilateralFilter(img, 50, 125, 100)
    output = cv2.Laplacian(img, -1, 3, 5)  # 偵測邊緣
    # 將邊框線加粗
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated_edges = cv2.dilate(output, kernel, iterations=1)
    # cv2.imshow("oxxostudio", dilated_edges)
    # 构建输出图像的完整路径
    output_path = os.path.join(output_folder, filename)

    # 使用cv2.imwrite()保存图像
    cv2.imwrite(output_path, dilated_edges)
