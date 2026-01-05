# Bible Doctrines Library

A Python-based project for generating and managing a comprehensive Christian Doctrines Library with scripture references.

## Overview

This project generates three main HTML pages for WordPress:
1. **Doctrines Library** - A searchable, tagged library of Christian doctrines with scripture references
2. **Scripture Index** - A comprehensive index of all scripture references organized by book
3. **Analytics Dashboard** - Statistics on scripture usage, most-cited verses, and doctrine coverage

## Features

### 🔍 Enhanced Search & Filter
- Real-time search across all content
- Filter doctrines by 18 keyword categories
- Instant visual feedback
- Keyboard shortcuts (ESC to clear)

### 🏷️ Keyword Tagging System
- Automatic categorization of doctrines
- 18 theological topics (Salvation, Grace, Christ, etc.)
- Click tags to filter related doctrines
- Visual tag display on each doctrine

### 💡 Verse Preview
- Hover over scripture references to see verse text
- Smart tooltip positioning
- Cached results for performance
- Ready for Bible API integration

### 📊 Analytics Dashboard
- Most-cited books of the Bible
- Most-referenced individual verses
- Doctrine coverage statistics
- Visual data presentation

### 📱 Responsive Design
- Mobile-optimized layouts
- Smooth animations and transitions
- Gradient backgrounds
- Accessible on all devices

## Files

### WordPress-Ready Pages
- `Doctrines/doctrines_library_wp_clean.html` - Main doctrines library page (enhanced)
- `Doctrines/scripture_index_wp_clean.html` - Scripture reference index (with search)
- `Doctrines/scripture_analytics_wp.html` - Analytics dashboard (NEW)

### Python Scripts

**Core Generators:**
- `add_new_doctrines.py` - Add new doctrines to the library
- `fix_missing_links.py` - Fix broken or missing links between doctrines and scriptures
- `generate_scripture_index.py` - Generate the scripture index from doctrine references
- `generate_wp_versions.py` - Generate WordPress-ready HTML versions
- `link_verses_in_doctrines.py` - Link scripture verses within doctrine content

**Enhancement Scripts:**
- `generate_analytics.py` - Create scripture usage analytics dashboard
- `add_search_functionality.py` - Add real-time search/filter to pages
- `add_verse_preview.py` - Add hover tooltips for verse previews
- `add_keyword_tags.py` - Add keyword tagging and topic filtering system

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
