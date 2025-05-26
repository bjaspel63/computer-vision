import cv2

img = cv2.imread("sample.jpg")     # Load an image

# Apply Gaussian Blur to smooth the image
blurred = cv2.GaussianBlur(img, (7, 7), 0) #7,7 = Size of the blur area (must be odd numbers); 0 =Auto-calculate the blur strength.
cv2.imshow("Blurred Image", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
