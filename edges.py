import cv2

img = cv2.imread("sample.jpg")     # Load an image

edges = cv2.Canny(img, 100, 200) #Finds edges (lines and boundaries); 100, 200: Lower and upper edge detection thresholds
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

