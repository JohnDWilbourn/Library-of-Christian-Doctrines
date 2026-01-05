#!/usr/bin/env python3
"""
Add new doctrines from additional-doctrines-4.html to all doctrine library files.
Updates:
- Main content sections
- Table of Contents
- Category mappings
- Tags
"""

from pathlib import Path
import re

def read_additional_doctrines():
    """Read the new doctrines from additional-doctrines-4.html"""
    path = Path(__file__).parent / "Doctrines" / "additional-doctrines-4.html"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def update_file(filepath, new_doctrines_html):
    """Update a single doctrine library file with new doctrines"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the insertion point (before the closing </body> or before scripture analytics section)
    # Insert before "Thirty-Nine Irrevocable Absolutes" section
    pattern = r'(<section id="absolutes">)'
    
    # Add category headers and separators
    insertion = '\n<div class="doctrine-separator"></div>\n\n'
    
    # Add Devil's Seven to Hamartiology
    insertion += '''<div class="category-header" style="margin: 3em 0 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
<h2 style="margin: 0; font-size: 1.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📖 Additional Hamartiology Doctrines</h2>
<p style="margin: 0.5em 0 0 0; opacity: 0.9; font-size: 1.1em;">1 doctrine in this category</p>
</div>
'''
    
    # Extract Devil's Seven section
    devils_seven_match = re.search(r'<section id="devils-seven">.*?</section>', new_doctrines_html, re.DOTALL)
    if devils_seven_match:
        devils_seven = devils_seven_match.group(0)
        # Add tags
        devils_seven = devils_seven.replace('</section>', 
            '<div class="doctrine-tags" style="margin: 1em 0; padding: 0.5em 0; border-top: 1px solid #e5e7eb;"><span style="color: #6b7280; font-size: 0.9em; font-weight: 600; margin-right: 0.5em;">Tags:</span>' +
            '<span class="tag" data-tag="Angels" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Angels</span>' +
            '<span class="tag" data-tag="Doctrine" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Doctrine</span>' +
            '<span class="tag" data-tag="Satan" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Satan</span>' +
            '<span class="tag" data-tag="Sin" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Sin</span>' +
            '<span class="tag" data-tag="Spiritual Warfare" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Spiritual Warfare</span>' +
            '</div></section>')
        insertion += devils_seven + '\n<div class="doctrine-separator"></div>\n\n'
    
    # Add Prayer to Spiritual Life
    insertion += '''<div class="category-header" style="margin: 3em 0 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
<h2 style="margin: 0; font-size: 1.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📖 Additional Spiritual Life Doctrines</h2>
<p style="margin: 0.5em 0 0 0; opacity: 0.9; font-size: 1.1em;">1 doctrine in this category</p>
</div>
'''
    
    prayer_match = re.search(r'<section id="prayer">.*?</section>', new_doctrines_html, re.DOTALL)
    if prayer_match:
        prayer = prayer_match.group(0)
        prayer = prayer.replace('</section>', 
            '<div class="doctrine-tags" style="margin: 1em 0; padding: 0.5em 0; border-top: 1px solid #e5e7eb;"><span style="color: #6b7280; font-size: 0.9em; font-weight: 600; margin-right: 0.5em;">Tags:</span>' +
            '<span class="tag" data-tag="Doctrine" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Doctrine</span>' +
            '<span class="tag" data-tag="Holy Spirit" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Holy Spirit</span>' +
            '<span class="tag" data-tag="Prayer" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Prayer</span>' +
            '<span class="tag" data-tag="Spiritual Growth" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Spiritual Growth</span>' +
            '</div></section>')
        insertion += prayer + '\n<div class="doctrine-separator"></div>\n\n'
    
    # Add Royal Family to Ecclesiology
    insertion += '''<div class="category-header" style="margin: 3em 0 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
<h2 style="margin: 0; font-size: 1.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📖 Additional Ecclesiology Doctrines</h2>
<p style="margin: 0.5em 0 0 0; opacity: 0.9; font-size: 1.1em;">1 doctrine in this category</p>
</div>
'''
    
    royal_family_match = re.search(r'<section id="royal-family">.*?</section>', new_doctrines_html, re.DOTALL)
    if royal_family_match:
        royal_family = royal_family_match.group(0)
        royal_family = royal_family.replace('</section>', 
            '<div class="doctrine-tags" style="margin: 1em 0; padding: 0.5em 0; border-top: 1px solid #e5e7eb;"><span style="color: #6b7280; font-size: 0.9em; font-weight: 600; margin-right: 0.5em;">Tags:</span>' +
            '<span class="tag" data-tag="Christ" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Christ</span>' +
            '<span class="tag" data-tag="Church Age" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Church Age</span>' +
            '<span class="tag" data-tag="Doctrine" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Doctrine</span>' +
            '<span class="tag" data-tag="Holy Spirit" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Holy Spirit</span>' +
            '<span class="tag" data-tag="Position in Christ" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Position in Christ</span>' +
            '</div></section>')
        insertion += royal_family + '\n<div class="doctrine-separator"></div>\n\n'
    
    # Add Interpretations of History  
    insertion += '''<div class="category-header" style="margin: 3em 0 1.5em 0; padding: 1.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
<h2 style="margin: 0; font-size: 1.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📖 History & Prophecy Doctrines</h2>
<p style="margin: 0.5em 0 0 0; opacity: 0.9; font-size: 1.1em;">1 doctrine in this category</p>
</div>
'''
    
    history_match = re.search(r'<section id="interpretations-history">.*?</section>', new_doctrines_html, re.DOTALL)
    if history_match:
        history = history_match.group(0)
        history = history.replace('</section>', 
            '<div class="doctrine-tags" style="margin: 1em 0; padding: 0.5em 0; border-top: 1px solid #e5e7eb;"><span style="color: #6b7280; font-size: 0.9em; font-weight: 600; margin-right: 0.5em;">Tags:</span>' +
            '<span class="tag" data-tag="Doctrine" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Doctrine</span>' +
            '<span class="tag" data-tag="History" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">History</span>' +
            '<span class="tag" data-tag="Prophecy" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Prophecy</span>' +
            '<span class="tag" data-tag="Sovereignty" style="display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; padding: 0.25em 0.75em; margin: 0.25em; border-radius: 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s ease;">Sovereignty</span>' +
            '</div></section>')
        insertion += history + '\n<div class="doctrine-separator"></div>\n\n'
    
    # Insert the new content
    content = re.sub(pattern, insertion + r'\1', content)
    
    # Update Table of Contents
    toc_pattern = r'(<a href="#absolutes">Thirty-Nine Irrevocable Absolutes)'
    toc_addition = '''<a href="#devils-seven">Doctrine of the Devil's Seven</a> |
        <a href="#prayer">Categorical Doctrine of Prayer</a> |
        <a href="#royal-family">Doctrine of the Royal Family of God</a> |
        <a href="#interpretations-history">Doctrine of the Interpretations of History</a> |
        ''' + r'\1'
    content = re.sub(toc_pattern, toc_addition, content)
    
    # Update categoryMap to add new doctrines
    category_map_pattern = r'("Hamartiology \(Sin & Redemption\)": \[)([^\]]+)(\])'
    content = re.sub(category_map_pattern, 
                    r'\1\2, "Doctrine of the Devil\'s Seven"\3', content)
    
    category_map_pattern2 = r'("Spiritual Life": \[)([^\]]+)(\])'
    content = re.sub(category_map_pattern2, 
                    r'\1\2, "Categorical Doctrine of Prayer"\3', content)
    
    category_map_pattern3 = r'("Ecclesiology \(Church\)": \[)([^\]]+)(\])'
    content = re.sub(category_map_pattern3, 
                    r'\1\2, "Doctrine of the Royal Family of God"\3', content)
    
    # Add new category for Interpretations of History
    eschatology_pattern = r'("Eschatology & Prophecy": \["Doctrine of Days"\])'
    content = re.sub(eschatology_pattern, 
                    r'\1, "History & Interpretation": ["Doctrine of the Interpretations of History"]', content)
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {filepath}")

def main():
    """Main function to update all doctrine files"""
    print("Reading new doctrines from additional-doctrines-4.html...")
    new_doctrines = read_additional_doctrines()
    
    # Update the WordPress publish file
    wp_publish_path = Path(__file__).parent / "Doctrines" / "doctrines_library_wp_publish.html"
    print(f"\nUpdating {wp_publish_path}...")
    update_file(wp_publish_path, new_doctrines)
    
    print("\n✅ All files updated successfully!")
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Commit to Git")
    print("3. Deploy to WordPress")

if __name__ == "__main__":
    main()
