import numpy as np
import cv2

def viewImage(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image = cv2.imread('shot.png')
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# viewImage(hsv_img)

green_low = np.array([45 , 100, 50] )
green_high = np.array([75, 255, 255])
curr_mask = cv2.inRange(hsv_img, green_low, green_high)
hsv_img[curr_mask > 0] = ([75,255,200])
# viewImage(hsv_img) ## 2

## converting the HSV image to Gray inorder to be able to apply 
## contouring
RGB_again = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
gray = cv2.cvtColor(RGB_again, cv2.COLOR_RGB2GRAY)
#viewImage(gray) ## 3

ret, threshold = cv2.threshold(gray, 90, 255, 0)
# viewImage(threshold) ## 4

a, contours,  _ =  cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
from pprint import pprint
pprint(contours)
cv2.drawContours(image, contours, -1, (255, 255, 255), 3)
viewImage(image) ## 5