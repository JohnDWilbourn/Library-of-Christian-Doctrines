# ESV API Key Reference

## Your ESV API Key

**Key:** `2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465`

**Account:** john-wilbourn

**Status:** ✅ Active and configured in published pages

---

## Where It's Currently Used

### 1. Scripture Index Page ✅
**File:** `Doctrines/scripture_index_wp_publish.html`
**Line:** 6769
```javascript
const ESV_API_KEY = '2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465';
```

### 2. Doctrines Library Page ✅
**File:** `Doctrines/doctrines_library_wp_publish.html`
**Line:** 4732
```javascript
esv: {
    enabled: true,
    key: '2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465',
    baseUrl: 'https://api.esv.org/v3/passage/text/'
}
```

### 3. Analytics Page ✅
**File:** `Doctrines/scripture_analytics_wp.html`
**Status:** Check if configured (same key)

---

## Where to Add for New Pages

### For Divine Decree Page

Add this in the JavaScript section after the verse tooltip code:

```javascript
<script>
// ESV API Configuration
const ESV_API_KEY = '2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465';
const ESV_API_URL = 'https://api.esv.org/v3/passage/text/';

// Enhanced verse fetching with ESV API
async function fetchVerseText(reference) {
    try {
        // Check cache first
        const cached = localStorage.getItem(`verse_${reference}`);
        if (cached) {
            const data = JSON.parse(cached);
            if (Date.now() - data.timestamp < 30 * 24 * 60 * 60 * 1000) { // 30 days
                return data.text;
            }
        }

        // Fetch from ESV API
        const url = `${ESV_API_URL}?q=${encodeURIComponent(reference)}&include-passage-references=false&include-verse-numbers=false&include-footnotes=false&include-headings=false`;

        const response = await fetch(url, {
            headers: {
                'Authorization': `Token ${ESV_API_KEY}`
            }
        });

        if (!response.ok) {
            throw new Error(`ESV API error: ${response.status}`);
        }

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

### For Divine Essence Page

Same configuration as Divine Decree above.

---

## API Limits and Compliance

### Free Tier Limits
- **60 requests per minute**
- **1,000 requests per hour**
- **5,000 requests per day**

### Current Implementation
✅ **Rate limiting:** Enforced in doctrines library
✅ **Caching:** 30-day localStorage cache
✅ **Cache size:** Max 500 verses (FIFO)
✅ **Copyright notice:** Included where required

### Cache Strategy
```javascript
// Check if verse is cached (30-day expiry)
const cached = localStorage.getItem(`verse_${reference}`);
if (cached && !isExpired(cached)) {
    return cached.text;
}

// Fetch from API and cache
const verse = await fetchFromESV(reference);
cacheVerse(reference, verse, 30days);
```

---

## Testing Your API Key

### Quick Test in Browser Console
```javascript
// Test ESV API key
fetch('https://api.esv.org/v3/passage/text/?q=John+3:16', {
    headers: {
        'Authorization': 'Token 2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465'
    }
})
.then(r => r.json())
.then(data => console.log('✓ API key works!', data.passages[0]))
.catch(err => console.error('✗ API key error:', err));
```

### Expected Response
```json
{
  "query": "John 3:16",
  "canonical": "John 3:16",
  "parsed": [[43003016, 43003016]],
  "passage_meta": [...],
  "passages": [
    "For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life."
  ]
}
```

---

## Usage in Cross-Reference System

When adding the cross-reference feature to Divine Decree/Essence, the ESV API will be used to:

1. **Fetch verse text** for tooltip previews
2. **Display full verses** in the cross-reference panel
3. **Cache responses** to minimize API calls

### Integration with Cross-References

The cross-reference panel can optionally show verse text:

```javascript
// In showCrossReferences() function
sortedRefs.forEach(async ref => {
    const verseText = await fetchVerseText(ref.verse);

    html += `
        <div class="cross-ref-item">
            <div class="cross-ref-verse">${ref.verse}</div>
            <div class="cross-ref-text">${verseText}</div>
            <div class="cross-ref-strength">${strengthLabel}</div>
        </div>
    `;
});
```

---

## Security Notes

### Is it safe to expose the API key?

**Yes, for ESV API free tier:**
- ✅ Designed for client-side use
- ✅ Only allows read access to Bible text
- ✅ No write/delete permissions
- ✅ Rate limited per key automatically
- ✅ Can regenerate key if needed

### Best Practices
1. Use caching to minimize API calls
2. Implement rate limiting on client side
3. Don't use API key for commercial apps (free tier is non-commercial)
4. Monitor usage at https://api.esv.org/account/

---

## Regenerating Your Key

If needed, you can regenerate your ESV API key at:

1. Visit https://api.esv.org/account/
2. Log in as john-wilbourn
3. Navigate to "API Keys"
4. Click "Regenerate Key"
5. Update all published pages with new key

**Files to update if regenerated:**
- `Doctrines/scripture_index_wp_publish.html` (line 6769)
- `Doctrines/doctrines_library_wp_publish.html` (line 4732)
- `Doctrines/scripture_analytics_wp.html` (if configured)
- Any new doctrine pages (Divine Decree, Divine Essence)

---

## Copyright Compliance

### Required ESV Copyright Notice

Include this notice on any page displaying ESV text:

```html
<div class="esv-copyright" style="font-size: 0.85em; color: #6b7280; margin-top: 2em; padding-top: 1em; border-top: 1px solid #e5e7eb;">
    <p>Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®),
    copyright © 2001 by Crossway, a publishing ministry of Good News Publishers.
    Used by permission. All rights reserved.
    The ESV text may not be quoted in any publication made available to the public by a
    Creative Commons license. The ESV may not be translated in whole or in part into any other language.</p>
    <p>Users may not copy or download more than 500 verses of the ESV Bible or more than one half
    of any book of the ESV Bible.</p>
</div>
```

**Add this notice to:**
- Divine Decree page (if using ESV API for tooltips)
- Divine Essence page (if using ESV API for tooltips)
- Any page that displays ESV verse text

---

## Alternative: Using Without API

The tooltip and cross-reference systems work without the ESV API:

### Fallback Behavior
```javascript
// If API call fails or key is missing
return `${reference} - Click to view on ESV.org`;
```

### Benefits of Using API
- ✅ Users see verse text immediately
- ✅ Better user experience
- ✅ Reduces clicks to external site
- ✅ Enhances study functionality

### Works Without API
- ✅ All navigation features
- ✅ Cross-reference relationships
- ✅ Click-through to ESV.org
- ✅ Cross-reference panel structure

---

## Quick Reference

**ESV API Documentation:** https://api.esv.org/docs/

**Your API Key:** `2ff0f1743ba8fc2e6ccb4e8c941970cd44c5e465`

**Account Dashboard:** https://api.esv.org/account/

**Current Usage:** Check dashboard for real-time statistics

**Daily Limit:** 5,000 requests (resets at midnight UTC)

**Cache Duration:** 30 days (recommended by ESV)

**Max Cached Verses:** 500 verses (per ESV terms)

---

**Document Version:** 1.0
**Created:** 2026-01-08
**Status:** Reference document for all ESV API integration
