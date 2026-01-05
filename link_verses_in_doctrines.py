#!/usr/bin/env python3
"""
Add ESV.org links to all scripture references in doctrines_library.html
"""

import re
from pathlib import Path

# Normalize book names
BOOK_ALIASES = {
    "Psalm": "Psalms",
    "Ps": "Psalms",
    "1 Sam": "1 Samuel",
    "2 Sam": "2 Samuel",
    "1 Chron": "1 Chronicles",
    "2 Chron": "2 Chronicles",
    "1 Cor": "1 Corinthians",
    "2 Cor": "2 Corinthians",
    "1 Thess": "1 Thessalonians",
    "2 Thess": "2 Thessalonians",
    "1 Tim": "1 Timothy",
    "2 Tim": "2 Timothy",
    "1 Pet": "1 Peter",
    "2 Pet": "2 Peter",
    "Phil": "Philippians",
    "Col": "Colossians",
    "Eph": "Ephesians",
    "Gal": "Galatians",
    "Heb": "Hebrews",
    "Rev": "Revelation",
    "Matt": "Matthew",
    "Prov": "Proverbs",
    "Eccl": "Ecclesiastes",
    "Gen": "Genesis",
    "Ex": "Exodus",
    "Lev": "Leviticus",
    "Num": "Numbers",
    "Neh": "Nehemiah",
    "Deut": "Deuteronomy",
    "Josh": "Joshua",
    "Judg": "Judges",
    "Isa": "Isaiah",
    "Jer": "Jeremiah",
    "Lam": "Lamentations",
    "Ezek": "Ezekiel",
    "Dan": "Daniel",
    "Hos": "Hosea",
    "Obad": "Obadiah",
    "Jon": "Jonah",
    "Mic": "Micah",
    "Nah": "Nahum",
    "Hab": "Habakkuk",
    "Zeph": "Zephaniah",
    "Hag": "Haggai",
    "Zech": "Zechariah",
    "Mal": "Malachi",
    "Rom": "Romans",
    "Tit": "Titus",
}

def link_scripture_reference(match):
    """Convert a scripture reference match to an ESV.org link."""
    full_text = match.group(0)
    book = match.group(1).strip().rstrip('.')
    chapter = match.group(2)
    verse_start = match.group(3)
    verse_end = match.group(4) if len(match.groups()) >= 4 and match.group(4) else None
    
    # Normalize book name
    normalized_book = BOOK_ALIASES.get(book, book)
    
    # Build ESV URL
    esv_book = normalized_book.replace(' ', '+')
    if verse_end and verse_end != verse_start:
        esv_ref = f"{chapter}:{verse_start}-{verse_end}"
    else:
        esv_ref = f"{chapter}:{verse_start}"
    
    esv_url = f"https://www.esv.org/{esv_book}+{esv_ref}"
    
    # Return the linked version
    return f'<a href="{esv_url}" target="_blank">{full_text}</a>'

def process_doctrines_file(file_path):
    """Process the doctrines library file and add links to scripture references."""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match scripture references
    # Look for: Book chapter:verse or Book chapter:verse-verse
    # But NOT when already inside an <a> tag
    pattern = r'(?<![">])([123]?\s*[A-Z][a-z]+\.?)\s+(\d+):(\d+)(?:[–—\-](\d+))?(?=\s|[,;.\)]|<)'
    
    # First, let's protect existing links by temporarily replacing them
    existing_links = []
    def save_link(match):
        existing_links.append(match.group(0))
        return f"___LINK_{len(existing_links)-1}___"
    
    # Save existing <a> tags
    content = re.sub(r'<a[^>]*>.*?</a>', save_link, content, flags=re.DOTALL)
    
    # Now add links to scripture references
    content = re.sub(pattern, link_scripture_reference, content)
    
    # Restore existing links
    for i, link in enumerate(existing_links):
        content = content.replace(f"___LINK_{i}___", link)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Scripture references in {file_path} have been linked to ESV.org")

def main():
    library_path = Path(__file__).parent / "Doctrines" / "doctrines_library.html"
    process_doctrines_file(library_path)

if __name__ == "__main__":
    main()
