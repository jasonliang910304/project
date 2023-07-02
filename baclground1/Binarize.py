import cv2
import matplotlib.pyplot as plt
from rembg import remove
from PIL import Image
import numpy as np

# Load the background-removed image
img = cv2.imread("img2.png", cv2.IMREAD_UNCHANGED)
# Convert the image to grayscale


# Apply thresholding to convert grayscale to binary image
ret, thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
# Convert BGR to RGB to display using matplotlib
# imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# Display Original, Grayscale, and Binary Images
# plt.subplot(131), plt.imshow(img, cmap="gray"), plt.title(
# "Background-Removed Image"
# ), plt.axis("off")
# plt.subplot(132), plt.imshow(gray, cmap="gray"), plt.title("Grayscale Image"), plt.axis(
# "off"
# )
plt.subplot(133), plt.imshow(thresh, cmap="gray"), plt.title("Binary Image"), plt.axis(
    "off"
)
plt.show()
