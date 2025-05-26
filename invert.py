import cv2

img = cv2.imread("sample.jpg")     # Load an image

invert = cv2.bitwise_not(img)
cv2.imshow("Invert Image Color", invert)
cv2.waitKey(0)
cv2.destroyAllWindows()
