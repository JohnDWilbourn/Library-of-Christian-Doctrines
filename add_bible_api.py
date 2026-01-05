#!/usr/bin/env python3
"""
Add Live Bible API Integration
Integrates ESV API for real verse text retrieval in tooltips.
Includes fallback to API.Bible as alternative.
"""

from bs4 import BeautifulSoup

def add_bible_api_script():
    """Generate JavaScript for live Bible API integration."""
    
    return """
<script>
(function() {
    // Bible API Configuration
    // To use ESV API: Get free key from https://api.esv.org/
    // To use API.Bible: Get free key from https://scripture.api.bible/
    
    const API_CONFIG = {
        // ESV API (preferred)
        esv: {
            enabled: false, // Set to true when you have an API key
            key: 'YOUR_ESV_API_KEY_HERE', // Get from https://api.esv.org/
            baseUrl: 'https://api.esv.org/v3/passage/text/'
        },
        // API.Bible (fallback)
        apiBible: {
            enabled: false, // Set to true when you have an API key
            key: 'YOUR_API_BIBLE_KEY_HERE', // Get from https://scripture.api.bible/
            bibleId: 'de4e12af7f28f599-02', // KJV Bible ID
            baseUrl: 'https://api.scripture.api.bible/v1/bibles/'
        }
    };
    
    // Cache for API responses
    const apiCache = new Map();
    
    /**
     * Fetch verse text from ESV API
     */
    async function fetchFromESV(reference) {
        if (!API_CONFIG.esv.enabled || !API_CONFIG.esv.key || API_CONFIG.esv.key === 'YOUR_ESV_API_KEY_HERE') {
            return null;
        }
        
        try {
            const url = API_CONFIG.esv.baseUrl + '?' + new URLSearchParams({
                q: reference,
                'include-headings': 'false',
                'include-footnotes': 'false',
                'include-verse-numbers': 'false',
                'include-short-copyright': 'false',
                'include-passage-references': 'false'
            });
            
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Token ${API_CONFIG.esv.key}`
                }
            });
            
            if (!response.ok) throw new Error('ESV API error');
            
            const data = await response.json();
            return {
                text: data.passages[0]?.trim() || 'Verse not found',
                version: 'ESV',
                success: true
            };
        } catch (error) {
            console.warn('ESV API fetch failed:', error);
            return null;
        }
    }
    
    /**
     * Fetch verse text from API.Bible
     */
    async function fetchFromAPIBible(reference) {
        if (!API_CONFIG.apiBible.enabled || !API_CONFIG.apiBible.key || API_CONFIG.apiBible.key === 'YOUR_API_BIBLE_KEY_HERE') {
            return null;
        }
        
        try {
            // Convert reference to API format (e.g., "John 3:16" -> "JHN.3.16")
            const normalized = normalizeReferenceForAPI(reference);
            if (!normalized) return null;
            
            const url = `${API_CONFIG.apiBible.baseUrl}${API_CONFIG.apiBible.bibleId}/passages/${normalized}`;
            
            const response = await fetch(url, {
                headers: {
                    'api-key': API_CONFIG.apiBible.key
                }
            });
            
            if (!response.ok) throw new Error('API.Bible error');
            
            const data = await response.json();
            return {
                text: data.data?.content?.replace(/<[^>]+>/g, '').trim() || 'Verse not found',
                version: 'KJV',
                success: true
            };
        } catch (error) {
            console.warn('API.Bible fetch failed:', error);
            return null;
        }
    }
    
    /**
     * Normalize reference for API.Bible format
     */
    function normalizeReferenceForAPI(reference) {
        // This is a simplified version - would need full book name mapping
        const bookMap = {
            'Gen': 'GEN', 'Exod': 'EXO', 'Matt': 'MAT', 'John': 'JHN',
            'Rom': 'ROM', 'Eph': 'EPH', '1 Cor': '1CO', '2 Cor': '2CO',
            // Add more mappings as needed
        };
        
        const match = reference.match(/^([^0-9]+)\\s*(\\d+):(\\d+)/);
        if (!match) return null;
        
        const book = match[1].trim();
        const chapter = match[2];
        const verse = match[3];
        
        const bookCode = bookMap[book];
        if (!bookCode) return null;
        
        return `${bookCode}.${chapter}.${verse}`;
    }
    
    /**
     * Get verse text with API fallback chain
     */
    async function getVerseText(reference) {
        // Check cache first
        if (apiCache.has(reference)) {
            return apiCache.get(reference);
        }
        
        // Try ESV API first
        let result = await fetchFromESV(reference);
        
        // Fallback to API.Bible
        if (!result) {
            result = await fetchFromAPIBible(reference);
        }
        
        // Final fallback to placeholder
        if (!result) {
            result = {
                text: 'API key required for live verse preview. Click link to view verse on ESV.org',
                version: 'Info',
                success: false
            };
        }
        
        // Cache result
        apiCache.set(reference, result);
        return result;
    }
    
    /**
     * Update existing verse tooltip system with API
     */
    if (typeof window.getVerseText === 'undefined') {
        // No existing tooltip system, create one
        console.log('⚠ Verse tooltip system not found. Run add_verse_preview.py first');
    } else {
        // Override existing getVerseText function
        const originalGetVerseText = window.getVerseText;
        window.getVerseText = async function(reference) {
            return await getVerseText(reference);
        };
        console.log('✓ Live Bible API integrated with verse tooltips');
    }
    
    // Expose API configuration for easy updates
    window.BIBLE_API_CONFIG = API_CONFIG;
    
    // Display API status
    console.log('📖 Bible API Status:');
    console.log('  ESV API:', API_CONFIG.esv.enabled ? '✓ Enabled' : '✗ Disabled (add API key)');
    console.log('  API.Bible:', API_CONFIG.apiBible.enabled ? '✓ Enabled' : '✗ Disabled (add API key)');
    
    if (!API_CONFIG.esv.enabled && !API_CONFIG.apiBible.enabled) {
        console.log('');
        console.log('To enable live verse previews:');
        console.log('1. Get free API key from https://api.esv.org/');
        console.log('2. Edit the HTML file and update API_CONFIG.esv.key');
        console.log('3. Set API_CONFIG.esv.enabled = true');
    }
})();
</script>

<!-- API Configuration Instructions -->
<!--
To enable live Bible verse previews:

Option 1: ESV API (Recommended)
1. Visit https://api.esv.org/ and create a free account
2. Generate an API key
3. Find "API_CONFIG.esv.key" in this file and replace 'YOUR_ESV_API_KEY_HERE' with your key
4. Change "enabled: false" to "enabled: true" for ESV
5. Save and reload the page

Option 2: API.Bible (Alternative)
1. Visit https://scripture.api.bible/ and sign up
2. Generate an API key
3. Find "API_CONFIG.apiBible.key" and replace with your key
4. Change "enabled: false" to "enabled: true" for apiBible
5. Save and reload the page

Free API Limits:
- ESV API: 5,000 requests per day
- API.Bible: 5,000 requests per day

The system will cache responses to minimize API calls.
-->
"""

def add_bible_api(html_file, output_file):
    """Add Bible API integration to HTML file."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already exists
    if 'BIBLE_API_CONFIG' in content:
        print(f"ℹ Bible API already exists in {html_file}")
        return
    
    # Find the last closing div and insert before it
    last_div_pos = content.rfind('</div>')
    if last_div_pos != -1:
        before = content[:last_div_pos]
        after = content[last_div_pos:]
        result = before + add_bible_api_script() + '\n' + after
    else:
        result = content + add_bible_api_script()
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added Bible API integration to {output_file}")

def create_api_setup_guide():
    """Create a guide for setting up the Bible API."""
    
    guide = """# Bible API Setup Guide

## Overview
The doctrines library now supports live Bible verse previews using external APIs.

## Supported APIs

### 1. ESV API (English Standard Version) - RECOMMENDED
- **Website**: https://api.esv.org/
- **Cost**: Free (5,000 requests/day)
- **Quality**: Excellent, modern translation
- **Setup Time**: 5 minutes

#### Setup Steps:
1. Go to https://api.esv.org/
2. Click "Get API Key" or "Sign Up"
3. Create a free account
4. Generate an API key (available immediately)
5. Copy your API key

#### Configuration:
1. Open `Doctrines/doctrines_library_wp_clean.html`
2. Find the section with `API_CONFIG.esv.key`
3. Replace `'YOUR_ESV_API_KEY_HERE'` with your actual key
4. Change `enabled: false` to `enabled: true`
5. Save the file

Example:
```javascript
esv: {
    enabled: true,  // Changed from false
    key: 'abc123def456',  // Your actual API key
    baseUrl: 'https://api.esv.org/v3/passage/text/'
}
```

### 2. API.Bible (Alternative)
- **Website**: https://scripture.api.bible/
- **Cost**: Free (5,000 requests/day)
- **Versions**: Multiple (KJV, ASV, etc.)
- **Setup Time**: 5 minutes

#### Setup Steps:
1. Go to https://scripture.api.bible/
2. Sign up for a free account
3. Create an API key
4. Choose a Bible version (default: KJV)
5. Copy your API key and Bible ID

#### Configuration:
1. Open `Doctrines/doctrines_library_wp_clean.html`
2. Find `API_CONFIG.apiBible.key`
3. Replace `'YOUR_API_BIBLE_KEY_HERE'` with your key
4. Optionally change `bibleId` for different versions
5. Change `enabled: false` to `enabled: true`
6. Save the file

## Testing

After configuration:
1. Open the doctrines library in a browser
2. Open browser console (F12)
3. Look for "✓ Live Bible API integrated"
4. Hover over any scripture reference
5. You should see the actual verse text

## Troubleshooting

### "API key required" message appears
- Check that you set `enabled: true`
- Verify your API key is correct
- Check browser console for error messages

### Verses not loading
- Check internet connection
- Verify API key is active
- Check API rate limits (5,000/day)
- Look for errors in browser console

### CORS errors
- ESV and API.Bible both support CORS
- If using WordPress, ensure scripts are in HTML block
- May not work on local file:// protocol

## Best Practices

1. **Use Caching**: The system automatically caches API responses
2. **Monitor Usage**: Both APIs have 5,000 request/day limits
3. **Backup Plan**: Original tooltip system works without API
4. **Security**: API keys are client-side (acceptable for free tier)

## WordPress Integration

If using in WordPress Custom HTML block:
1. Configure API as described above
2. Copy entire HTML file content
3. Paste into Custom HTML block
4. API will work on frontend

Note: API keys will be visible in page source (this is normal for
free-tier APIs that allow client-side access).

## Cost Considerations

Both APIs are free with generous limits:
- **ESV**: 5,000 requests/day
- **API.Bible**: 5,000 requests/day

With caching, this easily supports hundreds of users per day.

## Alternative: No API

The system works without API keys:
- Shows placeholder message in tooltips
- Links still direct to ESV.org for full verses
- All other features work normally

## Support

- **ESV API**: https://api.esv.org/docs/
- **API.Bible**: https://scripture.api.bible/livedocs
"""
    
    with open('API_SETUP_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✓ Created API_SETUP_GUIDE.md")

def main():
    """Main execution."""
    print("Adding live Bible API integration...\n")
    
    # Add to doctrines library
    add_bible_api(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    # Add to scripture index
    add_bible_api(
        'Doctrines/scripture_index_wp_clean.html',
        'Doctrines/scripture_index_wp_clean.html'
    )
    
    # Create setup guide
    create_api_setup_guide()
    
    print("\n✓ Live Bible API integration added!")
    print("  - Supports ESV API (recommended)")
    print("  - Supports API.Bible (alternative)")
    print("  - Automatic caching for performance")
    print("  - Graceful fallback without API key")
    print("\n📖 See API_SETUP_GUIDE.md for configuration instructions")
    print("   Get free API key at: https://api.esv.org/")

if __name__ == '__main__':
    main()
