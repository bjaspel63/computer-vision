import cv2  # Import OpenCV, a library for working with images and videos

# Load an image from the same folder as this script
img = cv2.imread("sample.jpg")  # Make sure you have an image named 'sample.jpg'

# Show the image in a window
cv2.imshow("Original Image", img)

# Wait for a key press (0 = wait forever)
cv2.waitKey(0)

# Close all image windows
cv2.destroyAllWindows()
