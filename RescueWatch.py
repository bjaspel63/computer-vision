import cv2                           #opencv library for working images and videos
import mediapipe as mp               #detect body parts from video
import pyttsx3                       #text to speech library
import speech_recognition as sr      #converting spoken words into text
import threading                     #run multiple parts of your program at the same time
import requests                      #send message
import os                            #create folders to save photos
import logging                       #save messages
from datetime import datetime        #get the current date and time

# pushover
import requests

PUSHOVER_USER_KEY = "ux9g6f7azovx31yxk53mkad15d75j8"
PUSHOVER_API_TOKEN = "a72prp68hpkap7e64dwy43adgb8fnm"

def send_pushover_message(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Pushover notification sent!")
    else:
        print(f"❌ Failed to send pushover notification: {response.text}")

# Test
#send_pushover_message("Emergency alert: Help needed!")


def capture_photo(frame, reason):
    """
    Save a photo locally with timestamp and reason in filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitize reason text for filename
    safe_reason = reason.replace(" ", "_").replace(":", "")
    filename = f"alerts/{safe_reason}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"📸 Photo captured: {filename}")
    
    logging.basicConfig(filename="alerts/log.txt", level=logging.INFO) #log file
    logging.info(f"Pose triggered at ... {timestamp}_{safe_reason}")

def trigger_alert(reason):
    """
    Handle alert by speaking, sending notification, and saving photo.
    """ 
    global last_frame
    print(f"🚨 {reason}")
    threading.Thread(target=engine.say, args=(f"Emergency detected: {reason}",)).start()
    threading.Thread(target=engine.runAndWait).start()
    send_pushover_message(reason)
    if last_frame is not None:
        capture_photo(last_frame, reason)


def listen_for_voice_command():
    """
    Continuously listen for voice commands (like 'help') in a separate thread.
    """
    while True:
        with sr.Microphone() as source:
            try:
                print("🎤 Listening for voice commands...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio).lower()
                print(f"🗣️ Heard: {text}")
                if "help" in text:    #keyword
                    trigger_alert("Voice Command: Help detected")
            except Exception:
                # Ignore errors and continue listening
                continue

# make sure alerts folder exists to save photos
if not os.path.exists("alerts"):
    os.makedirs("alerts")

# initialize text to speech 
engine = pyttsx3.init()

# initialize speech recognizer
recognizer = sr.Recognizer()

# initialize webcam capture
cap = cv2.VideoCapture(0)

# initialize Pose and Hands recognition
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

mp_draw = mp.solutions.drawing_utils

# variable to store the latest frame for photo capture
last_frame = None

# start voice command listener in a background
threading.Thread(target=listen_for_voice_command, daemon=True).start()

print("✅ RescueWatch Started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()  # Capture frame from webcam
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Flip frame horizontally (mirror view)
    last_frame = frame.copy()  # Save a copy for capturing photo if needed
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    # --- Pose Detection ---
    pose_results = pose.process(img_rgb)  # Process pose landmarks
    if pose_results.pose_landmarks:
        # Draw pose landmarks on the frame
        mp_draw.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = pose_results.pose_landmarks.landmark
        # Extract key landmarks: shoulders and hips
        ls = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        rs = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        lh = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        rh = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        # Calculate average Y positions of shoulders and hips
        avg_shoulder_y = (ls.y + rs.y) / 2
        avg_hip_y = (lh.y + rh.y) / 2

        # If shoulder and hip Y positions are close, user may be collapsed/lying down
        if abs(avg_shoulder_y - avg_hip_y) < 0.05:
            trigger_alert("Pose Detection: Possible collapse")
        
        def is_flat_pose(ls, rs, lh, rh):
            shoulder_distance = abs(ls.y - rs.y)
            hip_distance = abs(lh.y - rh.y)
            return shoulder_distance < 0.05 and hip_distance < 0.05


    # Hand Gesture Detection
    hand_results = hands.process(img_rgb)  # Process hand landmarks
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Draw hand landmarks on frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Tips of fingers landmarks ids
            tips = [4, 8, 12, 16, 20]
            fingers = []

            # Thumb: compare x of tip and joint to check if extended
            if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers: compare y of tip and two joints below to check if extended
            for id in range(1, 5):
                if hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = sum(fingers)
            # If all five fingers extended, treat as emergency palm signal
            if total_fingers == 5:
                trigger_alert("Hand Gesture: Palm Detected")
            

    # Show video with landmarks and detection
    cv2.imshow("RescueWatch: AI Emergency Monitor", frame)

    # Press 'q' to quit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#  release camera and close windows
cap.release()
cv2.destroyAllWindows()

'''
pip install opencv-python mediapipe pyttsx3 SpeechRecognition requests pyaudio

pip install pyinstaller
pyinstaller --onefile --noconsole projectcv.py

OpenCV: https://opencv.org/

MediaPipe: https://google.github.io/mediapipe/

pyttsx3 (Text to Speech): https://pyttsx3.readthedocs.io/

SpeechRecognition: https://pypi.org/project/SpeechRecognition/

Requests (HTTP for Python): https://requests.readthedocs.io/

Python threading: https://docs.python.org/3/library/threading.html

Pushover: https://pushover.net

'''
