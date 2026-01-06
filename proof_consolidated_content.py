#!/usr/bin/env python3
"""
Proof and Review Tool for Consolidated Doctrine Content
========================================================
Helps review consolidated HTML content before generating WordPress pages.
Identifies common issues, provides statistics, and creates a review-friendly report.

Usage:
    python proof_consolidated_content.py <consolidated_file.html>
    
Example:
    python proof_consolidated_content.py Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html
"""

import re
import sys
from pathlib import Path
from collections import Counter

def extract_text_content(html_content):
    """Extract plain text from HTML for analysis"""
    # Remove script and style tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags but keep text
    text = re.sub(r'<[^>]+>', ' ', html_content)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def find_issues(html_content):
    """Find common issues in consolidated content"""
    issues = []
    
    # Check for duplicate DOCTYPE
    doctype_count = html_content.count('<!DOCTYPE html>')
    if doctype_count > 1:
        issues.append({
            'type': 'error',
            'message': f'Multiple DOCTYPE declarations found ({doctype_count})',
            'fix': 'Should only have one DOCTYPE at the start'
        })
    
    # Check for continuation markers
    continuation_patterns = [
        r'\(Continued\)',
        r'\(continued\)',
        r'Continued',
        r'CONTINUED'
    ]
    for pattern in continuation_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        if matches:
            issues.append({
                'type': 'warning',
                'message': f'Found "{pattern}" markers: {len(matches)} occurrences',
                'fix': 'Consider removing continuation markers after consolidation'
            })
    
    # Check for duplicate main titles
    h1_tags = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL | re.IGNORECASE)
    h1_texts = [re.sub(r'<[^>]+>', '', h).strip() for h in h1_tags]
    h1_counter = Counter(h1_texts)
    duplicates = {text: count for text, count in h1_counter.items() if count > 1}
    if duplicates:
        issues.append({
            'type': 'warning',
            'message': f'Duplicate H1 headings found: {duplicates}',
            'fix': 'Consider removing duplicate main titles'
        })
    
    # Check for empty sections
    empty_sections = re.findall(r'<div[^>]*class=["\']section["\'][^>]*>\s*</div>', html_content, re.IGNORECASE)
    if empty_sections:
        issues.append({
            'type': 'warning',
            'message': f'Empty section divs found: {len(empty_sections)}',
            'fix': 'Remove empty section containers'
        })
    
    # Check for unclosed tags (basic check)
    open_tags = len(re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*>', html_content))
    close_tags = len(re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)>', html_content))
    if abs(open_tags - close_tags) > 10:  # Allow some variance for self-closing tags
        issues.append({
            'type': 'warning',
            'message': f'Possible unclosed tags: {open_tags} open tags vs {close_tags} close tags',
            'fix': 'Review HTML structure for missing closing tags'
        })
    
    # Check for scripture references
    scripture_refs = re.findall(r'\b([1-3]?\s*[A-Z][a-z]+\.?\s+\d+:\d+(?:[–-]\d+)?[a-z]?)', html_content)
    if not scripture_refs:
        issues.append({
            'type': 'info',
            'message': 'No scripture references found',
            'fix': 'Consider adding scripture references or converting to links'
        })
    else:
        issues.append({
            'type': 'info',
            'message': f'Found {len(scripture_refs)} scripture references',
            'fix': 'Verify all references are properly formatted and linked'
        })
    
    return issues

def get_statistics(html_content, text_content):
    """Get statistics about the content"""
    stats = {}
    
    # Basic counts
    stats['total_characters'] = len(html_content)
    stats['total_words'] = len(text_content.split())
    stats['total_lines'] = html_content.count('\n')
    
    # HTML structure
    stats['h1_count'] = len(re.findall(r'<h1[^>]*>', html_content, re.IGNORECASE))
    stats['h2_count'] = len(re.findall(r'<h2[^>]*>', html_content, re.IGNORECASE))
    stats['h3_count'] = len(re.findall(r'<h3[^>]*>', html_content, re.IGNORECASE))
    stats['paragraph_count'] = len(re.findall(r'<p[^>]*>', html_content, re.IGNORECASE))
    stats['list_count'] = len(re.findall(r'<ol[^>]*>|<ul[^>]*>', html_content, re.IGNORECASE))
    stats['link_count'] = len(re.findall(r'<a[^>]*href', html_content, re.IGNORECASE))
    
    # Scripture references
    scripture_refs = re.findall(r'\b([1-3]?\s*[A-Z][a-z]+\.?\s+\d+:\d+(?:[–-]\d+)?[a-z]?)', html_content)
    stats['scripture_references'] = len(scripture_refs)
    stats['unique_scripture_refs'] = len(set(scripture_refs))
    
    # Estimate reading time (average 200 words per minute)
    stats['estimated_reading_time'] = round(stats['total_words'] / 200, 1)
    
    return stats

def create_review_report(input_file, stats, issues):
    """Create a review-friendly HTML report"""
    report_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Review Report - {Path(input_file).name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2em;
            line-height: 1.6;
            background: #f9fafb;
        }}
        h1 {{
            color: #1e40af;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 0.5em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1em;
            margin: 2em 0;
        }}
        .stat-card {{
            background: white;
            padding: 1.5em;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 0.5em 0;
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #1e40af;
        }}
        .issues-section {{
            margin: 2em 0;
        }}
        .issue {{
            background: white;
            padding: 1em;
            margin: 0.5em 0;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        .issue.error {{
            border-left-color: #ef4444;
            background: #fef2f2;
        }}
        .issue.warning {{
            border-left-color: #f59e0b;
            background: #fffbeb;
        }}
        .issue.info {{
            border-left-color: #3b82f6;
            background: #eff6ff;
        }}
        .issue-type {{
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.85em;
            margin-bottom: 0.5em;
        }}
        .issue.error .issue-type {{
            color: #dc2626;
        }}
        .issue.warning .issue-type {{
            color: #d97706;
        }}
        .issue.info .issue-type {{
            color: #2563eb;
        }}
        .fix-suggestion {{
            margin-top: 0.5em;
            padding-top: 0.5em;
            border-top: 1px solid #e5e7eb;
            font-style: italic;
            color: #6b7280;
        }}
        .review-checklist {{
            background: white;
            padding: 1.5em;
            border-radius: 8px;
            margin: 2em 0;
        }}
        .checklist-item {{
            padding: 0.5em 0;
            border-bottom: 1px solid #e5e7eb;
        }}
        .checklist-item:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <h1>📋 Content Review Report</h1>
    <p><strong>File:</strong> {Path(input_file).name}</p>
    <p><strong>Generated:</strong> {Path(input_file).stat().st_mtime if Path(input_file).exists() else 'N/A'}</p>
    
    <h2>📊 Statistics</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <h3>Content Size</h3>
            <div class="stat-value">{stats['total_characters']:,}</div>
            <div>characters</div>
        </div>
        <div class="stat-card">
            <h3>Word Count</h3>
            <div class="stat-value">{stats['total_words']:,}</div>
            <div>words</div>
        </div>
        <div class="stat-card">
            <h3>Reading Time</h3>
            <div class="stat-value">{stats['estimated_reading_time']}</div>
            <div>minutes</div>
        </div>
        <div class="stat-card">
            <h3>Headings</h3>
            <div class="stat-value">{stats['h1_count'] + stats['h2_count'] + stats['h3_count']}</div>
            <div>H1: {stats['h1_count']}, H2: {stats['h2_count']}, H3: {stats['h3_count']}</div>
        </div>
        <div class="stat-card">
            <h3>Scripture References</h3>
            <div class="stat-value">{stats['scripture_references']}</div>
            <div>{stats['unique_scripture_refs']} unique</div>
        </div>
        <div class="stat-card">
            <h3>Links</h3>
            <div class="stat-value">{stats['link_count']}</div>
            <div>total links</div>
        </div>
    </div>
    
    <div class="issues-section">
        <h2>🔍 Issues Found</h2>
        {''.join([
            f'''
        <div class="issue {issue['type']}">
            <div class="issue-type">{issue['type']}</div>
            <div>{issue['message']}</div>
            <div class="fix-suggestion">💡 {issue['fix']}</div>
        </div>
        ''' for issue in issues
        ]) if issues else '<p>✅ No issues found! Content looks good.</p>'}
    </div>
    
    <div class="review-checklist">
        <h2>✅ Review Checklist</h2>
        <div class="checklist-item">
            <input type="checkbox" id="check1"> <label for="check1">All content sections are present and in correct order</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check2"> <label for="check2">No duplicate headings or titles</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check3"> <label for="check3">Scripture references are properly formatted</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check4"> <label for="check4">All links work correctly</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check5"> <label for="check5">Content flows logically from section to section</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check6"> <label for="check6">No continuation markers or page break artifacts</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check7"> <label for="check7">Spelling and grammar checked</label>
        </div>
        <div class="checklist-item">
            <input type="checkbox" id="check8"> <label for="check8">Ready for WordPress page generation</label>
        </div>
    </div>
    
    <h2>📝 Next Steps</h2>
    <ol>
        <li>Review the consolidated HTML file in a browser</li>
        <li>Address any issues found above</li>
        <li>Complete the review checklist</li>
        <li>When ready, generate WordPress standalone page using:
            <pre>python generate_standalone_doctrine_page.py "Doctrine Name" consolidated_file.html</pre>
        </li>
    </ol>
</body>
</html>
'''
    return report_html

def main():
    if len(sys.argv) < 2:
        print("Usage: python proof_consolidated_content.py <consolidated_file.html>")
        print("\nExample:")
        print('  python proof_consolidated_content.py Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html')
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"❌ Error: File not found: {input_file}")
        sys.exit(1)
    
    print(f"📖 Analyzing: {input_file.name}")
    print()
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract text for analysis
    text_content = extract_text_content(html_content)
    
    # Get statistics
    print("📊 Gathering statistics...")
    stats = get_statistics(html_content, text_content)
    
    # Find issues
    print("🔍 Checking for issues...")
    issues = find_issues(html_content)
    
    # Create report
    print("📝 Creating review report...")
    report_html = create_review_report(input_file, stats, issues)
    
    # Write report
    report_file = input_file.parent / f"{input_file.stem}_review_report.html"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_html)
    
    # Print summary
    print()
    print("=" * 60)
    print("📋 REVIEW SUMMARY")
    print("=" * 60)
    print()
    print("📊 Statistics:")
    print(f"   • Total characters: {stats['total_characters']:,}")
    print(f"   • Total words: {stats['total_words']:,}")
    print(f"   • Estimated reading time: {stats['estimated_reading_time']} minutes")
    print(f"   • Headings: {stats['h1_count']} H1, {stats['h2_count']} H2, {stats['h3_count']} H3")
    print(f"   • Scripture references: {stats['scripture_references']} ({stats['unique_scripture_refs']} unique)")
    print(f"   • Links: {stats['link_count']}")
    print()
    
    if issues:
        print(f"🔍 Issues Found: {len(issues)}")
        errors = [i for i in issues if i['type'] == 'error']
        warnings = [i for i in issues if i['type'] == 'warning']
        infos = [i for i in issues if i['type'] == 'info']
        
        if errors:
            print(f"   ❌ Errors: {len(errors)}")
            for issue in errors:
                print(f"      - {issue['message']}")
        
        if warnings:
            print(f"   ⚠️  Warnings: {len(warnings)}")
            for issue in warnings[:3]:  # Show first 3
                print(f"      - {issue['message']}")
            if len(warnings) > 3:
                print(f"      ... and {len(warnings) - 3} more")
        
        if infos:
            print(f"   ℹ️  Info: {len(infos)}")
            for issue in infos:
                print(f"      - {issue['message']}")
    else:
        print("✅ No issues found!")
    
    print()
    print(f"📄 Review report saved: {report_file.name}")
    print()
    print("🚀 Next steps:")
    print("   1. Open the review report in a browser")
    print("   2. Review the consolidated HTML file")
    print("   3. Address any issues found")
    print("   4. When ready, generate WordPress page")

if __name__ == '__main__':
    main()
