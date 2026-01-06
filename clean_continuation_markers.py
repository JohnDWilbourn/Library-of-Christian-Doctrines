#!/usr/bin/env python3
"""
Quick Cleanup: Remove Continuation Markers
===========================================
Removes "(Continued)" markers and other artifacts from consolidated HTML.

Usage:
    python clean_continuation_markers.py <file.html> [output_file.html]
"""

import re
import sys
from pathlib import Path

def clean_continuation_markers(content):
    """Remove continuation markers and related artifacts"""
    changes = []
    
    # Remove "(Continued)" variations
    patterns = [
        (r'\s*\(Continued\)', ''),
        (r'\s*\(continued\)', ''),
        (r'\s*\(CONTINUED\)', ''),
        (r'\s*Continued', ''),
        (r'\s*CONTINUED', ''),
    ]
    
    for pattern, replacement in patterns:
        matches = len(re.findall(pattern, content, re.IGNORECASE))
        if matches > 0:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            changes.append(f"Removed {matches} instances of '{pattern}'")
    
    # Remove duplicate main titles (keep first occurrence)
    h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    h1_matches = list(re.finditer(h1_pattern, content, re.DOTALL | re.IGNORECASE))
    
    if len(h1_matches) > 1:
        # Find common titles (likely duplicates)
        h1_texts = [re.sub(r'<[^>]+>', '', m.group(1)).strip() for m in h1_matches]
        seen_titles = set()
        duplicates_removed = 0
        
        # Keep first occurrence, mark others for removal
        for i, match in enumerate(h1_matches):
            text = h1_texts[i]
            if text.lower() in seen_titles:
                # Remove duplicate
                content = content.replace(match.group(0), '', 1)
                duplicates_removed += 1
            else:
                seen_titles.add(text.lower())
        
        if duplicates_removed > 0:
            changes.append(f"Removed {duplicates_removed} duplicate H1 headings")
    
    # Remove empty section divs
    empty_sections = re.findall(r'<div[^>]*class=["\']section["\'][^>]*>\s*</div>', content, re.IGNORECASE)
    if empty_sections:
        for empty in empty_sections:
            content = content.replace(empty, '')
        changes.append(f"Removed {len(empty_sections)} empty section divs")
    
    return content, changes

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_continuation_markers.py <file.html> [output_file.html]")
        print("\nExample:")
        print('  python clean_continuation_markers.py doctrine_consolidated.html')
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.parent / f"{input_file.stem}_cleaned.html"
    
    if not input_file.exists():
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)
    
    print(f"🧹 Cleaning: {input_file.name}")
    print(f"💾 Output: {output_file.name}")
    print()
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # Clean
    cleaned_content, changes = clean_continuation_markers(content)
    
    new_size = len(cleaned_content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    # Print summary
    print("✅ Cleanup complete!")
    print()
    if changes:
        print("Changes made:")
        for change in changes:
            print(f"   • {change}")
    else:
        print("   No changes needed - file already clean!")
    
    print()
    print(f"   Size: {original_size:,} → {new_size:,} characters")
    print(f"   Reduction: {original_size - new_size:,} characters ({100 * (original_size - new_size) / original_size:.1f}%)")
    print()
    print(f"📄 Cleaned file saved: {output_file.name}")
    print()
    print("💡 Tip: Run proof_consolidated_content.py again to verify cleanup")

if __name__ == '__main__':
    main()
