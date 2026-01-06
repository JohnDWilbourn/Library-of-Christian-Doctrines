#!/usr/bin/env python3
"""
Generate Standalone Doctrine Pages with Full Navigation & Features
==================================================================
Creates WordPress-ready standalone pages for extensive doctrines (Essence, Decree)
with all navigation links and interactive features integrated.

Usage:
    python generate_standalone_doctrine_page.py <doctrine_name> <input_file> [output_file]
    
Example:
    python generate_standalone_doctrine_page.py "Divine Essence" \
        Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html \
        Doctrines/doctrine-of-divine-essence_wp_standalone.html
"""

import re
import sys
from pathlib import Path

# WordPress URLs (update these to match your site)
LIBRARY_URL = "https://intelligencereport.info/complete-library-of-christian-doctrine/"
INDEX_URL = "https://intelligencereport.info/comprehensive-biblical-reference-guide/"
ANALYTICS_URL = "https://intelligencereport.info/scripture-analytics/"

def extract_body_content(html_content):
    """Extract body content from HTML, removing DOCTYPE, html, head tags"""
    # Remove DOCTYPE and html tags
    html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'<html[^>]*>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</html>', '', html_content, flags=re.IGNORECASE)
    
    # Extract head content (for title)
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "Doctrine"
    
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        # If no body tag, assume entire content is body
        body_content = html_content
    
    # Remove style tags from body (we'll add our own)
    body_content = re.sub(r'<style[^>]*>.*?</style>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
    
    return title, body_content.strip()

def get_navigation_html(doctrine_name, current_page="doctrine"):
    """Generate navigation bar HTML"""
    if current_page == "doctrine":
        library_class = 'current-page'
        library_link = '<span class="current-page">📖 Doctrines Library</span>'
    else:
        library_class = ''
        library_link = f'<a href="{LIBRARY_URL}" style="display: inline-block; padding: 0.5em 1.2em; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border-radius: 8px; font-weight: 600; text-decoration: none; box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3); transition: all 0.2s ease;">📖 Doctrines Library</a>'
    
    return f'''
<!-- Cross-Page Navigation -->
<div style="margin: 1.5em 0; padding: 1em; background: linear-gradient(to right, #eff6ff, #dbeafe); border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);">
    <div style="display: inline-flex; gap: 1em; flex-wrap: wrap; justify-content: center; align-items: center;">
        {library_link}
        <a href="{INDEX_URL}" style="display: inline-block; padding: 0.5em 1.2em; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border-radius: 8px; font-weight: 600; text-decoration: none; box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3); transition: all 0.2s ease;">📑 Scripture Index</a>
        <a href="{ANALYTICS_URL}" style="display: inline-block; padding: 0.5em 1.2em; background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); color: white; border-radius: 8px; font-weight: 600; text-decoration: none; box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3); transition: all 0.2s ease;">📊 Analytics</a>
    </div>
</div>
'''

def get_verse_preview_script():
    """Get verse preview tooltip JavaScript"""
    return '''
<script>
// Verse Preview Tooltip System
(function() {
    const API_CONFIG = {
        enabled: false,  // Set to true and add apiKey to enable ESV API
        apiKey: '',
        provider: 'esv'  // 'esv' or 'biblegateway'
    };
    
    const verseCache = new Map();
    let tooltip = null;
    
    function createTooltip() {
        if (tooltip) return tooltip;
        tooltip = document.createElement('div');
        tooltip.id = 'verseTooltip';
        tooltip.style.cssText = `
            position: absolute;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 0.75em 1em;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 400px;
            font-size: 0.9em;
            line-height: 1.5;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s ease;
        `;
        document.body.appendChild(tooltip);
        return tooltip;
    }
    
    function showTooltip(verse, x, y) {
        const tip = createTooltip();
        tip.textContent = `Loading ${verse}...`;
        tip.style.left = x + 'px';
        tip.style.top = (y - 10) + 'px';
        tip.style.opacity = '1';
        
        // Check cache
        if (verseCache.has(verse)) {
            tip.textContent = verseCache.get(verse);
            return;
        }
        
        // For now, just show verse reference
        // In production, this would call ESV API
        tip.textContent = `${verse} - Click to view full text`;
        verseCache.set(verse, tip.textContent);
    }
    
    function hideTooltip() {
        if (tooltip) {
            tooltip.style.opacity = '0';
        }
    }
    
    // Add hover listeners to scripture links
    document.addEventListener('DOMContentLoaded', function() {
        const links = document.querySelectorAll('a[href*="esv.org"], a[href*="biblegateway"]');
        links.forEach(link => {
            link.addEventListener('mouseenter', function(e) {
                const verse = this.textContent.trim();
                showTooltip(verse, e.pageX, e.pageY);
            });
            link.addEventListener('mouseleave', hideTooltip);
            link.addEventListener('mousemove', function(e) {
                if (tooltip) {
                    tooltip.style.left = e.pageX + 'px';
                    tooltip.style.top = (e.pageY - 10) + 'px';
                }
            });
        });
    });
})();
</script>
'''

def get_search_script():
    """Get search functionality JavaScript"""
    return '''
<script>
// Search Functionality
(function() {
    const searchInput = document.getElementById('doctrineSearch');
    const searchResults = document.getElementById('searchResults');
    
    if (!searchInput) return;
    
    function performSearch(query) {
        if (!query || query.length < 2) {
            searchResults.textContent = '';
            searchResults.className = '';
            return;
        }
        
        const lowerQuery = query.toLowerCase();
        const sections = document.querySelectorAll('section, h2, h3, p, li');
        let matches = 0;
        
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            if (text.includes(lowerQuery)) {
                matches++;
                section.style.backgroundColor = matches === 1 ? '#fef3c7' : '';
            } else {
                section.style.backgroundColor = '';
            }
        });
        
        if (matches > 0) {
            searchResults.textContent = `Found ${matches} matching section${matches > 1 ? 's' : ''}`;
            searchResults.className = 'search-success';
            
            // Scroll to first match
            const firstMatch = document.querySelector('section[style*="background-color"], h2[style*="background-color"], h3[style*="background-color"]');
            if (firstMatch) {
                firstMatch.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            searchResults.textContent = 'No matches found';
            searchResults.className = 'search-error';
        }
    }
    
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(this.value);
        }, 300);
    });
    
    // ESC to clear
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            performSearch('');
        }
    });
})();
</script>
'''

def get_cross_reference_script():
    """Get cross-reference panel JavaScript (simplified version)"""
    return '''
<script>
// Cross-Reference Panel (Simplified)
(function() {
    // This would normally load cross-reference data
    // For standalone pages, we'll just show a message
    const scriptureLinks = document.querySelectorAll('a[href*="esv.org"], a[href*="biblegateway"]');
    
    scriptureLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const verse = this.textContent.trim();
            // In full version, this would show cross-references
            // For now, just allow normal link behavior
        });
    });
})();
</script>
'''

def generate_standalone_page(doctrine_name, body_content, title):
    """Generate complete standalone WordPress-ready HTML page"""
    
    # Clean up body content - remove extra whitespace
    body_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', body_content)
    
    page_html = f'''<!-- 
============================================================
WordPress Standalone Doctrine Page - Ready to Copy/Paste
============================================================
Doctrine: {doctrine_name}
Generated: Standalone page with full navigation and features

DEPLOYMENT INSTRUCTIONS:
1. Copy this entire file content
2. Go to WordPress page editor
3. Add a "Custom HTML" block
4. Paste the content
5. Update/Publish the page

FEATURES INCLUDED:
✅ Navigation links (Library, Index, Analytics)
✅ Verse preview tooltips
✅ Search functionality
✅ Responsive design
✅ Mobile-optimized
============================================================
-->

<!-- CRITICAL: Viewport for proper mobile rendering -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">

<!-- Hide WordPress auto-generated title -->
<style>
.entry-title, .page-title, h1.entry-title, .wp-block-post-title {{
    display: none !important;
}}
</style>

<h1 style="color: #1a202c !important; text-align: center !important; font-size: 2.5em !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.2) !important; padding: 1em 0 !important; margin: 0 0 0.5em 0 !important; font-weight: 700 !important;">
    {title}
</h1>

<!-- Dark mode support for title -->
<style>
@media (prefers-color-scheme: dark) {{
    h1[style*="{title[:20]}"] {{
        color: #f7fafc !important;
        text-shadow: 2px 2px 12px rgba(255,255,255,0.3), 0 0 20px rgba(147,197,253,0.4) !important;
    }}
}}
</style>

<div class="doctrine-standalone-wrapper" style="max-width: 1200px; margin: 0 auto; padding: 2em 1em;">

{get_navigation_html(doctrine_name)}

<!-- Search Container -->
<div class="search-container" style="margin: 2em 0; text-align: center;">
    <input id="doctrineSearch" placeholder="🔍 Search doctrine content..." style="width: 80%; max-width: 600px; padding: 12px 20px; font-size: 16px; border: 2px solid #3b82f6; border-radius: 25px; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2); transition: all 0.3s ease; outline: none;" type="text"/>
    <div id="searchResults" style="margin-top: 1em; text-align: center; font-style: italic;"></div>
</div>

<!-- Doctrine Content -->
<div class="doctrine-content" style="margin: 2em 0; padding: 2em; background: white; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); line-height: 1.8;">

{body_content}

</div>

</div>

<!-- Styles -->
<style>
.doctrine-standalone-wrapper {{
    font-family: Georgia, 'Times New Roman', serif;
    color: #1f2937;
    line-height: 1.8;
}}

.doctrine-content h1 {{
    color: #1e40af;
    font-size: 2em;
    margin-top: 2em;
    margin-bottom: 1em;
    border-bottom: 3px solid #3b82f6;
    padding-bottom: 0.5em;
}}

.doctrine-content h2 {{
    color: #1e40af;
    font-size: 1.6em;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
    border-bottom: 2px solid #4299e1;
    padding-bottom: 0.3em;
}}

.doctrine-content h3 {{
    color: #374151;
    font-size: 1.3em;
    margin-top: 1.2em;
    margin-bottom: 0.6em;
}}

.doctrine-content p {{
    margin: 1em 0;
    text-align: justify;
}}

.doctrine-content ol, .doctrine-content ul {{
    margin: 1em 0;
    padding-left: 2em;
}}

.doctrine-content li {{
    margin: 0.8em 0;
}}

.doctrine-content ol.roman {{
    list-style-type: upper-roman;
}}

.doctrine-content ol.alpha {{
    list-style-type: upper-alpha;
}}

.doctrine-content a[href*="esv.org"], 
.doctrine-content a[href*="biblegateway"] {{
    color: #2563eb;
    text-decoration: underline;
    transition: color 0.2s ease;
}}

.doctrine-content a[href*="esv.org"]:hover, 
.doctrine-content a[href*="biblegateway"]:hover {{
    color: #1d4ed8;
    text-decoration: none;
}}

/* Search Results Styling */
#searchResults {{
    font-weight: 500;
    font-size: 1.05em;
    padding: 0.5em;
    border-radius: 8px;
    transition: all 0.3s ease;
}}

#searchResults.search-success {{
    color: #059669;
    background: #d1fae5;
}}

#searchResults.search-error {{
    color: #dc2626;
    background: #fee2e2;
}}

/* Responsive Design */
@media (max-width: 768px) {{
    .doctrine-standalone-wrapper {{
        padding: 1em 0.5em;
    }}
    
    .doctrine-content {{
        padding: 1em;
    }}
    
    h1 {{
        font-size: 1.8em !important;
    }}
    
    .doctrine-content h1 {{
        font-size: 1.5em;
    }}
    
    .doctrine-content h2 {{
        font-size: 1.3em;
    }}
    
    #doctrineSearch {{
        width: 95% !important;
    }}
}}
</style>

{get_verse_preview_script()}
{get_search_script()}
{get_cross_reference_script()}

'''
    
    return page_html

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_standalone_doctrine_page.py <doctrine_name> <input_file> [output_file]")
        print("\nExample:")
        print('  python generate_standalone_doctrine_page.py "Divine Essence" \\')
        print('    Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html \\')
        print('    Doctrines/doctrine-of-divine-essence_wp_standalone.html')
        sys.exit(1)
    
    doctrine_name = sys.argv[1]
    input_file = Path(sys.argv[2])
    
    if len(sys.argv) > 3:
        output_file = Path(sys.argv[3])
    else:
        output_file = input_file.parent / f"{input_file.stem}_wp_standalone.html"
    
    print(f"📖 Generating standalone page for: {doctrine_name}")
    print(f"📄 Input: {input_file}")
    print(f"💾 Output: {output_file}")
    print()
    
    # Read input file
    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract content
    print("Extracting content...")
    title, body_content = extract_body_content(html_content)
    
    # Generate standalone page
    print("Generating standalone page...")
    standalone_html = generate_standalone_page(doctrine_name, body_content, title)
    
    # Write output
    print(f"Writing output file...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(standalone_html)
    
    print()
    print(f"✅ Successfully generated standalone page!")
    print(f"   File: {output_file.name}")
    print(f"   Size: {len(standalone_html):,} characters")
    print()
    print("📋 Next steps:")
    print("   1. Review the generated file")
    print("   2. Copy entire content to WordPress Custom HTML block")
    print("   3. Publish the page")
    print("   4. Update navigation links if needed")

if __name__ == '__main__':
    main()
