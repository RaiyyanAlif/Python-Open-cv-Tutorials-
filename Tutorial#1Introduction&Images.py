
import cv2

img = cv2.imread('logo.png',1)
img = cv2.resize(img,(0,0),fx=2,fy=2)
img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
cv2.imwrite('New_IMG.jpg',img)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
