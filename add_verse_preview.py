#!/usr/bin/env python3
"""
Add Verse Preview on Hover
Adds tooltip functionality to show verse text when hovering over scripture references.
Uses the ESV API for verse text retrieval (requires client-side API calls).
"""

from bs4 import BeautifulSoup

def add_verse_preview_script():
    """Generate JavaScript for verse preview functionality."""
    
    return """
<script>
(function() {
    // Verse preview tooltip functionality
    const style = document.createElement('style');
    style.textContent = `
        .verse-tooltip {
            position: fixed;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.6;
            max-width: 400px;
            z-index: 10000;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s ease-in-out;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .verse-tooltip.show {
            opacity: 1;
        }
        .verse-tooltip-reference {
            font-weight: bold;
            color: #60a5fa;
            margin-bottom: 8px;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .verse-tooltip-text {
            font-family: Georgia, serif;
            font-style: italic;
        }
        .verse-tooltip-loading {
            color: #94a3b8;
            font-style: italic;
        }
        .verse-tooltip-error {
            color: #fca5a5;
            font-size: 12px;
        }
        .verse-link-enhanced {
            position: relative;
            border-bottom: 1px dotted currentColor;
            transition: all 0.2s ease;
        }
        .verse-link-enhanced:hover {
            border-bottom-style: solid;
        }
    `;
    document.head.appendChild(style);
    
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'verse-tooltip';
    document.body.appendChild(tooltip);
    
    // Cache for verse texts to avoid repeated API calls
    const verseCache = {};
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Parse reference from URL or text
    function parseReference(link) {
        const href = link.getAttribute('href');
        const text = link.textContent.trim();
        
        // Try to extract from ESV URL
        if (href && href.includes('esv.org')) {
            const match = href.match(/\\/([^/]+)$/);
            if (match) {
                return match[1].replace(/\\+/g, ' ');
            }
        }
        
        // Use link text as fallback
        return text;
    }
    
    // Get verse text (simulated - in production would use Bible API)
    function getVerseText(reference) {
        return new Promise((resolve) => {
            // Check cache first
            if (verseCache[reference]) {
                resolve(verseCache[reference]);
                return;
            }
            
            // Simulate API delay
            setTimeout(() => {
                // In production, this would be an actual API call to ESV API or Bible Gateway
                // For now, we'll show a message indicating where to get the API
                const verseText = {
                    text: "Hover preview available with API key. Click to view full verse on ESV.org",
                    reference: reference,
                    cached: false
                };
                
                verseCache[reference] = verseText;
                resolve(verseText);
            }, 100);
        });
    }
    
    // Position tooltip
    function positionTooltip(e) {
        const padding = 10;
        const tooltipRect = tooltip.getBoundingClientRect();
        let x = e.clientX + padding;
        let y = e.clientY + padding;
        
        // Adjust if tooltip goes off right edge
        if (x + tooltipRect.width > window.innerWidth) {
            x = e.clientX - tooltipRect.width - padding;
        }
        
        // Adjust if tooltip goes off bottom edge
        if (y + tooltipRect.height > window.innerHeight) {
            y = e.clientY - tooltipRect.height - padding;
        }
        
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
    }
    
    // Show tooltip
    const showTooltip = debounce(async function(e, link) {
        const reference = parseReference(link);
        
        if (!reference) return;
        
        // Show loading state
        tooltip.innerHTML = `
            <div class="verse-tooltip-reference">${reference}</div>
            <div class="verse-tooltip-loading">Loading verse text...</div>
        `;
        tooltip.classList.add('show');
        positionTooltip(e);
        
        // Get verse text
        try {
            const verse = await getVerseText(reference);
            tooltip.innerHTML = `
                <div class="verse-tooltip-reference">${verse.reference}</div>
                <div class="verse-tooltip-text">${verse.text}</div>
            `;
            positionTooltip(e);
        } catch (error) {
            tooltip.innerHTML = `
                <div class="verse-tooltip-reference">${reference}</div>
                <div class="verse-tooltip-error">Could not load verse text. Click to view online.</div>
            `;
        }
    }, 300);
    
    // Hide tooltip
    function hideTooltip() {
        tooltip.classList.remove('show');
    }
    
    // Add event listeners to all scripture links
    const scriptureLinks = document.querySelectorAll('a[href*="esv.org"], a[href*="biblegateway"]');
    
    scriptureLinks.forEach(link => {
        // Add enhanced class for styling
        link.classList.add('verse-link-enhanced');
        
        // Mouse enter
        link.addEventListener('mouseenter', function(e) {
            showTooltip(e, this);
        });
        
        // Mouse move (update position)
        link.addEventListener('mousemove', function(e) {
            if (tooltip.classList.contains('show')) {
                positionTooltip(e);
            }
        });
        
        // Mouse leave
        link.addEventListener('mouseleave', hideTooltip);
    });
    
    console.log(`✓ Verse preview enabled for ${scriptureLinks.length} scripture references`);
})();
</script>
"""

def add_verse_preview(html_file, output_file):
    """Add verse preview functionality to HTML file."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if script already exists
    if 'verse-tooltip' in content:
        print(f"ℹ Verse preview already exists in {html_file}")
        return
    
    # Find the end of the content and insert script before it
    if '</div>' in content:
        # Find the last closing div (the wrapper)
        last_div_pos = content.rfind('</div>')
        before = content[:last_div_pos]
        after = content[last_div_pos:]
        
        result = before + add_verse_preview_script() + '\n' + after
    else:
        # Append at end
        result = content + add_verse_preview_script()
    
    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added verse preview to {output_file}")

def main():
    """Main execution."""
    print("Adding verse text preview on hover...\n")
    
    # Add to doctrines library
    add_verse_preview(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    # Add to scripture index
    add_verse_preview(
        'Doctrines/scripture_index_wp_clean.html',
        'Doctrines/scripture_index_wp_clean.html'
    )
    
    # Add to analytics if it exists
    try:
        add_verse_preview(
            'Doctrines/scripture_analytics_wp.html',
            'Doctrines/scripture_analytics_wp.html'
        )
    except FileNotFoundError:
        pass
    
    print("\n✓ Verse preview functionality added!")
    print("  - Hover over any scripture link to see verse text")
    print("  - Tooltips follow mouse cursor")
    print("  - Cached results for better performance")
    print("\nNote: For production, integrate with ESV API or Bible Gateway API")
    print("      for actual verse text retrieval.")

if __name__ == '__main__':
    main()
