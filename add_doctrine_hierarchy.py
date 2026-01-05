#!/usr/bin/env python3
"""
Add Doctrine Categorization and Hierarchy
Creates a hierarchical organization system for doctrines with collapsible sections.
"""

from bs4 import BeautifulSoup
from collections import defaultdict

# Define doctrine hierarchy
DOCTRINE_HIERARCHY = {
    "Theology Proper (God)": [
        "Doctrine of Divine Essence",
        "Doctrine of the Angel of Yahweh",
        "Doctrine of Operation Footstool",
    ],
    "Christology (Christ)": [
        "Doctrine of the Sustaining Ministry of God the Holy Spirit to the Incarnate Christ",
        "Doctrine of the Hypostatic Union",
        "Doctrine of the Blood of Christ",
    ],
    "Pneumatology (Holy Spirit)": [
        "Doctrine of the Ministry of the Holy Spirit",
    ],
    "Soteriology (Salvation)": [
        "Doctrine of Imputation",
        "Doctrine of Grace",
        "Doctrine of Justification",
        "Doctrine of Unlimited Atonement",
        "Doctrine of Position in Christ",
        "Doctrine of Propitiation",
        "Doctrine of Reconciliation",
        "Doctrine of Eternal Security",
        "Doctrine of Regeneration",
    ],
    "Hamartiology (Sin & Redemption)": [
        "Doctrine of Rebound",
        "Doctrine of Evil",
        "Doctrine of the Sin Unto Death",
        "Devil's Seven",
    ],
    "Spiritual Life": [
        "Summary of the Doctrine of Mental Attitude",
        "Doctrine of the Heart",
        "Doctrine of the Conscience",
        "Doctrine of Happiness",
        "Doctrine of Divine Guidance",
        "Doctrine of Repentance",
        "Prayer",
    ],
    "Ecclesiology (Church)": [
        "Doctrine of Witnessing",
        "Doctrine of the Levitical Priesthood",
        "Summary of the Doctrine of Giving",
        "Royal Family of God",
    ],
    "Discipline & Testing": [
        "Doctrine of Divine Discipline",
    ],
    "Practical Theology": [
        "Doctrine of Money",
        "Thirty-Nine Irrevocable Absolutes and One Revocable Absolute",
        "Delineation of Irrevocable and Revocable Absolutes",
    ],
    "Eschatology & Prophecy": [
        "Doctrine of Days",
    ],
    "History": [
        "Interpretations of History",
    ],
    "Apologetics": [
        "Science and the Bible",
        "Doctrine of Scientific Laws and the Universe",
    ],
}

def create_hierarchy_navigation(soup, wrapper):
    """Create hierarchical navigation menu."""
    
    nav_html = """
<div class="hierarchy-nav" style="margin: 2em 0; padding: 1.5em; background: white; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <h3 style="margin-top: 0; color: #1e40af; font-size: 1.3em; margin-bottom: 1em;">📚 Doctrine Categories</h3>
    <div class="category-buttons" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 0.75em;">
"""
    
    for i, (category, doctrines) in enumerate(DOCTRINE_HIERARCHY.items()):
        count = len(doctrines)
        # Different colors for different categories
        colors = [
            ("#8b5cf6", "#7c3aed"),  # Purple
            ("#ec4899", "#db2777"),  # Pink
            ("#f59e0b", "#d97706"),  # Amber
            ("#10b981", "#059669"),  # Green
            ("#3b82f6", "#2563eb"),  # Blue
            ("#ef4444", "#dc2626"),  # Red
            ("#06b6d4", "#0891b2"),  # Cyan
            ("#8b5cf6", "#7c3aed"),  # Purple (repeat)
            ("#f97316", "#ea580c"),  # Orange
            ("#14b8a6", "#0d9488"),  # Teal
            ("#6366f1", "#4f46e5"),  # Indigo
            ("#a855f7", "#9333ea"),  # Violet
        ]
        color1, color2 = colors[i % len(colors)]
        
        nav_html += f"""
        <button class="category-btn" data-category="{category}" 
                style="padding: 1em; border: 2px solid {color1}; border-radius: 8px; background: linear-gradient(135deg, {color1} 0%, {color2} 100%); color: white; cursor: pointer; text-align: left; transition: all 0.2s ease; font-weight: 600;">
            <div style="font-size: 1.1em; margin-bottom: 0.25em;">{category}</div>
            <div style="font-size: 0.85em; opacity: 0.9;">{count} doctrine{'s' if count != 1 else ''}</div>
        </button>
"""
    
    nav_html += """
    </div>
    <button id="showAllCategories" style="margin-top: 1em; padding: 0.75em 1.5em; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; width: 100%; transition: all 0.2s ease;">
        Show All Doctrines
    </button>
</div>

<style>
.category-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.category-section {
    margin: 2em 0;
    padding: 1.5em;
    background: linear-gradient(to right, #f9fafb, #f3f4f6);
    border-radius: 12px;
    border-left: 4px solid;
}
.category-section h2 {
    margin-top: 0;
    font-size: 1.5em;
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.category-section h2:hover {
    opacity: 0.8;
}
.category-toggle {
    font-size: 0.8em;
    transition: transform 0.3s ease;
}
.category-toggle.collapsed {
    transform: rotate(-90deg);
}
.category-content {
    margin-top: 1em;
}
.category-content.collapsed {
    display: none;
}
</style>

<script>
(function() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    const showAllBtn = document.getElementById('showAllCategories');
    const sections = document.querySelectorAll('.bd-wrapper section[id]');
    
    // Category to doctrine mapping
    const categoryMap = """ + str(DOCTRINE_HIERARCHY).replace("'", '"') + """;
    
    // Create reverse mapping (doctrine title to section id)
    const doctrineTitleToId = {};
    sections.forEach(section => {
        const h2 = section.querySelector('h2');
        if (h2) {
            doctrineTitleToId[h2.textContent.trim()] = section.id;
        }
    });
    
    // Category button click handlers
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const doctrinesInCategory = categoryMap[category] || [];
            
            // Hide all sections first
            sections.forEach(section => {
                section.style.display = 'none';
            });
            
            // Show only sections in this category
            doctrinesInCategory.forEach(doctrineTitle => {
                const sectionId = doctrineTitleToId[doctrineTitle];
                if (sectionId) {
                    const section = document.getElementById(sectionId);
                    if (section) {
                        section.style.display = '';
                        section.style.animation = 'fadeIn 0.3s ease';
                    }
                }
            });
            
            // Scroll to first doctrine
            const firstDoctrineId = doctrineTitleToId[doctrinesInCategory[0]];
            if (firstDoctrineId) {
                document.getElementById(firstDoctrineId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            
            // Highlight active button
            categoryButtons.forEach(b => {
                b.style.opacity = '0.6';
                b.style.transform = 'scale(0.98)';
            });
            this.style.opacity = '1';
            this.style.transform = 'scale(1)';
        });
    });
    
    // Show all button
    showAllBtn.addEventListener('click', function() {
        sections.forEach(section => {
            section.style.display = '';
        });
        categoryButtons.forEach(b => {
            b.style.opacity = '1';
            b.style.transform = 'scale(1)';
        });
    });
    
    console.log('✓ Doctrine hierarchy navigation enabled');
})();
</script>
"""
    
    # Insert after search container
    search_container = wrapper.find('div', class_='search-container')
    if search_container:
        nav_soup = BeautifulSoup(nav_html, 'html.parser')
        search_container.insert_after(nav_soup)

def add_category_headers(soup, wrapper):
    """Add category headers throughout the document."""
    
    # Find all sections
    sections = wrapper.find_all('section', id=True)
    
    # Create a map of doctrine titles to sections
    title_to_section = {}
    for section in sections:
        h2 = section.find('h2')
        if h2:
            title_to_section[h2.get_text(strip=True)] = section
    
    # Track which sections we've already processed
    processed = set()
    
    # Insert category headers
    for category, doctrines in DOCTRINE_HIERARCHY.items():
        first_doctrine = doctrines[0] if doctrines else None
        if first_doctrine and first_doctrine in title_to_section:
            section = title_to_section[first_doctrine]
            
            if section not in processed:
                # Create category header
                category_html = f"""
<div class="category-header" style="margin: 3em 0 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
    <h2 style="margin: 0; font-size: 1.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📖 {category}</h2>
    <p style="margin: 0.5em 0 0 0; opacity: 0.9; font-size: 1.1em;">{len(doctrines)} doctrine{'s' if len(doctrines) != 1 else ''} in this category</p>
</div>
"""
                
                header_soup = BeautifulSoup(category_html, 'html.parser')
                section.insert_before(header_soup)
                processed.add(section)

def add_hierarchy_system(html_file, output_file):
    """Add doctrine hierarchy to the library."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    wrapper = soup.find('div', class_='bd-wrapper')
    if not wrapper:
        print("Error: Could not find bd-wrapper")
        return
    
    # Add navigation menu
    create_hierarchy_navigation(soup, wrapper)
    
    # Add category headers
    add_category_headers(soup, wrapper)
    
    # Extract result
    result = str(wrapper)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added doctrine hierarchy to {output_file}")
    print(f"  - {len(DOCTRINE_HIERARCHY)} categories")
    print(f"  - Category navigation menu")
    print(f"  - Visual category headers")

def main():
    """Main execution."""
    print("Adding doctrine categorization and hierarchy...\n")
    
    add_hierarchy_system(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    print("\n✓ Doctrine hierarchy system complete!")
    print("  - Click category buttons to filter by theological topic")
    print("  - Category headers organize the content")
    print("  - 'Show All Doctrines' to reset view")

if __name__ == '__main__':
    main()
