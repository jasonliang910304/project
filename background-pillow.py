from rembg import remove
from PIL import Image


img = Image.open("cropped.png")
R = remove(img)
R.save("img2.png")
