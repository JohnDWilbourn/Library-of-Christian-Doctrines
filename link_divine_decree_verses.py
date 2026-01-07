#!/usr/bin/env python3
"""
Link all remaining unlinked scripture references in Divine Decree doctrine.
Converts plain text scripture references to ESV.org hyperlinks.
"""

import re
from pathlib import Path

# Bible book name mappings
BOOK_ALIASES = {
    # Old Testament
    'Gen': 'Genesis', 'Genesis': 'Genesis',
    'Ex': 'Exodus', 'Exod': 'Exodus', 'Exodus': 'Exodus',
    'Lev': 'Leviticus', 'Leviticus': 'Leviticus',
    'Num': 'Numbers', 'Numbers': 'Numbers',
    'Deut': 'Deuteronomy', 'Deuteronomy': 'Deuteronomy',
    'Josh': 'Joshua', 'Joshua': 'Joshua',
    'Judg': 'Judges', 'Judges': 'Judges',
    'Ruth': 'Ruth',
    '1 Sam': '1 Samuel', '2 Sam': '2 Samuel',
    '1 Samuel': '1 Samuel', '2 Samuel': '2 Samuel',
    '1 Kings': '1 Kings', '2 Kings': '2 Kings',
    '1 Chron': '1 Chronicles', '2 Chron': '2 Chronicles',
    '1 Chronicles': '1 Chronicles', '2 Chronicles': '2 Chronicles',
    'Ezra': 'Ezra', 'Neh': 'Nehemiah', 'Nehemiah': 'Nehemiah',
    'Esth': 'Esther', 'Esther': 'Esther',
    'Job': 'Job',
    'Ps': 'Psalms', 'Psalm': 'Psalms', 'Psalms': 'Psalms',
    'Prov': 'Proverbs', 'Proverbs': 'Proverbs',
    'Eccles': 'Ecclesiastes', 'Ecclesiastes': 'Ecclesiastes',
    'Song': 'Song of Solomon',
    'Isa': 'Isaiah', 'Isaiah': 'Isaiah',
    'Jer': 'Jeremiah', 'Jeremiah': 'Jeremiah',
    'Lam': 'Lamentations', 'Lamentations': 'Lamentations',
    'Ezek': 'Ezekiel', 'Ezekiel': 'Ezekiel',
    'Dan': 'Daniel', 'Daniel': 'Daniel',
    'Hos': 'Hosea', 'Hosea': 'Hosea',
    'Joel': 'Joel', 'Amos': 'Amos', 'Obad': 'Obadiah', 'Obadiah': 'Obadiah',
    'Jonah': 'Jonah', 'Mic': 'Micah', 'Micah': 'Micah',
    'Nah': 'Nahum', 'Nahum': 'Nahum',
    'Hab': 'Habakkuk', 'Habakkuk': 'Habakkuk',
    'Zeph': 'Zephaniah', 'Zephaniah': 'Zephaniah',
    'Hag': 'Haggai', 'Haggai': 'Haggai',
    'Zech': 'Zechariah', 'Zechariah': 'Zechariah',
    'Mal': 'Malachi', 'Malachi': 'Malachi',
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
    'Titus': 'Titus', 'Philem': 'Philemon', 'Philemon': 'Philemon',
    'Heb': 'Hebrews', 'Hebrews': 'Hebrews',
    'James': 'James',
    '1 Pet': '1 Peter', '2 Pet': '2 Peter',
    '1 Peter': '1 Peter', '2 Peter': '2 Peter',
    '1 John': '1 John', '2 John': '2 John', '3 John': '3 John',
    'Jude': 'Jude',
    'Rev': 'Revelation', 'Revelation': 'Revelation',
}

def link_unlinked_references(content):
    """Link all unlinked scripture references in parentheses."""

    # Build book pattern (sorted by length for proper matching)
    book_names = sorted(BOOK_ALIASES.keys(), key=len, reverse=True)
    book_pattern = '|'.join(re.escape(book) for book in book_names)

    # Pattern to match unlinked references: (Book chapter:verse)
    # Must be in parentheses and NOT already have an <a href
    pattern = r'\((?!<a )(' + book_pattern + r')\.?\s+(\d+):(\d+)([a-z]?)(?:(–|—|-)(\d+)([a-z]?))?(?:,\s*(\d+))?(?:\))'

    def replace_single_ref(match):
        """Replace a single scripture reference."""
        book_raw = match.group(1)
        chapter = match.group(2)
        verse_start = match.group(3)
        verse_suffix = match.group(4) or ''
        dash = match.group(5)
        verse_end = match.group(6)
        end_suffix = match.group(7) or ''

        # Normalize book name
        book = BOOK_ALIASES.get(book_raw, book_raw)
        book_url = book.replace(' ', '+')

        # Build URL
        if verse_end:
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}-{verse_end}"
            ref_text = f"{book_raw} {chapter}:{verse_start}{verse_suffix}{dash}{verse_end}{end_suffix}"
        else:
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}"
            ref_text = f"{book_raw} {chapter}:{verse_start}{verse_suffix}"

        return f'(<a href="{url}" target="_blank">{ref_text}</a>)'

    # Apply single reference pattern
    content = re.sub(pattern, replace_single_ref, content)

    # Also match references without parentheses (inline)
    inline_pattern = r'(?<![(<a])\b(' + book_pattern + r')\.?\s+(\d+):(\d+)([a-z]?)(?:(–|—|-)(\d+)([a-z]?))?(?=[,;.\s])'

    def replace_inline_ref(match):
        """Replace inline scripture references."""
        # Check if already linked
        full_match = match.group(0)

        book_raw = match.group(1)
        chapter = match.group(2)
        verse_start = match.group(3)
        verse_suffix = match.group(4) or ''
        dash = match.group(5)
        verse_end = match.group(6)
        end_suffix = match.group(7) or ''

        # Normalize book name
        book = BOOK_ALIASES.get(book_raw, book_raw)
        book_url = book.replace(' ', '+')

        # Build URL
        if verse_end:
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}-{verse_end}"
            ref_text = f"{book_raw} {chapter}:{verse_start}{verse_suffix}{dash}{verse_end}{end_suffix}"
        else:
            url = f"https://www.esv.org/{book_url}+{chapter}:{verse_start}"
            ref_text = f"{book_raw} {chapter}:{verse_start}{verse_suffix}"

        return f'<a href="{url}" target="_blank">{ref_text}</a>'

    # Apply inline reference pattern (but be careful not to double-link)
    # First, protect already linked references
    protected_content = re.sub(r'<a [^>]*>.*?</a>', lambda m: f'PROTECTED{hash(m.group(0))}PROTECTED', content)
    protected_content = re.sub(inline_pattern, replace_inline_ref, protected_content)
    # Restore protected content
    content = protected_content

    return content


def main():
    """Process the Divine Decree file."""
    file_path = Path('Doctrines/doctrine-of-the-divine-decree/divine-decree_wp_publish.html')

    if not file_path.exists():
        print(f"Error: {file_path} not found")
        return

    print(f"Processing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count unlinked before
    unlinked_pattern = r'\((?!<a )[A-Za-z0-9 \\.]+\s+\d+:\d+'
    before_count = len(re.findall(unlinked_pattern, content))

    # Link references
    content = link_unlinked_references(content)

    # Count unlinked after
    after_count = len(re.findall(unlinked_pattern, content))

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Processed {file_path}")
    print(f"  Unlinked references before: {before_count}")
    print(f"  Unlinked references after: {after_count}")
    print(f"  Linked: {before_count - after_count}")


if __name__ == '__main__':
    main()
