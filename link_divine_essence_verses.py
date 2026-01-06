#!/usr/bin/env python3
"""
Link all scripture references in the Divine Essence doctrine file.
Converts plain text scripture references to ESV.org hyperlinks.
"""

import re
from pathlib import Path

# Bible book name normalization
BOOK_ALIASES = {
    # Old Testament
    'Gen': 'Genesis', 'Genesis': 'Genesis',
    'Ex': 'Exodus', 'Exod': 'Exodus', 'Exodus': 'Exodus',
    'Lev': 'Leviticus', 'Leviticus': 'Leviticus',
    'Num': 'Numbers', 'Numbers': 'Numbers',
    'Deut': 'Deuteronomy', 'Deuteronomy': 'Deuteronomy',
    'Josh': 'Joshua', 'Joshua': 'Joshua',
    'Judg': 'Judges', 'Judges': 'Judges',
    '1 Sam': '1 Samuel', '2 Sam': '2 Samuel',
    '1 Kings': '1 Kings', '2 Kings': '2 Kings',
    '1 Chron': '1 Chronicles', '2 Chron': '2 Chronicles',
    '1 Chronicles': '1 Chronicles', '2 Chronicles': '2 Chronicles',
    'Ps': 'Psalms', 'Psalm': 'Psalms', 'Psalms': 'Psalms',
    'Prov': 'Proverbs', 'Proverbs': 'Proverbs',
    'Isa': 'Isaiah', 'Isaiah': 'Isaiah',
    'Jer': 'Jeremiah', 'Jeremiah': 'Jeremiah',
    'Ezek': 'Ezekiel', 'Ezekiel': 'Ezekiel',
    'Dan': 'Daniel', 'Daniel': 'Daniel',
    'Mal': 'Malachi', 'Malachi': 'Malachi',
    'Zech': 'Zechariah', 'Zechariah': 'Zechariah',
    'Job': 'Job',
    # New Testament
    'Matt': 'Matthew', 'Matthew': 'Matthew',
    'Mark': 'Mark',
    'Luke': 'Luke',
    'John': 'John',
    'Acts': 'Acts',
    'Rom': 'Romans', 'Romans': 'Romans',
    '1 Cor': '1 Corinthians', '2 Cor': '2 Corinthians',
    '1 Corinthians': '1 Corinthians', '2 Corinthians': '2 Corinthians',
    'Gal': 'Galatians', 'Galatians': 'Galatians',
    'Eph': 'Ephesians', 'Ephesians': 'Ephesians',
    'Phil': 'Philippians', 'Philippians': 'Philippians',
    'Col': 'Colossians', 'Colossians': 'Colossians',
    '1 Thess': '1 Thessalonians', '2 Thess': '2 Thessalonians',
    '1 Thessalonians': '1 Thessalonians', '2 Thessalonians': '2 Thessalonians',
    '1 Tim': '1 Timothy', '2 Tim': '2 Timothy',
    '1 Timothy': '1 Timothy', '2 Timothy': '2 Timothy',
    'Heb': 'Hebrews', 'Hebrews': 'Hebrews',
    'James': 'James',
    '1 Pet': '1 Peter', '2 Pet': '2 Peter',
    '1 Peter': '1 Peter', '2 Peter': '2 Peter',
    '1 John': '1 John', '2 John': '2 John', '3 John': '3 John',
    'Rev': 'Revelation', 'Revelation': 'Revelation',
}

def link_scripture_references(content):
    """Convert plain text scripture references to ESV.org hyperlinks."""

    # Pattern for scripture references: (Book Chapter:Verse) or (Book Chapter:Verse–Verse)
    # Examples: (John 3:16), (Rom. 1:20), (Isa. 55:8-9), (1 John 4:8)

    # Build regex pattern for all book names
    book_pattern = '|'.join(re.escape(book) for book in sorted(BOOK_ALIASES.keys(), key=len, reverse=True))

    # Pattern matches: (Book Chapter:Verse) with optional verse range and letter suffixes
    pattern = r'\((' + book_pattern + r')\.?\s+(\d+):(\d+)([a-z]?)(–|—|-)?(\d+)?([a-z]?)(?:;\s*(\d+):(\d+)([a-z]?)(–|—|-)?(\d+)?([a-z]?))*\)'

    def replace_reference(match):
        """Replace a single scripture reference with a hyperlink."""
        full_match = match.group(0)
        book_raw = match.group(1)

        # Normalize book name
        book = BOOK_ALIASES.get(book_raw, book_raw)
        book_url = book.replace(' ', '+')

        # Extract chapter and verses
        chapter = match.group(2)
        verse_start = match.group(3)
        verse_end = match.group(6) if match.group(6) else verse_start

        # Build URL
        if match.group(6):  # Has verse range
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}-{verse_end}"
        else:
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}"

        # Build link text (preserve original formatting)
        link_text = full_match[1:-1]  # Remove parentheses

        return f'(<a href="{url}" target="_blank">{link_text}</a>)'

    # Apply pattern
    content = re.sub(pattern, replace_reference, content)

    # Handle special cases with semicolons (multiple references)
    # Pattern: (Book 1:1; 2:2; 3:3)
    def handle_multiple_refs(match):
        """Handle multiple scripture references separated by semicolons."""
        refs = match.group(0)[1:-1].split(';')  # Remove parens and split
        book = None
        chapter = None
        linked_refs = []

        for ref in refs:
            ref = ref.strip()

            # Check if this ref has a book name
            book_match = re.match(r'([123]?\s*[A-Z][a-z]+\.?)\s+(\d+):(\d+)', ref)
            if book_match:
                book_raw = book_match.group(1)
                book = BOOK_ALIASES.get(book_raw.strip('.'), book_raw.strip('.'))
                chapter = book_match.group(2)
                verse = book_match.group(3)
                book_url = book.replace(' ', '+')
                url = f"https://www.esv.org/{book_url}+{chapter}:{verse}"
                linked_refs.append(f'<a href="{url}" target="_blank">{ref}</a>')
            # Check if this is just chapter:verse (inherits book)
            elif re.match(r'(\d+):(\d+)', ref) and book:
                chap_verse = re.match(r'(\d+):(\d+)', ref)
                ch = chap_verse.group(1)
                v = chap_verse.group(2)
                book_url = book.replace(' ', '+')
                url = f"https://www.esv.org/{book_url}+{ch}:{v}"
                linked_refs.append(f'<a href="{url}" target="_blank">{ref}</a>')
            else:
                linked_refs.append(ref)

        return f"({'; '.join(linked_refs)})"

    # Find remaining unlinked references with semicolons
    multi_ref_pattern = r'\((?:[123]?\s*[A-Z][a-z]+\.?\s+\d+:\d+[a-z]?(?:;\s*\d+:\d+[a-z]?)+)\)'
    content = re.sub(multi_ref_pattern, handle_multiple_refs, content)

    return content

def process_file(file_path):
    """Process a single doctrine file."""
    print(f"Processing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count references before
    before_count = len(re.findall(r'\([123]?\s*[A-Z][a-z]+\.?\s+\d+:\d+', content))

    # Link scripture references
    content = link_scripture_references(content)

    # Count references after (now as links)
    after_count = len(re.findall(r'<a href="https://www\.esv\.org/', content))

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Processed {file_path}")
    print(f"  Found {before_count} scripture references")
    print(f"  Created {after_count} links")

    return after_count

def main():
    """Main function."""
    file_path = Path('Doctrines/doctrine-of-divine-essence/divine-essence-3_wp_publish.html')

    if not file_path.exists():
        print(f"Error: {file_path} not found")
        return

    total_links = process_file(file_path)
    print(f"\n✓ Complete! Created {total_links} scripture links")

if __name__ == '__main__':
    main()
