import cv2

cap = cv2.VideoCapture(0) # 0 = default webcam

while True:
    ret, frame = cap.read() # Capture frame
    if not ret:
        break
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
