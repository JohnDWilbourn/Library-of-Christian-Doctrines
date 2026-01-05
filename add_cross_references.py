#!/usr/bin/env python3
"""
Add Cross-Reference Suggestion Engine
Analyzes scripture relationships to suggest related verses and doctrines.
"""

from bs4 import BeautifulSoup
from collections import defaultdict
import re

def extract_verse_relationships(html_file):
    """Extract relationships between verses based on co-occurrence in doctrines."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    # Track which verses appear together
    verse_co_occurrence = defaultdict(lambda: defaultdict(int))
    verse_to_doctrines = defaultdict(set)
    
    sections = soup.find_all('section', id=True)
    
    for section in sections:
        h2 = section.find('h2')
        doctrine_name = h2.get_text(strip=True) if h2 else "Unknown"
        
        # Find all scripture references in this doctrine
        links = section.find_all('a', href=True)
        verses_in_doctrine = []
        
        for link in links:
            href = link.get('href', '')
            if 'esv.org' in href or 'biblegateway' in href:
                verse_ref = link.get_text(strip=True)
                verses_in_doctrine.append(verse_ref)
                verse_to_doctrines[verse_ref].add(doctrine_name)
        
        # Record co-occurrences
        for i, verse1 in enumerate(verses_in_doctrine):
            for verse2 in verses_in_doctrine[i+1:]:
                verse_co_occurrence[verse1][verse2] += 1
                verse_co_occurrence[verse2][verse1] += 1
    
    return verse_co_occurrence, verse_to_doctrines

def generate_cross_references(verse_co_occurrence, min_occurrences=2):
    """Generate cross-reference suggestions."""
    
    cross_refs = {}
    
    for verse, related in verse_co_occurrence.items():
        # Get top related verses
        sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)
        # Filter by minimum occurrences
        filtered = [(v, count) for v, count in sorted_related if count >= min_occurrences]
        if filtered:
            cross_refs[verse] = filtered[:5]  # Top 5 related verses
    
    return cross_refs

def add_cross_reference_script(cross_refs, verse_to_doctrines):
    """Generate JavaScript for cross-reference suggestions."""
    
    # Prepare data for JavaScript
    cross_ref_data = {}
    for verse, related in cross_refs.items():
        cross_ref_data[verse] = [{'verse': v, 'strength': count} for v, count in related]
    
    doctrine_data = {}
    for verse, doctrines in verse_to_doctrines.items():
        doctrine_data[verse] = list(doctrines)[:3]  # Top 3 doctrines
    
    return f"""
<style>
.cross-ref-panel {{
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
}}
.cross-ref-panel.open {{
    right: 0;
}}
.cross-ref-toggle {{
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
}}
.cross-ref-toggle:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
}}
.cross-ref-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1em;
    padding-bottom: 1em;
    border-bottom: 2px solid #e5e7eb;
}}
.cross-ref-close {{
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    color: #6b7280;
    transition: color 0.2s;
}}
.cross-ref-close:hover {{
    color: #374151;
}}
.cross-ref-item {{
    padding: 1em;
    margin: 0.5em 0;
    background: #f9fafb;
    border-radius: 8px;
    border-left: 3px solid #6366f1;
    cursor: pointer;
    transition: all 0.2s ease;
}}
.cross-ref-item:hover {{
    background: #eff6ff;
    border-left-color: #4f46e5;
    transform: translateX(-4px);
}}
.cross-ref-verse {{
    font-weight: 600;
    color: #4f46e5;
    margin-bottom: 0.25em;
}}
.cross-ref-strength {{
    font-size: 0.85em;
    color: #6b7280;
}}
.cross-ref-doctrines {{
    font-size: 0.8em;
    color: #9ca3af;
    margin-top: 0.5em;
    font-style: italic;
}}
.cross-ref-empty {{
    text-align: center;
    color: #9ca3af;
    padding: 2em;
    font-style: italic;
}}
@media (max-width: 768px) {{
    .cross-ref-panel {{
        width: 100%;
        right: -100%;
    }}
}}
</style>

<button class="cross-ref-toggle" id="crossRefToggle">
    🔗 Cross-References
</button>

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

<script>
(function() {{
    // Cross-reference data
    const crossRefData = {cross_ref_data};
    const doctrineData = {doctrine_data};
    
    const panel = document.getElementById('crossRefPanel');
    const toggle = document.getElementById('crossRefToggle');
    const close = document.getElementById('crossRefClose');
    const content = document.getElementById('crossRefContent');
    
    let currentVerse = null;
    
    // Toggle panel
    toggle.addEventListener('click', () => {{
        panel.classList.toggle('open');
    }});
    
    close.addEventListener('click', () => {{
        panel.classList.remove('open');
    }});
    
    // Show cross-references for a verse
    function showCrossReferences(verse) {{
        currentVerse = verse;
        const refs = crossRefData[verse];
        const doctrines = doctrineData[verse] || [];
        
        if (!refs || refs.length === 0) {{
            content.innerHTML = `
                <div class="cross-ref-empty">
                    <strong>${{verse}}</strong><br><br>
                    No related verses found.<br>
                    This verse appears in: ${{doctrines.join(', ') || 'Unknown'}}
                </div>
            `;
            return;
        }}
        
        let html = `<div style="margin-bottom: 1em; padding: 1em; background: linear-gradient(to right, #eff6ff, #dbeafe); border-radius: 8px;">
                     <strong style="color: #1e40af;">${{verse}}</strong><br>
                     <span style="font-size: 0.9em; color: #6b7280;">Found in: ${{doctrines.join(', ') || 'Multiple doctrines'}}</span>
                    </div>`;
        
        html += '<h4 style="color: #6b7280; font-size: 0.9em; text-transform: uppercase; margin: 1em 0 0.5em 0;">Related Verses:</h4>';
        
        refs.forEach(ref => {{
            const relatedDoctrines = doctrineData[ref.verse] || [];
            const strengthLabel = ref.strength > 5 ? 'Strongly related' : 
                                 ref.strength > 2 ? 'Related' : 'Mentioned together';
            
            html += `
                <div class="cross-ref-item" onclick="showCrossReferences('${{ref.verse}}')">
                    <div class="cross-ref-verse">${{ref.verse}}</div>
                    <div class="cross-ref-strength">${{strengthLabel}} (${{ref.strength}} connection${{ref.strength > 1 ? 's' : ''}})</div>
                    ${{relatedDoctrines.length > 0 ? 
                        `<div class="cross-ref-doctrines">In: ${{relatedDoctrines.join(', ')}}</div>` : ''}}
                </div>
            `;
        }});
        
        content.innerHTML = html;
        
        // Scroll to top of panel
        panel.scrollTop = 0;
    }}
    
    // Add click handlers to all scripture links
    document.addEventListener('click', (e) => {{
        const link = e.target.closest('a[href*="esv.org"], a[href*="biblegateway"]');
        if (link) {{
            const verse = link.textContent.trim();
            if (crossRefData[verse]) {{
                showCrossReferences(verse);
                panel.classList.add('open');
            }}
        }}
    }});
    
    // Also listen for verse link hovers
    const scriptureLinks = document.querySelectorAll('a[href*="esv.org"], a[href*="biblegateway"]');
    scriptureLinks.forEach(link => {{
        link.addEventListener('mouseenter', function() {{
            const verse = this.textContent.trim();
            if (crossRefData[verse] && !panel.classList.contains('open')) {{
                // Optionally auto-show on hover
                // showCrossReferences(verse);
            }}
        }});
    }});
    
    // Expose function globally
    window.showCrossReferences = showCrossReferences;
    
    console.log(`✓ Cross-reference engine enabled with ${{Object.keys(crossRefData).length}} verses`);
}})();
</script>
"""

def add_cross_references(html_file, output_file):
    """Add cross-reference system to HTML file."""
    
    print(f"Analyzing scripture relationships in {html_file}...")
    
    # Extract relationships
    verse_co_occurrence, verse_to_doctrines = extract_verse_relationships(html_file)
    
    # Generate cross-references
    cross_refs = generate_cross_references(verse_co_occurrence, min_occurrences=2)
    
    print(f"  - Found {len(verse_to_doctrines)} unique verses")
    print(f"  - Generated {len(cross_refs)} cross-reference sets")
    
    # Read file
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already exists
    if 'cross-ref-panel' in content:
        print(f"ℹ Cross-references already exist in {html_file}")
        return
    
    # Add script
    script = add_cross_reference_script(cross_refs, verse_to_doctrines)
    
    # Insert before last closing div
    last_div_pos = content.rfind('</div>')
    if last_div_pos != -1:
        before = content[:last_div_pos]
        after = content[last_div_pos:]
        result = before + script + '\n' + after
    else:
        result = content + script
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added cross-references to {output_file}")

def main():
    """Main execution."""
    print("Adding cross-reference suggestion engine...\n")
    
    add_cross_references(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    print("\n✓ Cross-reference system complete!")
    print("  - Click any scripture reference to see related verses")
    print("  - Shows connection strength")
    print("  - Lists doctrines containing each verse")
    print("  - Sliding panel interface")

if __name__ == '__main__':
    main()
