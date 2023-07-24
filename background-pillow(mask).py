from rembg import remove
from PIL import Image
import numpy as np

img = Image.open("cropped.png")
R = remove(img)
img = np.array(R)
print("像素值范围：", img.min(), "to", img.max())
R.save("img2.png")
