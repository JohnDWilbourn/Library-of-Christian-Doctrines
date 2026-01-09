# Unified Styling Guide - Match Doctrines Library Appearance

## Goal

Make Divine Decree and Divine Essence pages **visually identical** to the beautiful Doctrines Library page in terms of:
- Colors and gradients
- Text visibility and contrast
- Layout and spacing
- Typography
- Dark mode appearance
- Overall professional polish

## Source of Truth

**Model Page:** Doctrines Library (`doctrines_library_wp_publish.html`)
**Why:** Beautiful colors, excellent text visibility, professional layout

## Complete Unified CSS

Replace the entire `<style>` section in both Divine Decree and Divine Essence pages with this:

```css
<style>
/* ===== WORDPRESS TITLE HIDING ===== */
.entry-title, .page-title, h1.entry-title, .wp-block-post-title {
    display: none !important;
}

/* ===== BASE COLORS - LIGHT MODE ===== */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --bg-tertiary: #f3f4f6;
    --text-primary: #1f2937;
    --text-secondary: #4b5563;
    --text-tertiary: #6b7280;
    --border-color: #e5e7eb;
    --accent-blue: #3b82f6;
    --accent-blue-dark: #2563eb;
    --accent-purple: #8b5cf6;
    --accent-purple-dark: #7c3aed;
}

/* ===== WRAPPER AND CONTAINER ===== */
.bd-wrapper, .doctrine-content-wrapper {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 900px;
    margin: 2em auto;
    padding: 20px;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.8;
}

/* ===== TYPOGRAPHY ===== */
h1 {
    font-size: 2.5em;
    font-weight: 700;
    color: #1a202c;
    text-align: center;
    margin: 0 0 0.5em 0;
    padding: 1em 0;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
}

h2 {
    font-size: 1.8em;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 2.5em;
    margin-bottom: 1em;
    padding-bottom: 0.5em;
    border-bottom: 3px solid var(--accent-blue);
}

h3 {
    font-size: 1.4em;
    font-weight: 600;
    color: var(--text-primary);
    margin-top: 2em;
    margin-bottom: 1em;
}

h4 {
    font-size: 1.2em;
    font-weight: 600;
    color: var(--text-secondary);
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}

p {
    margin: 1em 0;
    color: var(--text-primary);
}

/* ===== LINKS ===== */
a {
    color: var(--accent-blue);
    text-decoration: none;
    font-weight: 500;
    border-bottom: 1px solid #93c5fd;
    transition: all 0.2s ease;
}

a:hover {
    color: var(--accent-blue-dark);
    border-bottom-color: var(--accent-blue);
}

/* ===== LISTS ===== */
ol, ul {
    margin: 1.5em 0;
    padding-left: 2.5em;
}

li {
    margin-bottom: 1em;
    color: var(--text-primary);
}

/* List Style Types */
ol.roman {
    list-style-type: upper-roman;
}

ol.alpha, ol.upper-alpha {
    list-style-type: upper-alpha;
}

ol.lower-alpha {
    list-style-type: lower-alpha;
}

ol.lower-roman {
    list-style-type: lower-roman;
}

ol.decimal, ol.numeric {
    list-style-type: decimal;
}

/* ===== SECTIONS ===== */
.section {
    margin-bottom: 4em;
}

hr {
    margin: 3em 0;
    border: none;
    border-top: 2px solid var(--border-color);
}

/* ===== NAVIGATION (Cross-Page Links) ===== */
.page-nav, .cross-nav {
    margin: 1.5em 0;
    padding: 1em;
    background: linear-gradient(to right, #eff6ff, #dbeafe);
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.page-nav-links {
    display: inline-flex;
    gap: 1em;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
}

/* Navigation Button Base Style */
.page-nav a, .cross-nav a {
    display: inline-block;
    padding: 0.5em 1.2em;
    color: white;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
    border-bottom: none !important;
}

.page-nav a:hover, .cross-nav a:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

/* Current Page Indicator */
.current-page {
    display: inline-block;
    padding: 0.5em 1em;
    font-weight: 600;
    color: #1e40af;
    background: white;
    border-radius: 8px;
    border: 2px solid var(--accent-blue);
}

/* ===== NAVIGATION COLOR SCHEME ===== */
/* These match the Doctrines Library 5-page navigation */
.nav-doctrines-library {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.nav-scripture-index {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.nav-analytics {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.nav-divine-essence {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.nav-divine-decree {
    background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
}

/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1f2937;
        --bg-secondary: #374151;
        --bg-tertiary: #4b5563;
        --text-primary: #f3f4f6;
        --text-secondary: #d1d5db;
        --text-tertiary: #9ca3af;
        --border-color: #4b5563;
        --accent-blue: #60a5fa;
        --accent-blue-dark: #93c5fd;
    }

    body {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    .bd-wrapper, .doctrine-content-wrapper {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }

    h1 {
        color: #f7fafc;
        text-shadow: 2px 2px 12px rgba(255,255,255,0.3), 0 0 20px rgba(147,197,253,0.4);
    }

    h2 {
        color: var(--text-primary);
        border-bottom-color: var(--accent-blue);
    }

    h3, h4 {
        color: var(--text-secondary);
    }

    p, li {
        color: var(--text-primary);
    }

    a {
        color: var(--accent-blue);
        border-bottom-color: #3b82f6;
    }

    a:hover {
        color: var(--accent-blue-dark);
        border-bottom-color: var(--accent-blue);
    }

    .page-nav, .cross-nav {
        background: linear-gradient(to right, #1e3a8a, #1e40af);
    }

    .current-page {
        color: #93c5fd;
        background: var(--bg-secondary);
        border-color: var(--accent-blue);
    }

    hr {
        border-top-color: var(--border-color);
    }
}

/* ===== RESPONSIVE - MOBILE ===== */
@media (max-width: 768px) {
    .doctrine-content-wrapper, .bd-wrapper {
        padding: 10px;
        font-size: 16px;
        margin: 1em auto;
    }

    h1 {
        font-size: 1.8em;
    }

    h2 {
        font-size: 1.4em;
    }

    h3 {
        font-size: 1.2em;
    }

    h4 {
        font-size: 1.1em;
    }

    .page-nav, .cross-nav {
        padding: 0.75em;
    }

    .page-nav a, .cross-nav a {
        padding: 0.4em 1em;
        font-size: 0.9em;
    }
}

/* ===== PRINT STYLES ===== */
@media print {
    .page-nav, .cross-nav,
    .cross-ref-toggle, .cross-ref-panel {
        display: none !important;
    }

    body {
        background: white;
        color: black;
    }

    a {
        color: black;
        text-decoration: underline;
        border-bottom: none;
    }
}
</style>
```

## Navigation HTML Structure

Replace the navigation section with this **standardized 5-page navigation**:

```html
<!-- Cross-Page Navigation -->
<div class="page-nav">
    <div class="page-nav-links">
        <a href="https://intelligencereport.info/complete-library-of-christian-doctrine/" class="nav-doctrines-library">📖 Doctrines Library</a>
        <a href="https://intelligencereport.info/comprehensive-biblical-reference-guide/" class="nav-scripture-index">📑 Scripture Index</a>
        <a href="https://intelligencereport.info/scripture-analytics/" class="nav-analytics">📊 Analytics</a>
        <a href="https://intelligencereport.info/doctrine-of-divine-essence/" class="nav-divine-essence">✨ Divine Essence</a>
        <a href="https://intelligencereport.info/doctrine-of-the-divine-decree/" class="nav-divine-decree">⚖️ Divine Decree</a>
    </div>
</div>
```

**For Divine Essence page:** Make Divine Essence the current page:
```html
<span class="current-page">✨ Divine Essence</span>
<!-- Change the link to: -->
<a href="https://intelligencereport.info/doctrine-of-divine-essence/" class="nav-divine-essence">✨ Divine Essence</a>
```

**For Divine Decree page:** Make Divine Decree the current page:
```html
<span class="current-page">⚖️ Divine Decree</span>
```

## Page Title

Replace the page title with this unified format:

```html
<h1 style="color: #1a202c !important; text-align: center !important; font-size: 2.5em !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important; padding: 1em 0 !important; margin: 0 0 0.5em 0 !important; font-weight: 700 !important;">
    The Doctrine of the Divine Decree
</h1>

<!-- Dark mode support for title -->
<style>
@media (prefers-color-scheme: dark) {
    h1[style*="Doctrine of the Divine Decree"] {
        color: #f7fafc !important;
        text-shadow: 2px 2px 12px rgba(255,255,255,0.3), 0 0 20px rgba(147,197,253,0.4) !important;
    }
}
</style>
```

**For Divine Essence page:**
```html
<h1 style="color: #1a202c !important; text-align: center !important; font-size: 2.5em !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important; padding: 1em 0 !important; margin: 0 0 0.5em 0 !important; font-weight: 700 !important;">
    The Doctrine of the Divine Essence
</h1>

<!-- Dark mode support for title -->
<style>
@media (prefers-color-scheme: dark) {
    h1[style*="Doctrine of the Divine Essence"] {
        color: #f7fafc !important;
        text-shadow: 2px 2px 12px rgba(255,255,255,0.3), 0 0 20px rgba(147,197,253,0.4) !important;
    }
}
</style>
```

## Key Styling Improvements

### 1. **Better Text Visibility**
```css
/* Light mode - dark text on white */
--text-primary: #1f2937;  /* Very dark gray, excellent contrast */

/* Dark mode - light text on dark */
--text-primary: #f3f4f6;  /* Very light gray, excellent contrast */
```

### 2. **Modern Typography**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```
**Benefits:**
- Native system fonts (fast loading)
- Professional appearance
- Excellent readability
- Consistent with modern web standards

### 3. **Enhanced Headings**
```css
h2 {
    border-bottom: 3px solid var(--accent-blue);  /* Thicker, more visible */
    padding-bottom: 0.5em;
}
```

### 4. **Smooth Transitions**
```css
transition: all 0.2s ease;  /* On all interactive elements */
```

### 5. **Consistent Spacing**
```css
line-height: 1.8;  /* Comfortable reading */
margin: 1em 0;     /* Standard vertical rhythm */
```

## Color Palette Reference

### Light Mode
| Element | Color | Hex | Use |
|---------|-------|-----|-----|
| Background | White | `#ffffff` | Main page background |
| Text Primary | Dark Gray | `#1f2937` | Body text, headings |
| Text Secondary | Medium Gray | `#4b5563` | Subheadings |
| Text Tertiary | Light Gray | `#6b7280` | Metadata, captions |
| Accent Blue | Bright Blue | `#3b82f6` | Links, buttons, borders |
| Border | Very Light Gray | `#e5e7eb` | Separators, rules |

### Dark Mode
| Element | Color | Hex | Use |
|---------|-------|-----|-----|
| Background | Dark Gray | `#1f2937` | Main page background |
| Text Primary | Very Light Gray | `#f3f4f6` | Body text, headings |
| Text Secondary | Light Gray | `#d1d5db` | Subheadings |
| Accent Blue | Light Blue | `#60a5fa` | Links, buttons |
| Border | Medium Gray | `#4b5563` | Separators, rules |

### Navigation Gradients
| Page | Gradient | Use |
|------|----------|-----|
| Doctrines Library | Blue: `#3b82f6` → `#2563eb` | Main hub |
| Scripture Index | Green: `#10b981` → `#059669` | Verse lookup |
| Analytics | Purple: `#8b5cf6` → `#7c3aed` | Statistics |
| Divine Essence | Orange: `#f59e0b` → `#d97706` | Attribute doctrine |
| Divine Decree | Pink: `#ec4899` → `#db2777` | Sovereignty doctrine |

## Implementation Checklist

### For Divine Decree Page

- [ ] Replace entire `<style>` section with unified CSS above
- [ ] Update page title HTML to match format
- [ ] Replace navigation with standardized 5-page nav
- [ ] Mark "Divine Decree" as current page in navigation
- [ ] Remove any old custom styles that conflict
- [ ] Test in light mode - verify text visibility
- [ ] Test in dark mode - verify all colors work
- [ ] Test navigation hover effects
- [ ] Verify mobile responsive (768px breakpoint)
- [ ] Test in WordPress Custom HTML block

### For Divine Essence Page

- [ ] Replace entire `<style>` section with unified CSS above
- [ ] Update page title HTML to match format
- [ ] Replace navigation with standardized 5-page nav
- [ ] Mark "Divine Essence" as current page in navigation
- [ ] Remove any old custom styles that conflict
- [ ] Test in light mode - verify text visibility
- [ ] Test in dark mode - verify all colors work
- [ ] Test navigation hover effects
- [ ] Verify mobile responsive (768px breakpoint)
- [ ] Test in WordPress Custom HTML block

## Before and After Comparison

### Before (Inconsistent Styling)
- ❌ Different fonts across pages
- ❌ Varying heading sizes
- ❌ Inconsistent colors
- ❌ Different navigation styles
- ❌ Varying text contrast
- ❌ Inconsistent spacing

### After (Unified Styling)
- ✅ Same modern font family
- ✅ Consistent heading hierarchy
- ✅ Unified color palette
- ✅ Standardized 5-page navigation
- ✅ Excellent text visibility (light & dark)
- ✅ Consistent spacing and rhythm

## Testing Protocol

### Visual Comparison Test
1. Open Doctrines Library page in one browser tab
2. Open Divine Decree page in another tab
3. Open Divine Essence page in a third tab
4. Switch between tabs quickly
5. **Should look nearly identical** in:
   - Font style and sizes
   - Colors and contrast
   - Navigation appearance
   - Overall layout
   - Spacing and rhythm

### Dark Mode Test
1. Switch OS/browser to dark mode
2. Refresh all three pages
3. Verify:
   - Text is clearly visible (light on dark)
   - Navigation gradient changes appropriately
   - Links are visible (light blue)
   - No elements become invisible
   - Borders are visible but subtle

### Mobile Test
1. Resize browser to 375px width (iPhone SE)
2. Check all three pages
3. Verify:
   - Text remains readable
   - Navigation buttons wrap properly
   - No horizontal scrolling
   - All content accessible
   - Touch targets are adequate (min 44px)

## Common Issues and Fixes

### Issue: Text Hard to Read
**Cause:** Wrong color contrast
**Fix:** Use the CSS variables defined in `:root` - they're optimized for readability

### Issue: Navigation Looks Different
**Cause:** Old inline styles overriding new CSS
**Fix:** Remove old navigation HTML completely, use standardized version

### Issue: Dark Mode Text Invisible
**Cause:** Missing dark mode CSS rules
**Fix:** Ensure `@media (prefers-color-scheme: dark)` section is included

### Issue: Fonts Look Different
**Cause:** Old font-family declaration
**Fix:** Use the modern system font stack in the unified CSS

### Issue: Spacing Feels Off
**Cause:** Inconsistent margins/padding
**Fix:** Use the standard values from unified CSS (1em, 1.5em, 2em rhythm)

## Benefits of Unified Styling

1. **Professional Appearance** - All pages look like part of one cohesive library
2. **Better Readability** - Optimized text contrast and spacing
3. **Consistent UX** - Users know what to expect on each page
4. **Easier Maintenance** - Change once, apply everywhere
5. **Mobile Friendly** - Responsive design works consistently
6. **Accessibility** - High contrast ratios for readability
7. **Print Ready** - Clean print styles included

## Time Estimate

**Per Page:** 30-45 minutes
- Replace CSS: 15 minutes
- Update navigation: 10 minutes
- Test light/dark modes: 10 minutes
- Mobile testing: 10 minutes

**Both Pages:** 1-1.5 hours total

## Priority

**VERY HIGH** - This should be done **before** adding cross-references

**Why:**
- Establishes visual foundation
- Ensures consistency across all features
- Makes testing easier (one style to verify)
- Users expect professional, consistent appearance

---

**Document Version:** 1.0
**Created:** 2026-01-08
**Status:** Ready for implementation
**Priority:** Implement before Phase 0 (Cross-References)
