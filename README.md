# Bible Doctrines Library

A Python-based project for generating and managing a comprehensive Christian Doctrines Library with scripture references.

## Overview

This project generates two main HTML pages for WordPress:
1. **Doctrines Library** - A searchable library of Christian doctrines with scripture references
2. **Scripture Index** - A comprehensive index of all scripture references organized by book

## Files

### WordPress-Ready Pages
- `Doctrines/doctrines_library_wp_clean.html` - Main doctrines library page
- `Doctrines/scripture_index_wp_clean.html` - Scripture reference index

### Python Scripts
- `add_new_doctrines.py` - Add new doctrines to the library
- `fix_missing_links.py` - Fix broken or missing links between doctrines and scriptures
- `generate_scripture_index.py` - Generate the scripture index from doctrine references
- `generate_wp_versions.py` - Generate WordPress-ready HTML versions
- `link_verses_in_doctrines.py` - Link scripture verses within doctrine content

### Supporting Files
- `Doctrines/additional-css.txt` - Additional CSS styles
- `Doctrines/bible-doctrines-css.txt` - Main CSS for doctrines library
- `Doctrines/scripture-index-css.txt` - CSS for scripture index
- `Doctrines/scripture-index-css-strong.txt` - Enhanced CSS for scripture index

## Usage

### Publishing to WordPress
1. Copy the contents of `Doctrines/doctrines_library_wp_clean.html`
2. Paste into a WordPress Custom HTML block
3. Repeat for `Doctrines/scripture_index_wp_clean.html`

### Updating Content
Run the Python scripts in sequence as needed to regenerate the HTML files after making changes.

## Requirements
- Python 3.x
- BeautifulSoup4 (for HTML parsing)

## License
MIT License - See [LICENSE](LICENSE) file for details.

Feel free to use, modify, and distribute this project for your ministry or educational purposes.
