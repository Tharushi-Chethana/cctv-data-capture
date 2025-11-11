import cv2
import time
import os
from datetime import datetime
from PIL import Image
import pytesseract
import re
import openpyxl
from openpyxl import Workbook


# Configuration
camera_url = "rtsp://admin:" \
"@10.1.8.13:554/stream1"
base_folder = "capturedImages"
os.makedirs(base_folder, exist_ok=True)
excel_path = "CCTV_OCR_Data.xlsx"

# Path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
custom_config = r'--oem 3 --psm 6'


# Function: Extract OCR data from image
def extract_ocr_data(image_path):
    img = Image.open(image_path)

    # Crop coordinates: (left, top, right, bottom)
    job_counter_crop = img.crop((400, 470, 800, 550))
    datetime_crop = img.crop((1930, 410, 2230, 470))
    status_crop = img.crop((2320, 430, 2620, 470))

    # OCR
    job_text = pytesseract.image_to_string(job_counter_crop, config=custom_config)
    datetime_text = pytesseract.image_to_string(datetime_crop, config=custom_config)
    status_text = pytesseract.image_to_string(status_crop, config=custom_config)

    # Clean text
    job_text = job_text.replace('\n', ' ').strip()
    job_text = re.sub(r'^O(?=m)', '0', job_text)
    job_text = re.sub(r'\s+=', ' =', job_text)
    datetime_text = datetime_text.strip()
    status_text = status_text.strip()

    return job_text, datetime_text, status_text

# Function: Save data to Excel
def save_to_excel(job_text, datetime_text, status_text):
    if os.path.exists(excel_path):
        wb = openpyxl.load_workbook(excel_path)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["Captured Time", "Job Counter", "Date & Time (Screen)", "Status"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([now, job_text, datetime_text, status_text])
    wb.save(excel_path)
    print(f"Data saved to {excel_path}")

# Function: Capture a fresh frame from RTSP
def capture_frame():
    cap = cv2.VideoCapture(camera_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Grab latest frame
    time.sleep(2)  # Give camera time to initialize
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Failed to capture frame from camera.")
    return frame

# Main loop
print("Starting 5-minute interval capture... Press Ctrl+C to stop.")

try:
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        daily_folder = os.path.join(base_folder, today)
        os.makedirs(daily_folder, exist_ok=True)

        try:
            frame = capture_frame()
        except RuntimeError as e:
            print(f"{e} Retrying in 10 seconds...")
            time.sleep(10)
            continue

        timestamp = datetime.now().strftime("%I.%M%p")
        filename = os.path.join(daily_folder, f"{timestamp}.png")
        cv2.imwrite(filename, frame)
        print(f"Saved image: {filename}")

        # OCR and save results
        job_text, datetime_text, status_text = extract_ocr_data(filename)
        print(f"OCR Results -> Job: {job_text}, Date/Time: {datetime_text}, Status: {status_text}")
        save_to_excel(job_text, datetime_text, status_text)

        print("Waiting 5 minutes until next capture...\n")
        time.sleep(300)  # 5 minutes

except KeyboardInterrupt:
    print("\nCapture stopped by user.")
finally:
    cv2.destroyAllWindows()