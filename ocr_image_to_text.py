#!/usr/bin/env python3
"""
OCR Utility: Extract Text from Image
Uses pytesseract and Pillow to read text from image files (JPG, PNG, etc.)

Usage:
    python ocr_image_to_text.py /path/to/image.jpg

Outputs extracted text to stdout.
"""

import sys
from pathlib import Path
from PIL import Image
import pytesseract

def ocr_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def main():
    if len(sys.argv) != 2:
        print("Usage: python ocr_image_to_text.py /path/to/image.jpg")
        sys.exit(1)
    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"File not found: {image_path}")
        sys.exit(1)
    text = ocr_image(image_path)
    print(text)

if __name__ == "__main__":
    main()
