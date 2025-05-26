import cv2

img = cv2.imread("sample.jpg")     # Load an image

edges = cv2.Canny(img, 100, 200)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

