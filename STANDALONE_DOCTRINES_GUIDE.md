# Standalone Doctrine Pages Guide

## Overview

The **Doctrine of Divine Essence** and **Doctrine of the Divine Decree** are extensive doctrines that have been generated as standalone WordPress pages with full navigation and interactive features integrated.

## Generated Files

### Doctrine of Divine Essence
- **Consolidated**: `Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html`
- **Standalone WordPress Page**: `Doctrines/doctrine-of-divine-essence_wp_standalone.html`
- **Size**: ~95 KB

### Doctrine of the Divine Decree
- **Consolidated**: `Doctrines/doctrine-of-the-divine-decree/doctrine-of-the-divine-decree_consolidated.html`
- **Standalone WordPress Page**: `Doctrines/doctrine-of-the-divine-decree_wp_standalone.html`
- **Size**: ~84 KB

## Features Included

Both standalone pages include:

✅ **Cross-Page Navigation**
- Links to Doctrines Library
- Links to Scripture Index
- Links to Analytics Dashboard
- Consistent styling with main library

✅ **Search Functionality**
- Real-time search across doctrine content
- Highlights matching sections
- ESC key to clear search
- Visual feedback

✅ **Verse Preview Tooltips**
- Hover over scripture references to see tooltips
- Ready for ESV API integration (currently shows verse reference)

✅ **Responsive Design**
- Mobile-optimized layouts
- Works on all screen sizes
- Touch-friendly navigation

✅ **WordPress-Ready**
- Self-contained HTML (no external dependencies)
- Scoped CSS to avoid theme conflicts
- Copy/paste ready for Custom HTML blocks

## Deployment Instructions

### Step 1: Create WordPress Pages

1. Log into WordPress admin
2. Create two new pages:
   - **Page 1**: "Doctrine of Divine Essence" (or your preferred title)
   - **Page 2**: "Doctrine of the Divine Decree" (or your preferred title)

### Step 2: Add Content

For each page:

1. Open the page editor
2. Add a **Custom HTML** block
3. Open the corresponding `*_wp_standalone.html` file
4. Copy **ALL** content (Ctrl+A, Ctrl+C)
5. Paste into the Custom HTML block (Ctrl+V)
6. **Update/Publish** the page

### Step 3: Update Navigation Links (if needed)

If your WordPress URLs differ from the defaults, edit the navigation section in each standalone file:

```html
<!-- Find this section and update URLs -->
<a href="https://intelligencereport.info/complete-library-of-christian-doctrine/">📖 Doctrines Library</a>
<a href="https://intelligencereport.info/comprehensive-biblical-reference-guide/">📑 Scripture Index</a>
<a href="https://intelligencereport.info/scripture-analytics/">📊 Analytics</a>
```

### Step 4: Link from Main Library

In your main **Doctrines Library** page, add links to these standalone pages:

```html
<a href="[your-wordpress-url]/doctrine-of-divine-essence/">Read Full Doctrine of Divine Essence</a>
<a href="[your-wordpress-url]/doctrine-of-the-divine-decree/">Read Full Doctrine of the Divine Decree</a>
```

## Regenerating Pages

If you need to regenerate the standalone pages after making changes:

```bash
# For Divine Essence
cd /home/johndavid/Projects/Christian-Doctrine
python3 generate_standalone_doctrine_page.py "Doctrine of Divine Essence" \
    Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html \
    Doctrines/doctrine-of-divine-essence_wp_standalone.html

# For Divine Decree
python3 generate_standalone_doctrine_page.py "Doctrine of the Divine Decree" \
    Doctrines/doctrine-of-the-divine-decree/doctrine-of-the-divine-decree_consolidated.html \
    Doctrines/doctrine-of-the-divine-decree_wp_standalone.html
```

## Script Usage

The `generate_standalone_doctrine_page.py` script can be used for any doctrine:

```bash
python3 generate_standalone_doctrine_page.py <doctrine_name> <input_file> [output_file]
```

**Parameters:**
- `doctrine_name`: Display name for the doctrine (used in navigation)
- `input_file`: Path to consolidated HTML file
- `output_file`: (Optional) Output path (defaults to `{input_file}_wp_standalone.html`)

## Integration with Main Library

### Option 1: Summary + Link
In the main doctrines library, show a brief summary with a "Read Full Doctrine" link:

```html
<section id="divine-essence-summary">
    <h2>Doctrine of Divine Essence</h2>
    <p>Brief summary here...</p>
    <p><a href="[url]/doctrine-of-divine-essence/">Read Full Doctrine →</a></p>
</section>
```

### Option 2: Full Integration
If you want to include the full content in the main library later, you can extract the content section from the standalone file and insert it into the main library page.

## Troubleshooting

### Navigation Links Not Working
- Check that URLs match your WordPress site structure
- Ensure pages are published (not drafts)
- Verify permalink settings

### Search Not Working
- Ensure JavaScript is enabled
- Check browser console for errors (F12)
- Verify the search input element exists

### Styling Conflicts
- The CSS is scoped to `.doctrine-standalone-wrapper`
- If conflicts occur, add `!important` to specific rules
- Check WordPress theme CSS for overrides

### Verse Tooltips Not Showing
- Tooltips work on hover over scripture links
- Currently shows verse reference (ESV API integration optional)
- Check that links have `href` attributes with "esv.org" or "biblegateway"

## Next Steps

1. ✅ Review generated standalone pages
2. ✅ Deploy to WordPress
3. ✅ Test navigation links
4. ✅ Add links from main library page
5. ⏳ (Optional) Enable ESV API for verse previews
6. ⏳ (Optional) Add cross-reference data

## Files Generated

```
Doctrines/
├── doctrine-of-divine-essence/
│   ├── doctrine-of-divine-essence_consolidated.html
│   └── doctrine-of-divine-essence_wp_standalone.html
└── doctrine-of-the-divine-decree/
    ├── doctrine-of-the-divine-decree_consolidated.html
    └── doctrine-of-the-divine-decree_wp_standalone.html
```

---

**Generated**: January 2026  
**Script**: `generate_standalone_doctrine_page.py`  
**Status**: ✅ Ready for WordPress deployment
