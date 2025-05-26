import cv

# Convert the image to black and white (grayscale)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Show the grayscale image
cv2.imshow("Grayscale", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
