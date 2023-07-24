import cv2
import numpy as np
from ultralytics import YOLO
from matplotlib import pyplot as plt
from rembg import remove

"""
background remove
"""
model = YOLO("parkinggrid.pt")  # import model
results = model("parking.png")  # send car.jpg into results
img = cv2.imread("parking.png")
crop = None  # use for save the output
r = None
for result in results:
    boxes = result.boxes.cpu().numpy()
    if len(boxes) > 0:
        box = boxes[0]
        r = box.xyxy[0].astype(int)
        crop = img[
            #   up   : down, left : right
            r[1] : r[3],
            r[0] : r[2],
        ]

# remove background
bgremoved = remove(crop)
binary_img = bgremoved[:, :, 3]
output = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
output[r[1] : r[3], r[0] : r[2]] = binary_img

# Apply negative effect (Invert colors)
output = 255 - output


# use for test
"""
print(bgremoved)
plt.imshow(output, cmap="gray")
plt.show()
"""


cv2.imwrite("result.png", output)
