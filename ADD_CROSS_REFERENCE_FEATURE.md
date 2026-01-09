# Adding Cross-Reference Feature to Individual Doctrine Pages

## Overview

This document explains how to add the beautiful cross-reference button and panel functionality from the Doctrines Library page to individual doctrine pages (Divine Essence and Divine Decree).

## What is the Cross-Reference Feature?

The cross-reference system:
1. **Fixed button** in bottom-right corner labeled "🔗 Cross-References"
2. **Sliding panel** from the right side showing related verses
3. **Interactive hover/click** on scripture links shows related verses
4. **Connection strength** indicators (Strong, Moderate, Weak)
5. **Clickable verse cards** to explore verse relationships
6. **Mobile-responsive** design

## Visual Elements

### Button
- **Position:** Fixed, bottom-right (20px from right, 80px from bottom)
- **Color:** Purple gradient (`#6366f1` to `#4f46e5`)
- **Effect:** Lifts on hover with shadow enhancement
- **Label:** "🔗 Cross-References"

### Panel
- **Slides in from right** (off-screen at -400px, slides to 0px when open)
- **Width:** 380px desktop, 100% mobile
- **Background:** White
- **Contains:** Header with close button (×) and scrollable content area

### Verse Cards
- **Light gray background** (`#f9fafb`)
- **Purple left border** (3px, `#6366f1`)
- **Hover effect:** Shifts left 4px, changes to blue background (`#eff6ff`)
- **Shows:** Verse reference, connection strength, related doctrines

## Implementation Steps

### Step 1: Add HTML Structure

Add these elements **before the closing `</div>` tag** of your main wrapper (just before final `</body>` or end of content):

```html
<!-- Cross-Reference Toggle Button -->
<button class="cross-ref-toggle" id="crossRefToggle">
    �� Cross-References
</button>

<!-- Cross-Reference Sliding Panel -->
<div class="cross-ref-panel" id="crossRefPanel">
    <div class="cross-ref-header">
        <h3 style="margin: 0; color: #4f46e5;">📖 Related Verses</h3>
        <button class="cross-ref-close" id="crossRefClose">×</button>
    </div>
    <div id="crossRefContent">
        <div class="cross-ref-empty">
            Hover over or click a scripture reference to see related verses
        </div>
    </div>
</div>
```

### Step 2: Add CSS Styles

Add this CSS in your `<style>` block (after existing styles):

```css
/* ===== CROSS-REFERENCE SYSTEM ===== */

/* Floating Toggle Button */
.cross-ref-toggle {
    position: fixed;
    right: 20px;
    bottom: 80px;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    border: none;
    padding: 1em 1.5em;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    transition: all 0.3s ease;
    z-index: 9999;
}

.cross-ref-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
}

/* Sliding Panel */
.cross-ref-panel {
    position: fixed;
    right: -400px;
    top: 0;
    width: 380px;
    height: 100vh;
    background: white;
    box-shadow: -4px 0 12px rgba(0, 0, 0, 0.2);
    transition: right 0.3s ease;
    z-index: 9998;
    overflow-y: auto;
    padding: 1.5em;
}

.cross-ref-panel.open {
    right: 0;
}

/* Panel Header */
.cross-ref-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1em;
    padding-bottom: 1em;
    border-bottom: 2px solid #e5e7eb;
}

/* Close Button */
.cross-ref-close {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    color: #6b7280;
    transition: color 0.2s;
}

.cross-ref-close:hover {
    color: #374151;
}

/* Content Area */
#crossRefContent {
    max-height: calc(100vh - 120px);
    overflow-y: auto;
}

/* Verse Cards */
.cross-ref-item {
    padding: 1em;
    margin: 0.5em 0;
    background: #f9fafb;
    border-radius: 8px;
    border-left: 3px solid #6366f1;
    cursor: pointer;
    transition: all 0.2s ease;
}

.cross-ref-item:hover {
    background: #eff6ff;
    border-left-color: #4f46e5;
    transform: translateX(-4px);
}

.cross-ref-verse {
    font-weight: 600;
    color: #4f46e5;
    margin-bottom: 0.25em;
}

.cross-ref-strength {
    font-size: 0.85em;
    color: #6b7280;
}

.cross-ref-doctrines {
    font-size: 0.8em;
    color: #9ca3af;
    margin-top: 0.5em;
    font-style: italic;
}

.cross-ref-empty {
    text-align: center;
    color: #9ca3af;
    padding: 2em;
    font-style: italic;
}

/* Dark Mode Support */
@media (prefers-color-scheme: dark) {
    .cross-ref-panel {
        background: #1f2937;
        color: #f3f4f6;
    }

    .cross-ref-header {
        border-bottom-color: #374151;
    }

    .cross-ref-item {
        background: #374151;
        border-left-color: #6366f1;
    }

    .cross-ref-item:hover {
        background: #1e3a8a;
    }

    .cross-ref-verse {
        color: #93c5fd;
    }

    .cross-ref-close:hover {
        color: #f3f4f6;
    }
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .cross-ref-panel {
        width: 100%;
        right: -100%;
    }

    .cross-ref-toggle {
        bottom: 20px;
        right: 10px;
        padding: 0.8em 1.2em;
        font-size: 0.9em;
        z-index: 10000;
        -webkit-tap-highlight-color: rgba(99, 102, 241, 0.3);
    }

    .cross-ref-panel.open {
        right: 0;
    }

    #crossRefContent {
        max-height: calc(100vh - 100px);
    }
}
```

### Step 3: Add ESV API Configuration (Optional but Recommended)

Add your ESV API key to enable live verse text in tooltips and cross-reference panel:

```javascript
<script>
// ESV API Configuration
const ESV_API_KEY = '2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465'; // Your john-wilbourn account key
const ESV_API_URL = 'https://api.esv.org/v3/passage/text/';

// Fetch verse text from ESV API with caching
async function fetchVerseText(reference) {
    try {
        // Check 30-day cache first
        const cached = localStorage.getItem(`verse_${reference}`);
        if (cached) {
            const data = JSON.parse(cached);
            if (Date.now() - data.timestamp < 30 * 24 * 60 * 60 * 1000) {
                return data.text;
            }
        }

        // Fetch from ESV API
        const url = `${ESV_API_URL}?q=${encodeURIComponent(reference)}&include-passage-references=false&include-verse-numbers=false&include-footnotes=false&include-headings=false`;

        const response = await fetch(url, {
            headers: { 'Authorization': `Token ${ESV_API_KEY}` }
        });

        if (!response.ok) throw new Error(`API error: ${response.status}`);

        const data = await response.json();
        const verseText = data.passages[0].trim();

        // Cache for 30 days
        localStorage.setItem(`verse_${reference}`, JSON.stringify({
            text: verseText,
            timestamp: Date.now()
        }));

        return verseText;
    } catch (error) {
        console.error('Error fetching verse:', error);
        return `${reference} - Click to view on ESV.org`;
    }
}
</script>
```

**Benefits:**
- ✅ Shows actual verse text in cross-reference panel
- ✅ 30-day caching reduces API calls
- ✅ Graceful fallback if API fails
- ✅ Complies with ESV rate limits (5,000/day)

**See also:** [`ESV_API_KEY_REFERENCE.md`](./ESV_API_KEY_REFERENCE.md) for complete API documentation

### Step 4: Add Cross-Reference Data

Create a `crossRefData` JavaScript object with verse relationships. This will be **page-specific**.

**For Divine Decree:**
Extract verses from the Divine Decree page and create relationships based on doctrinal themes.

**For Divine Essence:**
Extract verses from the Divine Essence page and create relationships.

```javascript
<script>
(function() {
    // Cross-reference data - CUSTOMIZE FOR EACH PAGE
    const crossRefData = {
        'John 3:16': [
            {'verse': '1 John 2:2', 'strength': 9},
            {'verse': '2 Cor. 5:21', 'strength': 5},
            {'verse': 'Deut. 4:39', 'strength': 4},
            {'verse': 'Ps. 19:9', 'strength': 4}
        ],
        'Rom. 8:28': [
            {'verse': 'Eph. 1:11', 'strength': 7},
            {'verse': 'Phil. 2:13', 'strength': 5},
            {'verse': 'Ps. 2:7', 'strength': 3}
        ]
        // Add more verses...
    };

    // Doctrine name mapping for "In: X doctrine" labels
    const doctrineData = {
        'John 3:16': ['Salvation', 'Divine Love', 'Grace'],
        'Rom. 8:28': ['Providence', 'Sovereignty']
        // Add more...
    };

    // UI elements
    const panel = document.getElementById('crossRefPanel');
    const toggle = document.getElementById('crossRefToggle');
    const close = document.getElementById('crossRefClose');
    const content = document.getElementById('crossRefContent');

    // Toggle panel visibility
    toggle.addEventListener('click', () => {
        panel.classList.toggle('open');
    });

    close.addEventListener('click', () => {
        panel.classList.remove('open');
    });

    // Show cross-references for a verse
    function showCrossReferences(verse) {
        try {
            if (!crossRefData || !doctrineData) {
                content.innerHTML = '<div class="cross-ref-empty">Error: Data not loaded</div>';
                return;
            }

            const refs = crossRefData[verse];

            if (!refs || refs.length === 0) {
                content.innerHTML = `
                    <div class="cross-ref-empty">
                        <strong>${verse}</strong><br><br>
                        No cross-references found for this verse in this doctrine.
                    </div>
                `;
                panel.classList.add('open');
                return;
            }

            // Sort by strength (highest first)
            const sortedRefs = refs.sort((a, b) => b.strength - a.strength);

            let html = `<h4 style="color: #6366f1; margin-bottom: 1em;">${verse}</h4>`;

            sortedRefs.forEach(ref => {
                const strengthLabel = ref.strength >= 7 ? '🔗 Strong' :
                                     ref.strength >= 4 ? '🔗 Moderate' :
                                     '🔗 Weak';
                const relatedDoctrines = doctrineData[ref.verse] || [];

                html += `
                    <div class="cross-ref-item" onclick="showCrossReferences('${ref.verse}')">
                        <div class="cross-ref-verse">${ref.verse}</div>
                        <div class="cross-ref-strength">${strengthLabel} (${ref.strength} connection${ref.strength > 1 ? 's' : ''})</div>
                        ${relatedDoctrines.length > 0 ?
                            `<div class="cross-ref-doctrines">In: ${relatedDoctrines.join(', ')}</div>` : ''}
                    </div>
                `;
            });

            content.innerHTML = html;
            panel.classList.add('open');
        } catch (error) {
            content.innerHTML = `<div class="cross-ref-empty">Error: ${error.message}</div>`;
        }
    }

    // Add hover/click listeners to all scripture links
    document.querySelectorAll('a[href*="esv.org"], a[href*="biblegateway"]').forEach(link => {
        // Parse verse reference from link text or URL
        const verseText = link.textContent.trim();

        // Highlight if has cross-references
        if (crossRefData[verseText]) {
            link.style.position = 'relative';
            link.setAttribute('data-has-crossref', 'true');
        }

        // Click: Show cross-references
        link.addEventListener('click', (e) => {
            if (crossRefData[verseText]) {
                e.preventDefault();
                showCrossReferences(verseText);
            }
        });

        // Hover preview: Show cross-reference indicator
        link.addEventListener('mouseenter', () => {
            if (crossRefData[verseText] && !panel.classList.contains('open')) {
                toggle.style.transform = 'scale(1.1)';
                toggle.innerHTML = `🔗 ${crossRefData[verseText].length} related`;
            }
        });

        link.addEventListener('mouseleave', () => {
            toggle.style.transform = 'scale(1)';
            toggle.innerHTML = '🔗 Cross-References';
        });
    });

    console.log(`✓ Cross-reference engine enabled with ${Object.keys(crossRefData).length} verses`);
})();
</script>
```

### Step 4: Generate Cross-Reference Data

**Option A: Manual Creation (Recommended for Divine Essence & Decree)**

1. List all scripture references in the document
2. Group verses by theological theme
3. Assign connection strengths:
   - **10:** Verses about exact same concept
   - **7-9:** Verses about closely related concepts
   - **4-6:** Verses about related but distinct concepts
   - **2-3:** Verses tangentially related

**Example for Divine Decree:**

```javascript
const crossRefData = {
    // Divine Decree verses
    'Ps. 2:7': [
        {'verse': 'Dan. 9:24', 'strength': 8},  // Both about divine decree
        {'verse': 'Ps. 148:6', 'strength': 7},
        {'verse': 'Eph. 1:4-6', 'strength': 9}, // Election
        {'verse': 'Rom. 8:28', 'strength': 8}   // All things work together
    ],
    'Eph. 1:4-6': [
        {'verse': 'Ps. 2:7', 'strength': 9},
        {'verse': '2 Tim. 1:9', 'strength': 8},
        {'verse': '1 Pet. 1:2', 'strength': 7}
    ],
    'Rom. 8:28': [
        {'verse': 'Eph. 1:11', 'strength': 9},
        {'verse': 'Ps. 2:7', 'strength': 8},
        {'verse': 'Phil. 2:13', 'strength': 6}
    ]
    // Add all verses from Divine Decree...
};
```

**Option B: Use Existing Doctrines Library Data**

Since the Doctrines Library already has 937 cross-reference relationships, you can:

1. Extract the `crossRefData` from `doctrines_library_wp_publish.html`
2. Filter to include only verses present in Divine Decree/Essence
3. Paste the filtered subset into your page

**Quick Script to Extract Relevant Verses:**

```bash
# Extract verses from a specific doctrine page
grep -oE '<a[^>]*href="[^"]*esv\.org[^"]*"[^>]*>[^<]+</a>' divine-decree_wp_publish.html | \
  sed 's/.*>\([^<]*\)<.*/\1/' | sort -u
```

### Step 5: Add ESV Copyright Notice

**REQUIRED if using ESV API:** Add this copyright notice to your page:

```html
<!-- ESV Copyright Notice (required when displaying ESV text) -->
<div class="esv-copyright" style="font-size: 0.85em; color: #6b7280; margin-top: 2em; padding-top: 1em; border-top: 1px solid #e5e7eb; text-align: center;">
    <p><strong>Scripture quotations are from the ESV® Bible</strong> (The Holy Bible, English Standard Version®),
    copyright © 2001 by Crossway, a publishing ministry of Good News Publishers.
    Used by permission. All rights reserved.</p>
</div>
```

**Add to both pages if using ESV API for verse text.**

### Step 6: Testing Checklist

- [ ] Button appears in bottom-right corner
- [ ] Button lifts on hover
- [ ] Panel slides in from right when button clicked
- [ ] Close button (×) works
- [ ] Panel closes when close button clicked
- [ ] Verse cards display with correct styling
- [ ] Clicking verse card shows its cross-references
- [ ] Connection strength labels are accurate
- [ ] Mobile responsive: Panel full-width on mobile
- [ ] Dark mode: All elements visible and styled
- [ ] Scripture links highlight when they have cross-references
- [ ] Hover on link shows preview in button

## Data Structure Reference

### crossRefData Object
```javascript
{
    'Verse Reference': [
        {
            'verse': 'Related Verse',
            'strength': 1-10  // Connection strength
        },
        // More related verses...
    ]
}
```

### doctrineData Object
```javascript
{
    'Verse Reference': ['Theme 1', 'Theme 2', 'Theme 3']
}
```

## Connection Strength Guidelines

- **10:** Same verse repeated, or exact parallel passage
- **9:** Direct doctrinal parallel (e.g., John 3:16 + 1 John 2:2 on propitiation)
- **7-8:** Strong thematic connection within same doctrine
- **5-6:** Moderate connection, related but distinct concepts
- **3-4:** Loose connection, supporting or contrasting idea
- **2:** Tangential mention or background context

## Color Customization

Want different colors? Update these values:

```css
/* Button color - currently purple */
background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);

/* Change to blue */
background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);

/* Change to green */
background: linear-gradient(135deg, #10b981 0%, #059669 100%);

/* Change to orange (like Divine Essence nav) */
background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
```

## Benefits

1. **Enhanced User Experience** - Users can explore related verses without leaving the page
2. **Doctrinal Connections** - Shows how verses relate within theological themes
3. **Study Aid** - Helps readers understand verse context and relationships
4. **Professional Look** - Matches the polished appearance of the Doctrines Library
5. **Mobile-Friendly** - Works beautifully on all screen sizes

## File Locations

- **Doctrines Library (source):** `/home/johndavid/Projects/Christian-Doctrine/Doctrines/doctrines_library_wp_publish.html`
- **Divine Decree (target):** `/home/johndavid/Projects/Christian-Doctrine/Doctrines/doctrine-of-the-divine-decree/divine-decree_wp_publish.html`
- **Divine Essence (target):** `/home/johndavid/Projects/Christian-Doctrine/Doctrines/doctrine-of-divine-essence/divine-essence-3_wp_publish.html`

## Next Steps

1. Add HTML structure to both pages
2. Add CSS styling to both pages
3. Create page-specific `crossRefData` objects
4. Add JavaScript functionality
5. Test on desktop and mobile
6. Test in both light and dark modes
7. Deploy to WordPress

---

**Document Version:** 1.0
**Created:** 2026-01-08
**Status:** Ready for implementation
**Estimated Time:** 2-3 hours per page (including data creation)
