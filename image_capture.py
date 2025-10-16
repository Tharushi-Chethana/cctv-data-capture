import cv2
import time
import os
from datetime import datetime

# RTSP stream with username and password
camera_url = "rtsp://admin:Printcare@12@10.1.8.13:554/stream1"

# Base folder to save captured images
base_folder = "capturedImages"
os.makedirs(base_folder, exist_ok=True)

# Open video stream
cap = cv2.VideoCapture(camera_url)
if not cap.isOpened():
    print("Error: Could not connect to camera.")
    exit()

print("Camera connected. Starting daily capture every 5 minutes...")

try:
    while True:
        # Get today's date for folder
        today = datetime.now().strftime("%Y-%m-%d")
        daily_folder = os.path.join(base_folder, today)
        os.makedirs(daily_folder, exist_ok=True)

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            time.sleep(5)  # retry in 5 seconds
            continue

        # Create timestamp for filename
        timestamp = datetime.now().strftime("%I.%M%p")
        filename = os.path.join(daily_folder, f"{timestamp}.png")

        # Save image
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

        # Wait 5 minutes
        time.sleep(300)  # 5 minutes = 300 seconds

except KeyboardInterrupt:
    print("\nCapture stopped by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
