# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bible Doctrines Library - A Python-based content management system for generating WordPress-ready HTML pages for a comprehensive Christian Doctrines Library. The project creates three main outputs:
1. Doctrines Library (searchable, tagged doctrines with scripture references)
2. Scripture Index (reverse lookup of doctrines by scripture)
3. Analytics Dashboard (scripture usage statistics)

## Core Architecture

### File Processing Pipeline

The project uses a sequential pipeline to transform and enhance doctrine content:

1. **Source Content** → Raw doctrine HTML in `Doctrines/` directory
2. **Scripture Linking** → `link_verses_in_doctrines.py` converts text references to ESV.org links
3. **Index Generation** → `generate_scripture_index.py` builds reverse lookup by extracting all scripture references
4. **Analytics Generation** → `generate_analytics.py` creates usage statistics
5. **WordPress Publishing** → Output files (`*_wp_publish.html`, `*_wp_clean.html`) ready for WordPress Custom HTML blocks

### Two-File Output Strategy

Most generators create both:
- `*_wp_publish.html` - Production file with all features
- `*_wp_clean.html` - Alternate version (typically identical or simplified)

Both files are self-contained HTML with embedded CSS/JavaScript to avoid WordPress theme conflicts.

### CSS Scoping

All styles are wrapped in container classes to prevent WordPress conflicts:
- Doctrines library: `.doctrines-library` wrapper
- Scripture index: `.si-wrapper` wrapper
- Analytics: `.analytics-wrapper` wrapper

## Common Development Commands

### Running Core Generators

```bash
# Link scripture references in doctrines (first step)
python3 link_verses_in_doctrines.py

# Generate scripture index from linked doctrines
python3 generate_scripture_index.py

# Generate analytics dashboard
python3 generate_analytics.py

# Fix unlinked scripture references
python3 fix_unlinked_references.py

# Add new doctrines to library
python3 add_new_doctrines.py
```

### Running Enhancement Scripts

```bash
# Add search functionality
python3 add_search_functionality.py

# Add verse preview tooltips
python3 add_verse_preview.py

# Add keyword tagging system
python3 add_keyword_tags.py

# Add Bible API integration
python3 add_bible_api.py

# Add PDF export capability
python3 add_pdf_export.py

# Add PWA (Progressive Web App) support
python3 add_pwa_support.py
```

### Complete Regeneration Workflow

After making changes to doctrines, regenerate all outputs:

```bash
python3 fix_unlinked_references.py
python3 generate_scripture_index.py
python3 generate_analytics.py
```

## Scripture Reference Processing

### Book Name Normalization

The codebase uses `BOOK_ALIASES` dictionaries (in multiple scripts) to normalize Bible book names:
- Abbreviations → Full names (e.g., "Matt" → "Matthew", "1 Cor" → "1 Corinthians")
- Variants → Standard forms (e.g., "Psalm" → "Psalms")

When adding scripture parsing functionality, reuse these dictionaries for consistency.

### Reference Patterns

Scripture references are matched using regex patterns like:
```python
r'\b([123]?\s*[A-Z][a-z]+\.?)\s+(\d+):(\d+)(?:[–—\-](\d+))?'
```

This captures: `Book Chapter:Verse` or `Book Chapter:Verse-Verse`

### ESV.org Link Format

Scripture links use this format:
```
https://www.esv.org/{Book}+{Chapter}:{Verse}
```
Example: `https://www.esv.org/John+3:16`

Spaces in book names are replaced with `+`.

## HTML Structure

### Doctrine Sections

Each doctrine is wrapped in:
```html
<section id="unique-doctrine-id">
  <h2>Doctrine Title</h2>
  <div class="doctrine-content">...</div>
  <div class="doctrine-tags">
    <span class="tag" data-tag="Category">Category</span>
  </div>
</section>
```

### Cross-Reference System

The doctrines library includes a cross-reference panel that:
- Analyzes verse co-occurrence across doctrines
- Shows related verses when a scripture link is clicked
- Stores data in JavaScript object embedded in HTML

Cross-reference data structure:
```javascript
const crossRefData = {
  "John 3:16": [
    {ref: "John 3:17", doctrines: ["Salvation", "Grace"]},
    // ...
  ]
};
```

## WordPress Integration

### Deployment Process

1. Copy contents of `*_wp_publish.html` file
2. In WordPress admin, create/edit page
3. Add Custom HTML block
4. Paste entire HTML contents
5. Publish

### Embedded Resources

All CSS, JavaScript, and some images are embedded in HTML to create self-contained pages. External images are referenced from WordPress media library or CDN.

### Known Constraints

- WordPress may strip some JavaScript if security plugins are active
- Custom HTML blocks preserve all code if properly configured
- Some themes may add conflicting styles (CSS scoping mitigates this)

## Python Environment

### Dependencies

Only one external dependency:
```bash
pip install beautifulsoup4
```

All other imports are from Python standard library: `re`, `pathlib`, `collections`, `html.parser`

### Python Version

Developed with Python 3.12.3, compatible with Python 3.x

### Virtual Environment

Project includes `.venv/` directory (not in git). To recreate:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install beautifulsoup4
```

## Doctrine Organization

### Keyword Tag System

Doctrines are categorized with 18 keyword tags:
- Salvation, Grace, Christ, Holy Spirit, Faith
- Sin, Redemption, Church Age, Eternal Security
- Prayer, Spiritual Growth, Angels, Satan
- Spiritual Warfare, Position in Christ, Doctrine
- History, Prophecy, Sovereignty

Tags are added via `add_keyword_tags.py` and stored inline in doctrine sections.

### Category Headers

Doctrines are grouped by theological category with visual headers:
- Hamartiology (Sin & Redemption)
- Spiritual Life
- Ecclesiology (Church)
- Eschatology & Prophecy
- History & Interpretation

## Working with Individual Doctrines

### Adding New Doctrines

New doctrines can be added in subdirectories like `Doctrines/doctrine-of-divine-essence/`:
1. Create doctrine content files
2. Use helper scripts (`consolidate_doctrine.py`, `format_for_library.py`, `clean_artifacts.py`)
3. Integrate into main library with `add_new_doctrines.py`

### Table of Contents Management

When adding doctrines, update the TOC in the main HTML:
- Located near top of `doctrines_library_wp_publish.html`
- Links use `#section-id` anchors
- Separator: pipe character `|` between links

## Special Features

### Dark Mode Support

The library auto-detects system theme preference using:
```css
@media (prefers-color-scheme: dark) { ... }
```

Both light and dark mode styles are included in the CSS.

### Export Functionality

Individual doctrines can be exported to PDF via browser print dialog:
- Export buttons added to each section heading
- JavaScript temporarily isolates section content for printing
- CSS includes `@media print` rules

### Search Implementation

Real-time search filters visible doctrines/references:
- Debounced input handling
- Case-insensitive matching
- Highlights matching content
- Shows result count
- Keyboard shortcut: ESC to clear

### Verse Preview Tooltips

Hover tooltips show verse text:
- Smart positioning (avoids viewport edges)
- Cached lookups for performance
- Ready for Bible API integration (currently shows placeholder)

## Git Workflow

### Main Branch

All work is done on `main` branch. Files tracked:
- All Python scripts (`.py`)
- Production HTML files (`*_wp_publish.html`, `*_wp_clean.html`)
- Documentation (`.md` files)
- CSS reference files (`.txt` files)
- Images in `Doctrines/Images/`

### Ignored Files

`.gitignore` excludes:
- Virtual environments (`.venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- OS files (`.DS_Store`)
- Temporary files (`*.tmp`, lock files)

### Recent Changes Pattern

Check git log to understand recent work:
```bash
git log --oneline -10
```

Common commit patterns:
- "Mobile rendering fixes, API integration, and security updates"
- "Fix cross-reference system..."
- "Regenerate scripture index to include X new doctrines"

## Troubleshooting

### Missing Scripture References

If scripture index is missing references:
1. Run `fix_unlinked_references.py` to convert plain text to links
2. Run `generate_scripture_index.py` to rebuild index

### Broken Cross-References

Cross-references must have complete verse references (no bare numbers). The system extracts book/chapter context from surrounding text.

### WordPress Display Issues

If features don't work in WordPress:
- Check for JavaScript console errors
- Verify Custom HTML block is used (not regular editor)
- Check if security plugins are stripping scripts
- Verify theme isn't overriding scoped CSS

## Additional Documentation

The repository includes extensive documentation:
- `README.md` - User-facing documentation
- `PROJECT_CONTEXT.md` - Complete project context and history
- `Doctrines/UPDATE_SUMMARY.md` - Recent feature additions
- `ESV_API_COMPLIANCE.md` - Bible API usage guidelines
- `WORDPRESS_DEPLOYMENT.md` - WordPress publishing guide

Refer to these for detailed information on specific features.
