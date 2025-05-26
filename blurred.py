import cv2

img = cv2.imread("sample.jpg")     # Load an image

blurred = cv2.GaussianBlur(img, (7, 7), 0)
cv2.imshow("Blurred Image", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
