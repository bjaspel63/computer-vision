import cv2

cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read() # Capture frame
    if not ret:
        break
    edges = cv2.Canny(frame, 100, 200) # Apply edge filter
    cv2.imshow("Edge Filter", edges) # Show it


    if cv2.waitKey(1) & 0xFF == ord('q'): # Waits 1 ms; checks if 'q' was pressed
        break

cap.release() #Turns off webcam
cv2.destroyAllWindows()
