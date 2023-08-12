import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
image = cv2.imread("rotated.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (25, 25), 0)
sharp = cv2.Laplacian(blurred,-1,1, ksize=5)
sharpened = cv2.addWeighted(gray, 1.5, sharp, -0.5, 0)
cvt=cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
cv2.imwrite("car2.jpg", sharpened)
cv2.imshow("My Image", sharpened)
cv2.waitKey(0)
cv2.destroyAllWindows()


#img_name = "ozim4711k5da1_jpg.rf.e2803a4ed05ab0bbe017bee089d25a07.jpg"
#img = Image.open(img_name)
#text = pytesseract.image_to_string("car1.jpg", lang='eng')
#print(text)