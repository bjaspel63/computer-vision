import cv2

img = cv2.imread("sample.jpg")     # Load an image
cv2.imshow("Original Image", img)  # Display it in a window
cv2.waitKey(0)                     # Wait for key press
cv2.destroyAllWindows()           # Close the window
