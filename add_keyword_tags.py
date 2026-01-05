#!/usr/bin/env python3
"""
Add Keyword Tagging System
Adds automatic keyword tagging and tag-based filtering to the doctrines library.
"""

from bs4 import BeautifulSoup
import re
from collections import defaultdict

# Define keyword categories and keywords
KEYWORD_CATEGORIES = {
    'Salvation': ['salvation', 'saved', 'justification', 'regeneration', 'redemption', 'propitiation', 'reconciliation', 'atonement', 'imputation', 'eternal security'],
    'Holy Spirit': ['holy spirit', 'spirit', 'filling', 'indwelling', 'spirituality', 'spiritual life'],
    'Christ': ['christ', 'jesus', 'lord', 'incarnation', 'hypostatic union', 'deity', 'humanity', 'messiah'],
    'Grace': ['grace', 'unmerited favor', 'divine favor'],
    'Faith': ['faith', 'believe', 'believing', 'trust'],
    'Doctrine': ['doctrine', 'teaching', 'truth', 'bible doctrine', 'word of god'],
    'Sin': ['sin', 'sins', 'sinned', 'transgression', 'iniquity', 'evil', 'carnality'],
    'Church Age': ['church', 'church age', 'believer', 'royal family', 'mystery doctrine'],
    'Spiritual Growth': ['spiritual growth', 'maturity', 'edification', 'sanctification', 'gap', 'spiritual life'],
    'Divine Attributes': ['omnipotence', 'omniscience', 'omnipresence', 'sovereignty', 'eternal', 'immutable', 'divine essence'],
    'Prayer': ['prayer', 'pray', 'praying', 'intercession'],
    'Angels': ['angel', 'angels', 'cherubim', 'seraphim', 'demon', 'demons', 'satan', 'devil'],
    'Priesthood': ['priest', 'priesthood', 'levitical', 'royal priesthood'],
    'Prophecy': ['prophecy', 'prophesy', 'prophecies', 'prophetic', 'future'],
    'Mental Attitude': ['mental attitude', 'thinking', 'mind', 'heart', 'soul', 'conscience', 'emotion'],
    'Divine Discipline': ['discipline', 'judgment', 'chastisement', 'warning discipline'],
    'Giving': ['giving', 'tithing', 'offerings', 'generosity', 'stewardship'],
    'Happiness': ['happiness', 'joy', 'contentment', 'blessing', 'prosperity'],
    'History': ['history', 'historical', 'interpretation', 'interpretations', 'cyclical', 'linear', 'historical cycles'],
}

def extract_keywords_from_doctrine(text, title):
    """Extract relevant keywords from doctrine content."""
    text_lower = text.lower()
    title_lower = title.lower()
    
    found_tags = set()
    
    for category, keywords in KEYWORD_CATEGORIES.items():
        for keyword in keywords:
            # Check if keyword appears in title (higher weight) or content
            if keyword in title_lower or text_lower.count(keyword) >= 2:
                found_tags.add(category)
                break  # One match per category is enough
    
    return sorted(list(found_tags))

def add_tagging_system(html_file, output_file):
    """Add keyword tagging system to doctrines library."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    # Find the wrapper div
    wrapper = soup.find('div', class_='bd-wrapper')
    if not wrapper:
        print("Error: Could not find bd-wrapper")
        return
    
    # Collect all tags and their doctrines
    doctrine_tags = {}
    all_tags = set()
    
    # Process each section
    sections = wrapper.find_all('section', id=True)
    for section in sections:
        h2 = section.find('h2')
        if not h2:
            continue
        
        title = h2.get_text(strip=True)
        content_text = section.get_text()
        
        # Extract keywords
        tags = extract_keywords_from_doctrine(content_text, title)
        doctrine_tags[section.get('id')] = tags
        all_tags.update(tags)
        
        # Add tags to the section
        if tags:
            tags_html = '<div class="doctrine-tags" style="margin: 1em 0; padding: 0.5em 0; border-top: 1px solid #e5e7eb;">'
            tags_html += '<span style="color: #6b7280; font-size: 0.9em; font-weight: 600; margin-right: 0.5em;">Tags:</span>'
            
            for tag in tags:
                tags_html += f'<span class="tag" data-tag="{tag}" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">{tag}</span>'
            
            tags_html += '</div>'
            
            # Insert before the closing section tag
            tags_soup = BeautifulSoup(tags_html, 'html.parser')
            section.append(tags_soup)
    
    # Add tag filter UI
    tag_filter_html = f"""
<div class="tag-filter-container" style="margin: 2em 0; padding: 1.5em; background: linear-gradient(to right, #eff6ff, #dbeafe); border-radius: 12px; border-left: 4px solid #3b82f6;">
    <h3 style="margin-top: 0; color: #1e40af; font-size: 1.2em;">Filter by Topic</h3>
    <div id="tagFilters" style="display: flex; flex-wrap: wrap; gap: 0.5em;">
        <button class="tag-filter-btn active" data-filter="all" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; padding: 0.5em 1em; border-radius: 12px; cursor: pointer; font-weight: 600; transition: all 0.2s ease; box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);">All Topics</button>
        {''.join([f'<button class="tag-filter-btn" data-filter="{tag}" style="background: white; color: #3b82f6; border: 2px solid #3b82f6; padding: 0.5em 1em; border-radius: 12px; cursor: pointer; font-weight: 600; transition: all 0.2s ease;">{tag}</button>' for tag in sorted(all_tags)])}
    </div>
    <div id="filterResults" style="margin-top: 1em; color: #6b7280; font-style: italic;"></div>
</div>

<script>
(function() {{
    const filterButtons = document.querySelectorAll('.tag-filter-btn');
    const sections = document.querySelectorAll('.bd-wrapper section[id]');
    const filterResults = document.getElementById('filterResults');
    const doctrineTags = {repr(doctrine_tags)};
    
    // Add hover effects to filter buttons
    filterButtons.forEach(btn => {{
        btn.addEventListener('mouseenter', function() {{
            if (!this.classList.contains('active')) {{
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 8px rgba(59, 130, 246, 0.3)';
            }}
        }});
        
        btn.addEventListener('mouseleave', function() {{
            if (!this.classList.contains('active')) {{
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            }}
        }});
    }});
    
    // Add click listeners to tag filter buttons
    filterButtons.forEach(btn => {{
        btn.addEventListener('click', function() {{
            const filter = this.getAttribute('data-filter');
            
            // Update active state
            filterButtons.forEach(b => {{
                b.classList.remove('active');
                b.style.background = 'white';
                b.style.color = '#3b82f6';
                b.style.border = '2px solid #3b82f6';
                b.style.boxShadow = 'none';
            }});
            
            this.classList.add('active');
            this.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            this.style.color = 'white';
            this.style.border = 'none';
            this.style.boxShadow = '0 2px 4px rgba(16, 185, 129, 0.3)';
            
            // Filter sections
            let visibleCount = 0;
            
            sections.forEach(section => {{
                const sectionId = section.getAttribute('id');
                const sectionTags = doctrineTags[sectionId] || [];
                
                if (filter === 'all' || sectionTags.includes(filter)) {{
                    section.style.display = '';
                    section.style.opacity = '1';
                    visibleCount++;
                }} else {{
                    section.style.display = 'none';
                    section.style.opacity = '0';
                }}
            }});
            
            // Update results
            if (filter === 'all') {{
                filterResults.textContent = '';
            }} else {{
                filterResults.textContent = `Showing ${{visibleCount}} doctrine(s) tagged with "${{filter}}"`;
                filterResults.style.color = '#10b981';
            }}
        }});
    }});
    
    // Add click listeners to inline tags
    document.addEventListener('click', function(e) {{
        if (e.target.classList.contains('tag')) {{
            const tag = e.target.getAttribute('data-tag');
            const filterBtn = document.querySelector(`[data-filter="${{tag}}"]`);
            if (filterBtn) {{
                filterBtn.click();
                // Scroll to filter section
                document.querySelector('.tag-filter-container').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}
    }});
    
    // Add hover effect to inline tags
    document.querySelectorAll('.tag').forEach(tag => {{
        tag.addEventListener('mouseenter', function() {{
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 2px 6px rgba(37, 99, 235, 0.4)';
        }});
        
        tag.addEventListener('mouseleave', function() {{
            this.style.transform = 'scale(1)';
            this.style.boxShadow = 'none';
        }});
    }});
    
    console.log('✓ Keyword tagging system enabled with {len(all_tags)} categories');
}})();
</script>
"""
    
    # Insert tag filter after search container
    search_container = wrapper.find('div', class_='search-container')
    if search_container:
        filter_soup = BeautifulSoup(tag_filter_html, 'html.parser')
        search_container.insert_after(filter_soup)
    
    # Extract just the wrapper content
    result = str(wrapper)
    
    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added keyword tagging system to {output_file}")
    print(f"  - {len(all_tags)} topic categories")
    print(f"  - Tagged {len(doctrine_tags)} doctrines")
    print(f"  - Topics: {', '.join(sorted(all_tags))}")

def main():
    """Main execution."""
    print("Adding keyword tagging system...\n")
    
    add_tagging_system(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    print("\n✓ Keyword tagging system complete!")
    print("  - Click any tag to filter doctrines by topic")
    print("  - Click 'All Topics' to show all doctrines")
    print("  - Tags are clickable within each doctrine")

if __name__ == '__main__':
    main()
