from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import re
import openpyxl
from openpyxl import Workbook
import os

# --- Load image ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
img_path = "SampleImage2.png"
img = Image.open(img_path)

# --- Crop areas ---
job_counter_crop = img.crop((60, 70, 360, 150))
datetime_crop = img.crop((1350, 20, 1700, 80))
status_crop = img.crop((1760, 40, 2000, 100)) 

# --- OCR ---
custom_config = r'--oem 3 --psm 6'
job_text = pytesseract.image_to_string(job_counter_crop, config=custom_config)
datetime_text = pytesseract.image_to_string(datetime_crop, config=custom_config)
status_text = pytesseract.image_to_string(status_crop, config=custom_config)

# --- Clean OCR text ---
job_text = job_text.replace('\n', ' ').strip()
job_text = re.sub(r'^O(?=m)', '0', job_text)
job_text = re.sub(r'\s+=', ' =', job_text)
datetime_text = datetime_text.strip()
status_text = status_text.strip()

# --- Display results ---
print("Job Counter OCR:", job_text)
print("Date & Time OCR:", datetime_text)
print("Status OCR:", status_text)

# --- Save to Excel ---
excel_path = "CCTV_OCR_Data.xlsx"

if os.path.exists(excel_path):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
else:
    wb = Workbook()
    ws = wb.active
    ws.append(["Job Counter", "Date & Time", "Status"])

ws.append([job_text, datetime_text, status_text])
wb.save(excel_path)
print(f"Data saved to {excel_path}")
