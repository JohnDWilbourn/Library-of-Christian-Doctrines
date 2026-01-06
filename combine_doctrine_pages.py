#!/usr/bin/env python3
"""
Combine TOC + Page Files into Single Doctrine File
===================================================
Combines TOC.html.txt + page1 through page33 (.html and .txt files)
into a single file ready for consolidation and proofing.

Usage:
    python combine_doctrine_pages.py [doctrine_folder]
    
Example:
    python combine_doctrine_pages.py Doctrines/doctrine-of-divine-essence
"""

import sys
from pathlib import Path
import re

def natural_sort_key(text):
    """Sort files naturally: page1, page2, ..., page10, page11"""
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    return [convert(c) for c in re.split(r'(\d+)', text)]

def find_page_files(folder):
    """Find TOC and all page files in order"""
    folder = Path(folder)
    
    # Find TOC file
    toc_files = list(folder.glob('TOC.*'))
    if not toc_files:
        print(f"⚠️  Warning: No TOC file found in {folder}")
        toc_file = None
    else:
        toc_file = toc_files[0]  # Use first TOC file found
        print(f"📑 Found TOC: {toc_file.name}")
    
    # Find all page files (page1 through page33)
    page_files = []
    for ext in ['.html', '.txt', '.hrml']:  # Include .hrml typo
        page_files.extend(folder.glob(f'page*{ext}'))
    
    # Sort naturally: page1, page2, ..., page10, page11, etc.
    page_files.sort(key=lambda p: natural_sort_key(p.stem))
    
    # Filter to page1-page33
    filtered_pages = []
    for page_file in page_files:
        match = re.search(r'page(\d+)', page_file.stem)
        if match:
            page_num = int(match.group(1))
            if 1 <= page_num <= 33:
                filtered_pages.append(page_file)
    
    # Remove duplicates (if both .html and .txt exist, prefer .html)
    seen_pages = {}
    for page_file in filtered_pages:
        page_num = re.search(r'page(\d+)', page_file.stem).group(1)
        if page_num not in seen_pages:
            seen_pages[page_num] = page_file
        elif page_file.suffix == '.html':
            seen_pages[page_num] = page_file  # Prefer .html over .txt
    
    page_files = sorted(seen_pages.values(), key=lambda p: natural_sort_key(p.stem))
    
    print(f"📄 Found {len(page_files)} page files (page1-page33)")
    
    return toc_file, page_files

def combine_files(toc_file, page_files, output_file):
    """Combine TOC + page files into single HTML file"""
    combined_content = []
    
    # Add TOC first
    if toc_file:
        print(f"   Adding: {toc_file.name}")
        with open(toc_file, 'r', encoding='utf-8') as f:
            combined_content.append(f.read())
    
    # Add pages in order
    for page_file in page_files:
        print(f"   Adding: {page_file.name}")
        with open(page_file, 'r', encoding='utf-8') as f:
            combined_content.append(f.read())
    
    # Combine all content
    combined = '\n\n'.join(combined_content)
    
    # Write output
    output_file = Path(output_file)
    output_file.write_text(combined, encoding='utf-8')
    
    return len(combined_content), len(combined)

def main():
    # Determine doctrine folder
    if len(sys.argv) > 1:
        doctrine_folder = Path(sys.argv[1])
    else:
        # Default to divine-essence
        doctrine_folder = Path('Doctrines/doctrine-of-divine-essence')
    
    if not doctrine_folder.exists():
        print(f"❌ Error: Folder not found: {doctrine_folder}")
        sys.exit(1)
    
    print("=" * 60)
    print("📚 Combine Doctrine Pages")
    print("=" * 60)
    print(f"📁 Folder: {doctrine_folder}")
    print()
    
    # Find files
    toc_file, page_files = find_page_files(doctrine_folder)
    
    if not page_files:
        print("❌ Error: No page files found!")
        sys.exit(1)
    
    print()
    print(f"📋 Files to combine:")
    if toc_file:
        print(f"   1. {toc_file.name}")
    for i, page_file in enumerate(page_files, start=2 if toc_file else 1):
        print(f"   {i}. {page_file.name}")
    
    # Output file
    output_file = doctrine_folder / 'doctrine-of-divine-essence.html'
    
    print()
    print(f"💾 Combining into: {output_file.name}")
    print()
    
    # Combine files
    file_count, char_count = combine_files(toc_file, page_files, output_file)
    
    print()
    print("=" * 60)
    print("✅ COMBINE COMPLETE")
    print("=" * 60)
    print(f"   Files combined: {file_count}")
    print(f"   Total size: {char_count:,} characters")
    print(f"   Output: {output_file.name}")
    print()
    print("🚀 Next steps:")
    print("   1. Consolidate: python3 consolidate_doctrine.py doctrine-of-divine-essence.html")
    print("   2. Proof: python3 proof_consolidated_content.py doctrine-of-divine-essence_consolidated.html")
    print("   3. Review the report and fix any issues")
    print("   4. Generate WordPress page when ready")

if __name__ == '__main__':
    main()
