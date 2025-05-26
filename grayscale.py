import cv2

img = cv2.imread("sample.jpg")     # Load an image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert the image to black and white (grayscale)

# Show the grayscale image
cv2.imshow("Grayscale", gray)
cv2.waitKey(0)                     # Wait for key press
cv2.destroyAllWindows()           # Close the window
