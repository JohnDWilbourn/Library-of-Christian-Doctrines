# OCR Utility Development Log
# ===========================
# Purpose: Track all steps, issues, and solutions for the image-to-text OCR utility
# Project: Bible Doctrines Library - OCR Integration
# Start Date: January 6, 2026

## Project Intent
- Build a utility to extract text from images (JPG, PNG, etc.) and generate faithfully formatted HTML output for integration into the Bible Doctrines Library.
- Maintain a detailed log of all steps, issues, and solutions to help build a guide for what works and what doesn't.

## Log Entries

- [2026-01-06] User requested an OCR utility to extract text from images and output HTML with matching formatting.
- [2026-01-06] Created ocr_image_to_text.py for extracting text from images using pytesseract and Pillow.
- [2026-01-06] User requested ongoing log for all changes, issues, and solutions for this utility.
- [2026-01-06] Issue encountered: Python virtual environment (venv) creation failed with error CREATE_VENV.VENV_FAILED_CREATION. This blocks isolated package installation for OCR dependencies.
	- Error details: VenvError raised during venv creation script.
	- Next step: Troubleshoot venv creation or consider system-wide install of dependencies.

# Add new entries below as work progresses.
