from PIL import Image
import pytesseract
import os

# If running on Windows, set Tesseract path explicitly:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Sample test image
test_image = "SampleImage.png"   # put your sample file in the same folder

if not os.path.exists(test_image):
    print(f"Error: {test_image} not found.")
    exit()

# Load image
img = Image.open(test_image)

# Run OCR
custom_config = r'--oem 3 --psm 6'
extracted_text = pytesseract.image_to_string(img, config=custom_config)

# Print result on screen
print("\n--- OCR RESULT ---\n")
print(extracted_text)

# Save result as .txt file
output_file = "sample_output.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(extracted_text)

print(f"\nOCR result saved to {output_file}")