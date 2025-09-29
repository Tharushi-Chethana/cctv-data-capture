import cv2
import time

# RTSP stream from your CCTV
camera_url = "rtsp://admin:Printcare@12@10.1.8.13:554/stream1"

# Open video stream
cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Error: Could not connect to camera.")
    exit()

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Save image
    filename = f"capture_{frame_count}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Saved {filename}")

    frame_count += 1

    # Wait 5 seconds before capturing next frame
    time.sleep(5)
