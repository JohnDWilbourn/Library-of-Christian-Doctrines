#!/usr/bin/env python3
"""
Scripture Analytics Generator
Analyzes scripture references across the doctrines library and generates statistics.
"""

import re
from collections import Counter, defaultdict
from bs4 import BeautifulSoup

def extract_scripture_references(html_file):
    """Extract all scripture references and their associated doctrines."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Wrap in proper HTML structure for BeautifulSoup
        soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    references = []
    current_doctrine = ""
    
    # Find all sections
    sections = soup.find_all('section', id=True)
    
    for section in sections:
        # Get doctrine name from h2
        h2 = section.find('h2')
        if h2:
            current_doctrine = h2.get_text(strip=True)
        
        # Find all scripture links in this section
        links = section.find_all('a', href=True)
        for link in links:
            href = link.get('href', '')
            if 'esv.org' in href or 'biblegateway' in href:
                # Extract book and reference from URL or link text
                text = link.get_text(strip=True)
                references.append({
                    'reference': text,
                    'doctrine': current_doctrine,
                    'url': href
                })
    
    return references

def parse_reference(ref_string):
    """Parse a scripture reference into components."""
    # Match patterns like "John 3:16", "Genesis 1:1", "Psalms 119"
    # Handle various formats: "Matt. 1:18", "Isaiah 11:2", "1 Pet. 3:18-19"
    
    # Clean up the reference
    ref_string = ref_string.strip()
    
    # Pattern: optional number + book name + chapter + optional :verse or :verse-verse
    match = re.match(r'([0-9]*\s*[A-Za-z\.]+)\s+(\d+)(?::(\d+))?(?:[-–](\d+))?', ref_string)
    
    if match:
        book = match.group(1).strip().replace('.', '')
        chapter = int(match.group(2))
        verse_start = int(match.group(3)) if match.group(3) else 1
        verse_end = int(match.group(4)) if match.group(4) else verse_start
        
        return {
            'book': book,
            'chapter': chapter,
            'verse_start': verse_start,
            'verse_end': verse_end,
            'verse_count': verse_end - verse_start + 1
        }
    return None

def generate_analytics(references):
    """Generate comprehensive analytics from scripture references."""
    
    # Count references per book
    book_counter = Counter()
    doctrine_counter = Counter()
    book_doctrine_map = defaultdict(set)
    verse_usage = defaultdict(int)
    
    for ref in references:
        parsed = parse_reference(ref['reference'])
        if parsed:
            book = parsed['book']
            book_counter[book] += 1
            doctrine_counter[ref['doctrine']] += 1
            book_doctrine_map[book].add(ref['doctrine'])
            
            # Count individual verses
            for verse in range(parsed['verse_start'], parsed['verse_end'] + 1):
                verse_key = f"{book} {parsed['chapter']}:{verse}"
                verse_usage[verse_key] += 1
    
    return {
        'total_references': len(references),
        'unique_doctrines': len(doctrine_counter),
        'books_referenced': len(book_counter),
        'most_cited_books': book_counter.most_common(10),
        'doctrines_with_most_refs': doctrine_counter.most_common(10),
        'most_referenced_verses': sorted(verse_usage.items(), key=lambda x: x[1], reverse=True)[:20],
        'book_doctrine_coverage': {book: len(doctrines) for book, doctrines in book_doctrine_map.items()}
    }

def generate_analytics_html(analytics):
    """Generate HTML report of analytics."""
    
    # Generate book rows
    book_rows = ""
    for i, (book, count) in enumerate(analytics['most_cited_books'], 1):
        book_rows += f"<tr><td>{i}</td><td>{book}</td><td>{count}</td></tr>\n            "
    
    # Generate doctrine rows
    doctrine_rows = ""
    for i, (doctrine, count) in enumerate(analytics['doctrines_with_most_refs'], 1):
        # Truncate long doctrine names
        short_name = doctrine if len(doctrine) < 80 else doctrine[:77] + "..."
        doctrine_rows += f"<tr><td>{i}</td><td>{short_name}</td><td>{count}</td></tr>\n            "
    
    # Generate verse rows
    verse_rows = ""
    for i, (verse, count) in enumerate(analytics['most_referenced_verses'], 1):
        verse_rows += f"<tr><td>{i}</td><td>{verse}</td><td>{count}</td></tr>\n            "
    
    html = f"""<!-- WordPress-Ready Scripture Analytics -->
<style>
.analytics-wrapper {{
    font-family: Georgia, serif;
    line-height: 1.6;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    border-radius: 8px;
}}
.analytics-wrapper h2 {{
    color: #ffffff;
    text-align: center;
    font-size: 2.5em;
    padding: 1em 0;
    margin: 0 0 0.5em 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}}
.analytics-wrapper .container {{
    background: white;
    border-radius: 12px;
    padding: 2em;
    box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}}
.analytics-wrapper .stat-box {{
    background: linear-gradient(to right, #e0f2fe, #dbeafe);
    border-left: 4px solid #3b82f6;
    padding: 1.5em;
    margin: 1em 0;
    border-radius: 8px;
}}
.analytics-wrapper .stat-box h3 {{
    color: #1e40af;
    margin-top: 0;
}}
.analytics-wrapper .stat-number {{
    font-size: 2.5em;
    font-weight: bold;
    color: #2563eb;
    text-align: center;
    margin: 0.5em 0;
}}
.analytics-wrapper table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-radius: 8px;
    overflow: hidden;
}}
.analytics-wrapper th, .analytics-wrapper td {{
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}}
.analytics-wrapper th {{
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    font-weight: bold;
}}
.analytics-wrapper tr:nth-child(even) {{
    background-color: #f9fafb;
}}
.analytics-wrapper tr:hover {{
    background-color: #eff6ff;
}}
.analytics-wrapper .back-link {{
    display: inline-block;
    margin-bottom: 1.5em;
    padding: 0.75em 1.5em;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border-radius: 8px;
    font-weight: bold;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
}}
.analytics-wrapper .back-link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
}}
</style>

<div class="analytics-wrapper">
<h2>📊 Scripture Analytics Dashboard</h2>
<div class="container">
    <a href="https://intelligencereport.info/complete-library-of-christian-doctrine/" class="back-link">← Back to Doctrines Library</a>
    
    <div class="stat-box">
        <h3>Overview Statistics</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1em;">
            <div>
                <div class="stat-number">{analytics['total_references']}</div>
                <div style="text-align: center; color: #6b7280;">Total Scripture References</div>
            </div>
            <div>
                <div class="stat-number">{analytics['unique_doctrines']}</div>
                <div style="text-align: center; color: #6b7280;">Unique Doctrines</div>
            </div>
            <div>
                <div class="stat-number">{analytics['books_referenced']}</div>
                <div style="text-align: center; color: #6b7280;">Books Referenced</div>
            </div>
        </div>
    </div>
    
    <div class="stat-box">
        <h3>📖 Most Cited Books</h3>
        <table>
            <tr><th>Rank</th><th>Book</th><th>References</th></tr>
            {book_rows}
        </table>
    </div>
    
    <div class="stat-box">
        <h3>📝 Doctrines with Most Scripture References</h3>
        <table>
            <tr><th>Rank</th><th>Doctrine</th><th>References</th></tr>
            {doctrine_rows}
        </table>
    </div>
    
    <div class="stat-box">
        <h3>⭐ Most Referenced Verses</h3>
        <table>
            <tr><th>Rank</th><th>Verse</th><th>Times Used</th></tr>
            {verse_rows}
        </table>
    </div>
</div>
</div>
"""
    
    return html

def main():
    """Main execution."""
    print("Generating scripture analytics...")
    
    # Extract references
    html_file = 'Doctrines/doctrines_library_wp_clean.html'
    references = extract_scripture_references(html_file)
    print(f"✓ Extracted {len(references)} scripture references")
    
    # Generate analytics
    analytics = generate_analytics(references)
    print(f"✓ Analyzed {analytics['total_references']} total references")
    print(f"✓ Found {analytics['unique_doctrines']} unique doctrines")
    print(f"✓ Covered {analytics['books_referenced']} books of the Bible")
    
    # Generate HTML report
    html_output = generate_analytics_html(analytics)
    
    # Save to file
    output_file = 'Doctrines/scripture_analytics_wp.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"\n✓ Analytics report saved to: {output_file}")
    print("\nTop 5 Most Cited Books:")
    for i, (book, count) in enumerate(analytics['most_cited_books'][:5], 1):
        print(f"  {i}. {book}: {count} references")
    
    print("\nTop 5 Most Referenced Verses:")
    for i, (verse, count) in enumerate(analytics['most_referenced_verses'][:5], 1):
        print(f"  {i}. {verse}: used {count} times")

if __name__ == '__main__':
    main()
