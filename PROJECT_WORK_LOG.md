# Project Work Log (Unified)

> This log consolidates all major work logs for the Christian Doctrine project. 
> **Instruction:** When adding new entries, categorize them under the appropriate section according to the scope of work (e.g., OCR Utility, Doctrine Editing, General Project Changes). This ensures clarity and traceability for all contributors.

---

## Doctrine of Divine Essence HTML Workflow

**There are to be three HTML files for each doctrine:**
1. **Original Source HTML** – Faithfully transcribed from the original paper or source document. No editorial changes, only digitization and basic structure.
2. **Intermediary (Clean) HTML** – Edited for structure, clarity, and internal consistency. This is the working file for all corrections, formatting, and completeness checks. No WordPress-specific code or features.
3. **WordPress Publish HTML** – Final, production-ready file. Includes all WordPress-specific requirements, navigation, and features. Should match the style and structure of the main Library, Index, and Analytics WordPress files:
    - doctrines_library_wp_publish.html
    - scripture_index_wp_publish.html
    - scripture_analytics_wp_publish.html

> When working on doctrine files, always:
> - Maintain the original source HTML as a reference.
> - Make all edits and corrections in the intermediary (clean) HTML.
> - Only add WordPress navigation, analytics, and deployment features in the publish HTML.
> - Log all major changes and file transitions below.

---

## OCR Utility Development Log

### Purpose
Track all steps, issues, and solutions for the image-to-text OCR utility.

#### Log Entries
- [2026-01-06] User requested an OCR utility to extract text from images and output HTML with matching formatting.
- [2026-01-06] Created ocr_image_to_text.py for extracting text from images using pytesseract and Pillow.
- [2026-01-06] User requested ongoing log for all changes, issues, and solutions for this utility.
- [2026-01-06] Issue encountered: Python virtual environment (venv) creation failed with error CREATE_VENV.VENV_FAILED_CREATION. This blocks isolated package installation for OCR dependencies.
    - Error details: VenvError raised during venv creation script.
    - Next step: Troubleshoot venv creation or consider system-wide install of dependencies.

---

## General Project Change Log

### January 5, 2026
- Added viewport meta tag to doctrines_library_wp_publish.html for proper mobile rendering
- Fixed duplicate <style> tag in scripture_index_wp_publish.html
- Removed on-screen notification system that was showing error messages
- Fixed title visibility - added inline styles with dark mode support
- Hidden WordPress auto-generated page titles to prevent duplicates
- Fixed mobile table display issues (removed conflicting CSS)
- Updated all doctrine links from local paths to full WordPress URLs
- Added ESV API integration for verse excerpt population
- Created populate_scripture_index.py script for batch verse fetching
- Added API usage tracker widget (visible only to admin in browser)
- Cross-page navigation working on all three pages (Library, Index, Analytics)
- Current page shows as non-clickable span
- Full URLs for all inter-page links
- Commented out all console.log statements
- Removed unused showNotification function
- Added comprehensive .gitignore for security
- ESV API Key: Configured and working (2ff0...5465)
- Usage: 182 total requests as of session end
- Limit: 5,000 requests/day
- Strategy: Pre-populate verses server-side to minimize viewer API calls
- Files ready for WordPress upload: doctrines_library_wp_publish.html, scripture_index_wp_publish.html, scripture_analytics_wp_publish.html
- Created: ~/bible_venv (virtual environment)
- Installed: requests library
- API key, scripts, and credentials excluded from git for security

---

## Doctrine Editing & Consolidation Log

### Doctrine of Divine Essence
- [2026-01-05] Initial analysis: 18 HTML fragments concatenated, each with duplicate structure tags.
- [2026-01-05] Created consolidate_doctrine.py to merge fragments, preserving all content and structure.
- [2026-01-05] Ran consolidation: output is doctrine-of-divine-essence_consolidated.html (943 lines, 85KB).
- [2026-01-05] Quality verification: all content preserved, duplicate headers removed, HTML validated.
- [2026-01-05] Created clean_artifacts.py to remove duplicate tags and artifacts from modular construction.
- [2026-01-05] Cleaned file: doctrine-of-divine-essence_cleaned.html (769 lines, 81KB).
- [2026-01-05] Document structure verified: 18 major sections, 52 subsections, responsive design.
- [2026-01-05] Next steps: quality check, fix structure, standardize styling, add references, create WordPress-ready version, integrate into main library.

---

> When adding new entries, always specify the date, scope (OCR, General, Doctrine, etc.), and a concise description of the work or issue.
