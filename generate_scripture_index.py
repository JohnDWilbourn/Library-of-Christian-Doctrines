#!/usr/bin/env python3
"""
Generate a scripture index from doctrines_library.html
Extracts all scripture references and organizes them by book
"""

import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

# Bible books in order
BIBLE_BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
    "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther",
    "Job", "Psalms", "Psalm", "Proverbs", "Ecclesiastes", "Song of Solomon",
    "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel",
    "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
    "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi",
    "Matthew", "Mark", "Luke", "John",
    "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians",
    "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
    "1 John", "2 John", "3 John", "Jude", "Revelation"
]

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

class DoctrineHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_section = None
        self.current_section_title = None
        self.in_h2 = False
        self.in_section = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "section":
            for attr, value in attrs:
                if attr == "id":
                    self.current_section = value
                    self.in_section = True
        elif tag == "h2" and self.in_section:
            self.in_h2 = True
    
    def handle_endtag(self, tag):
        if tag == "section":
            self.in_section = False
            self.current_section = None
        elif tag == "h2":
            self.in_h2 = False
    
    def handle_data(self, data):
        if self.in_h2 and self.current_section:
            self.current_section_title = data.strip()

def extract_scripture_references(html_content):
    """Extract all scripture references from HTML content."""
    references = defaultdict(lambda: defaultdict(lambda: {'sections': set(), 'section_ids': set()}))
    
    # Parse HTML to get section information
    parser = DoctrineHTMLParser()
    parser.feed(html_content)
    
    # Multiple patterns to catch different scripture reference formats
    patterns = [
        # Standard format: Book chapter:verse or Book chapter:verse-verse
        r'\b([123]?\s*[A-Z][a-z]+\.?)\s+(\d+):(\d+)(?:[–—\-](\d+))?',
        # Parenthetical references: (Book chapter:verse)
        r'\(([123]?\s*[A-Z][a-z]+\.?)\s+(\d+):(\d+)(?:[–—\-](\d+))?\)',
    ]
    
    # Split content by sections
    sections = re.split(r'<section id="([^"]+)">', html_content)
    
    for i in range(1, len(sections), 2):
        if i+1 < len(sections):
            section_id = sections[i]
            section_content = sections[i+1]
            
            # Extract section title
            title_match = re.search(r'<h2>([^<]+)</h2>', section_content)
            section_title = title_match.group(1) if title_match else section_id
            
            # Find all scripture references using all patterns
            for pattern in patterns:
                matches = re.finditer(pattern, section_content)
                
                for match in matches:
                    book = match.group(1).strip().rstrip('.')
                    # Normalize book name
                    book = BOOK_ALIASES.get(book, book)
                    
                    chapter = match.group(2)
                    verse_start = match.group(3)
                    verse_end = match.group(4) if len(match.groups()) >= 4 and match.group(4) else verse_start
                    
                    ref = f"{chapter}:{verse_start}"
                    if verse_end and verse_end != verse_start:
                        ref += f"–{verse_end}"
                    
                    references[book][ref]['sections'].add(section_title)
                    references[book][ref]['section_ids'].add(section_id)
    
    return references

def generate_html_index(references):
    """Generate HTML for scripture index."""
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('    <meta charset="UTF-8">')
    html.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append('    <title>Scripture Index - Biblical Doctrines</title>')
    html.append('    <style>')
    html.append('        * { box-sizing: border-box; }')
    html.append('        body {')
    html.append('            font-family: Georgia, serif;')
    html.append('            line-height: 1.6;')
    html.append('            max-width: 1400px;')
    html.append('            margin: 0 auto;')
    html.append('            padding: 20px;')
    html.append('            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);')
    html.append('            min-height: 100vh;')
    html.append('        }')
    html.append('        h2 {')
    html.append('            color: #ffffff;')
    html.append('            text-align: center;')
    html.append('            font-size: 2.5em;')
    html.append('            border-bottom: none;')
    html.append('            padding: 1.5em 0;')
    html.append('            margin: 0 0 1em 0;')
    html.append('            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);')
    html.append('        }')
    html.append('        .container {')
    html.append('            background: white;')
    html.append('            border-radius: 12px;')
    html.append('            padding: 2em;')
    html.append('            box-shadow: 0 12px 24px rgba(0,0,0,0.2);')
    html.append('        }')
    html.append('        .header-info {')
    html.append('            text-align: center;')
    html.append('            margin-bottom: 2em;')
    html.append('            padding: 1em;')
    html.append('            background: linear-gradient(to right, #e0f2fe, #dbeafe);')
    html.append('            border-radius: 8px;')
    html.append('            border-left: 4px solid #3b82f6;')
    html.append('        }')
    html.append('        .header-info p {')
    html.append('            margin: 0.5em 0;')
    html.append('            color: #1e40af;')
    html.append('            font-size: 1.1em;')
    html.append('        }')
    html.append('        table {')
    html.append('            width: 100%;')
    html.append('            border-collapse: collapse;')
    html.append('            background-color: white;')
    html.append('            box-shadow: 0 4px 8px rgba(0,0,0,0.08);')
    html.append('            border-radius: 8px;')
    html.append('            overflow: hidden;')
    html.append('        }')
    html.append('        th, td {')
    html.append('            padding: 14px;')
    html.append('            text-align: left;')
    html.append('            border-bottom: 1px solid #e5e7eb;')
    html.append('        }')
    html.append('        th {')
    html.append('            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);')
    html.append('            color: white;')
    html.append('            font-weight: bold;')
    html.append('            position: sticky;')
    html.append('            top: 0;')
    html.append('            z-index: 10;')
    html.append('            text-transform: uppercase;')
    html.append('            font-size: 0.9em;')
    html.append('            letter-spacing: 0.05em;')
    html.append('        }')
    html.append('        tr:nth-child(even) {')
    html.append('            background-color: #f9fafb;')
    html.append('        }')
    html.append('        tr:hover {')
    html.append('            background-color: #eff6ff;')
    html.append('            transform: scale(1.001);')
    html.append('            transition: all 0.2s ease;')
    html.append('        }')
    html.append('        td:first-child {')
    html.append('            font-weight: bold;')
    html.append('            color: #1e40af;')
    html.append('            font-size: 1.05em;')
    html.append('        }')
    html.append('        td:nth-child(2) {')
    html.append('            font-family: "Courier New", monospace;')
    html.append('            color: #3b82f6;')
    html.append('            font-weight: 600;')
    html.append('        }')
    html.append('        td:nth-child(3) {')
    html.append('            font-style: italic;')
    html.append('            color: #6b7280;')
    html.append('            font-size: 0.95em;')
    html.append('        }')
    html.append('        td:nth-child(4) {')
    html.append('            color: #4b5563;')
    html.append('        }')
    html.append('        a {')
    html.append('            color: #2563eb;')
    html.append('            text-decoration: none;')
    html.append('            transition: all 0.2s ease;')
    html.append('            padding: 2px 4px;')
    html.append('            border-radius: 3px;')
    html.append('        }')
    html.append('        a:hover {')
    html.append('            background-color: #dbeafe;')
    html.append('            color: #1e40af;')
    html.append('        }')
    html.append('        .back-link {')
    html.append('            display: inline-block;')
    html.append('            margin-bottom: 1.5em;')
    html.append('            padding: 0.75em 1.5em;')
    html.append('            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);')
    html.append('            color: white;')
    html.append('            border-radius: 8px;')
    html.append('            font-weight: bold;')
    html.append('            box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);')
    html.append('            transition: all 0.3s ease;')
    html.append('        }')
    html.append('        .back-link:hover {')
    html.append('            transform: translateY(-2px);')
    html.append('            box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);')
    html.append('            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);')
    html.append('        }')
    html.append('        @media (max-width: 1024px) {')
    html.append('            body { padding: 15px; }')
    html.append('            .container { padding: 1.5em; }')
    html.append('            h2 { font-size: 2em; padding: 1em 0; }')
    html.append('            table { font-size: 0.95em; }')
    html.append('        }')
    html.append('        @media (max-width: 768px) {')
    html.append('            body { padding: 10px; }')
    html.append('            .container { padding: 1em; }')
    html.append('            h2 { font-size: 1.6em; padding: 0.75em 0; }')
    html.append('            th, td { padding: 10px 8px; font-size: 0.9em; }')
    html.append('            table { display: block; overflow-x: auto; white-space: nowrap; }')
    html.append('            thead, tbody, tr, th, td { display: table-cell; }')
    html.append('            .header-info { font-size: 0.9em; }')
    html.append('        }')
    html.append('        @media (max-width: 480px) {')
    html.append('            h2 { font-size: 1.4em; }')
    html.append('            th, td { padding: 8px 5px; font-size: 0.85em; }')
    html.append('            .back-link { padding: 0.6em 1em; font-size: 0.9em; }')
    html.append('            .header-info p { font-size: 0.95em; }')
    html.append('        }')
    html.append('    </style>')
    html.append('</head>')
    html.append('<body>')
    html.append('')
    html.append('<h2>Scripture Index</h2>')
    html.append('<div class="container">')
    html.append('    <a href="doctrines_library.html" class="back-link">← Back to Doctrines Library</a>')
    html.append('    ')
    html.append('    <div class="header-info">')
    html.append('        <p><strong>Comprehensive Biblical Reference Guide</strong></p>')
    html.append('        <p>All scripture references from the Doctrines Library, organized by book</p>')
    html.append('    </div>')
    html.append('')
    html.append('    <table>')
    html.append('        <tr><th>Book</th><th>Reference</th><th>Excerpt</th><th>Doctrine(s)</th></tr>')
    
    # Sort books by Bible order
    sorted_books = sorted(references.keys(), 
                         key=lambda x: BIBLE_BOOKS.index(x) if x in BIBLE_BOOKS else 999)
    
    for book in sorted_books:
        refs = references[book]
        sorted_refs = sorted(refs.keys(), key=lambda x: (int(x.split(':')[0]), int(x.split(':')[1].split('–')[0])))
        
        for ref in sorted_refs:
            data = refs[ref]
            doctrines = data['sections']
            section_ids = data['section_ids']
            
            # Create ESV.org URL for the verse
            # Format: www.esv.org/BookName+Chapter:Verse
            esv_book = book.replace(' ', '+')
            esv_ref = ref.replace('–', '-')  # ESV uses regular hyphen
            esv_url = f"https://www.esv.org/{esv_book}+{esv_ref}"
            
            # Create links for each doctrine
            doctrine_links = []
            for section_title, section_id in zip(sorted(doctrines), sorted(section_ids)):
                doctrine_links.append(f'<a href="doctrines_library.html#{section_id}">{section_title}</a>')
            
            doctrine_links_str = ', '.join(doctrine_links)
            
            html.append(f'        <tr>')
            html.append(f'            <td>{book}</td>')
            html.append(f'            <td><a href="{esv_url}" target="_blank">{ref}</a></td>')
            html.append(f'            <td>[Verse text to be added]</td>')
            html.append(f'            <td>{doctrine_links_str}</td>')
            html.append(f'        </tr>')
    
    html.append('    </table>')
    html.append('</div>')
    html.append('')
    html.append('</body>')
    html.append('</html>')
    
    return '\n'.join(html)

def main():
    # Read doctrines_library.html
    library_path = Path(__file__).parent / "Doctrines" / "doctrines_library.html"
    with open(library_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract references
    references = extract_scripture_references(content)
    
    # Generate HTML index
    html_index = generate_html_index(references)
    
    # Write to file
    output_path = Path(__file__).parent / "Doctrines" / "scripture_index_new.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_index)
    
    print(f"Scripture index generated: {output_path}")
    print(f"Found {len(references)} books with references")

if __name__ == "__main__":
    main()
