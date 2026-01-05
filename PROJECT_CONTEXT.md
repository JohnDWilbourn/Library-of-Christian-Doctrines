# Bible Doctrines Library - Project Context

## Project Overview
A Python-based content management system for generating and maintaining a comprehensive Christian Doctrines Library with bidirectional linking between doctrines and scripture references. The output is WordPress-ready HTML pages with embedded styling.

## Purpose & Intent
- Create a searchable, interconnected library of Christian doctrines
- Provide comprehensive scripture references for each doctrine
- Generate a reverse index showing which doctrines reference each scripture
- Make content easy to publish and maintain on WordPress

## Project Status: COMPLETE ✓ + ENHANCED

### Completed Work
1. **Core Scripts Developed:**
   - `generate_scripture_index.py` - Extracts all scripture references from doctrines and generates organized index
   - `generate_wp_versions.py` - Converts HTML to WordPress-ready format with scoped CSS
   - `link_verses_in_doctrines.py` - Links scripture verses within doctrine content
   - `add_new_doctrines.py` - Tool for adding new doctrines to the library
   - `fix_missing_links.py` - Repairs broken links between doctrines and scriptures

2. **Enhancement Scripts:**
   - `generate_analytics.py` - Generates comprehensive scripture usage statistics and analytics dashboard
   - `add_search_functionality.py` - Adds real-time search/filter to doctrines library and scripture index
   - `add_verse_preview.py` - Implements hover tooltips showing verse text previews
   - `add_keyword_tags.py` - Adds automatic keyword tagging and topic-based filtering system

3. **Production Files Generated:**
   - `Doctrines/doctrines_library_wp_clean.html` - Final WordPress-ready doctrines library with all enhancements
   - `Doctrines/scripture_index_wp_clean.html` - Final WordPress-ready scripture index with search
   - `Doctrines/scripture_analytics_wp.html` - NEW: Analytics dashboard with usage statistics
   - All files include embedded, scoped CSS and JavaScript to avoid WordPress theme conflicts

4. **Features Implemented:**
   - ✅ Enhanced real-time search/filter functionality (doctrines and scripture index)
   - ✅ Scripture analytics with most-cited books, verses, and doctrine statistics
   - ✅ Verse text preview on hover (tooltip system)
   - ✅ Keyword tagging system with 18 topic categories
   - ✅ Topic-based filtering in doctrines library
   - ✅ Responsive design optimized for mobile devices
   - ✅ Keyboard shortcuts (ESC to clear search)
   - ✅ Visual feedback and smooth animations

5. **Supporting Assets:**
   - CSS files for styling customization
   - Images folder with doctrine-related graphics
   - .gitignore configured to exclude intermediate build files
   - README.md with user documentation
   - MIT License for open source distribution

6. **Repository Setup:**
   - Git initialized and configured
   - Pushed to GitHub: https://github.com/JohnDWilbourn/Library-of-Christian-Doctrines
   - Open source under MIT License

## Architecture & Workflow

### File Structure
```
Bible/
├── Doctrines/
│   ├── doctrines_library_wp_clean.html    [PRODUCTION - Main library with enhancements]
│   ├── scripture_index_wp_clean.html      [PRODUCTION - Scripture index with search]
│   ├── scripture_analytics_wp.html        [PRODUCTION - Analytics dashboard]
│   ├── additional-css.txt                  [CSS customizations]
│   ├── bible-doctrines-css.txt            [Main library styling]
│   ├── scripture-index-css.txt            [Index styling]
│   └── Images/                            [Graphics assets]
├── generate_scripture_index.py            [Builds scripture index from doctrines]
├── generate_wp_versions.py                [Creates WordPress-ready HTML]
├── link_verses_in_doctrines.py           [Links verses in content]
├── add_new_doctrines.py                  [Adds new doctrine entries]
├── fix_missing_links.py                  [Repairs broken links]
├── generate_analytics.py                 [NEW: Creates analytics dashboard]
├── add_search_functionality.py           [NEW: Adds search/filter features]
├── add_verse_preview.py                  [NEW: Adds hover verse tooltips]
├── add_keyword_tags.py                   [NEW: Adds keyword tagging system]
├── README.md                             [User documentation]
├── PROJECT_CONTEXT.md                    [This file - full context]
└── LICENSE                               [MIT License]
```

### Content Processing Pipeline
1. **Doctrine Creation/Update** → Use `add_new_doctrines.py` or edit HTML manually
2. **Link Verses** → Run `link_verses_in_doctrines.py` to create internal verse links
3. **Generate Index** → Run `generate_scripture_index.py` to build scripture index
4. **Create WP Version** → Run `generate_wp_versions.py` to generate production files
5. **Fix Issues** → Run `fix_missing_links.py` if links are broken

### Key Features
- **Bidirectional Linking:** Doctrines link to scriptures; scriptures link back to doctrines
- **Real-Time Search:** Instant search/filter across all doctrines and scripture references
- **Keyword Tagging:** 18 topic categories with automatic tagging (Salvation, Grace, Christ, etc.)
- **Topic Filtering:** Click any tag to filter doctrines by theological topic
- **Verse Previews:** Hover over scripture links to see tooltips with verse text
- **Analytics Dashboard:** Comprehensive statistics on scripture usage and most-cited verses
- **Scoped CSS/JavaScript:** All styles and scripts prefixed to avoid WordPress conflicts
- **Responsive Design:** Mobile-friendly layouts with gradient backgrounds
- **Keyboard Shortcuts:** ESC to clear search, smooth animations and transitions
- **Bible Gateway Integration:** Scripture references link to external Bible reader
- **Performance Optimized:** Cached verse lookups, debounced search, minimal DOM manipulation

### CSS Scoping Strategy
- Doctrines library: All styles wrapped in `.doctrines-library` class
- Scripture index: All styles wrapped in `.si-wrapper` class
- This prevents conflicts with WordPress theme styles

## Publishing to WordPress

### Steps:
1. Log into WordPress admin
2. Create new page or edit existing
3. Add Custom HTML block
4. Copy entire contents of `doctrines_library_wp_clean.html`
5. Paste into Custom HTML block
6. Publish/Update page
7. Repeat for scripture index using `scripture_index_wp_clean.html`

### URLs Referenced:
- Back link in scripture index points to: `https://intelligencereport.info/complete-library-of-christian-doctrine/`

## Technical Details

### Python Dependencies
- BeautifulSoup4 (for HTML parsing and manipulation)
- Standard library: re, os, sys, collections

### HTML Structure
- Self-contained: CSS embedded in `<style>` tags
- Tables for data presentation
- Responsive media queries for mobile devices
- Gradient backgrounds for visual appeal

### Scripture Reference Format
- Book + Chapter:Verse format (e.g., "John 3:16")
- Links to Bible Gateway for full text
- Organized by biblical book order (Genesis → Revelation)

## Future Enhancements (Optional)
- [x] Add keyword tagging system for doctrines ✅ COMPLETED
- [x] Implement verse text preview on hover ✅ COMPLETED  
- [x] Build search/filter improvements ✅ COMPLETED
- [x] Add analytics for most-referenced verses ✅ COMPLETED
- [ ] Create doctrine categorization/hierarchy
- [ ] Add export to PDF functionality
- [ ] Integrate live Bible API (ESV/Bible Gateway) for actual verse text
- [ ] Add user annotations/notes system
- [ ] Create mobile app version
- [ ] Add cross-reference suggestions

## Git Workflow

### For Future Updates:
```bash
# After making changes
git add .
git commit -m "Description of changes"
git push

# To pull latest from another machine
git pull origin main
```

### Branches
- `main` - Production-ready code only

## Notes & Context

### Design Decisions:
1. **Embedded CSS**: Chosen over external stylesheets for WordPress portability
2. **Python Scripts**: Automation preferred over manual HTML editing for maintainability
3. **Single-file Output**: Each page is self-contained for easy WordPress deployment
4. **Scoped Selectors**: Prevents WordPress theme interference

### Naming Conventions:
- `*_wp_clean.html` = Final WordPress-ready production files
- `*_wp.html` = Intermediate WordPress versions (not tracked in git)
- `*.html` = Original source files (not tracked in git)

### Content Source:
Doctrines appear to be based on systematic theology, with comprehensive scripture support for each doctrine presented.

## Contact & Maintenance
- **Repository**: https://github.com/JohnDWilbourn/Library-of-Christian-Doctrines
- **License**: MIT License (open source)
- **Maintainer**: John David Wilbourn (johndwilbourn@gmail.com)

---

**Last Updated**: January 5, 2026
**Status**: Production-ready with major enhancements, published to GitHub
**Version**: 2.0 - Enhanced Edition
