#!/usr/bin/env python3
"""
Remove old cross-reference scripts and regenerate with fixed version.
"""

import re
from pathlib import Path

def remove_old_cross_refs(content):
    """Remove existing cross-reference script section."""
    # Find the style tag for cross-ref-panel
    pattern = r'<style>\s*\.cross-ref-panel\s*\{.*?</script>\s*</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

def main():
    """Remove old cross-refs from both files."""
    files = [
        Path(__file__).parent / "Doctrines" / "doctrines_library_wp_publish.html",
        Path(__file__).parent / "Doctrines" / "doctrines_library_wp_clean.html"
    ]
    
    for filepath in files:
        print(f"Removing old cross-refs from {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and remove the cross-reference section
        # Look for the style tag starting with .cross-ref-panel
        start_marker = '<style>\n.cross-ref-panel {'
        end_marker = '</script>\n</div>\n\n</body>'
        
        start_pos = content.find(start_marker)
        if start_pos != -1:
            # Find the end of the script section
            end_pos = content.find('</script>', start_pos)
            if end_pos != -1:
                # Include closing div
                end_pos = content.find('</div>', end_pos)
                if end_pos != -1:
                    # Remove the entire section
                    cleaned = content[:start_pos] + content[end_pos + 6:]
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(cleaned)
                    
                    print(f"  ✓ Removed old cross-references")
                else:
                    print(f"  ⚠ Could not find closing div")
            else:
                print(f"  ⚠ Could not find closing script tag")
        else:
            print(f"  ℹ No cross-references found (already clean)")
    
    print("\n✓ Ready to regenerate cross-references")
    print("Run: python3 add_cross_references.py")

if __name__ == "__main__":
    main()
