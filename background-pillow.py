from rembg import remove
from PIL import Image

img = Image.open("cropped.jpg")
R = remove(img)
R.save("img1.png")
