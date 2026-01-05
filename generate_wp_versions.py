#!/usr/bin/env python3
"""
Generate WordPress-ready versions of the HTML files.
Strips HTML structure and scopes CSS to avoid conflicts.
"""

from pathlib import Path
import re

def create_wp_doctrines():
    """Create WordPress version of doctrines_library.html"""
    
    # Read the original file
    source_path = Path(__file__).parent / "Doctrines" / "doctrines_library.html"
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract everything between <body> and </body>
    body_match = re.search(r'<body>(.*)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1).strip()
    else:
        print("Error: Could not find body content")
        return
    
    # Read the WP template
    wp_path = Path(__file__).parent / "Doctrines" / "doctrines_library_wp.html"
    with open(wp_path, 'r', encoding='utf-8') as f:
        wp_template = f.read()
    
    # Replace placeholder with actual content
    wp_content = wp_template.replace('<!-- Content will be inserted here by the Python script -->', body_content)
    
    # Write the final WordPress version
    with open(wp_path, 'w', encoding='utf-8') as f:
        f.write(wp_content)
    
    print(f"WordPress doctrines library generated: {wp_path}")

def create_wp_scripture_index():
    """Create WordPress version of scripture_index_new.html"""
    
    # Read the original file
    source_path = Path(__file__).parent / "Doctrines" / "scripture_index_new.html"
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract content between <body> and </body>
    body_match = re.search(r'<body>(.*)</body>', content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1).strip()
    else:
        print("Error: Could not find body content")
        return
    
    # Create scoped CSS
    css = """<!-- WordPress-Ready Version: Paste this entire content into WordPress Custom HTML block -->
<style>
/* Scoped styles for Scripture Index - prefixed with .si-wrapper to avoid conflicts */
.si-wrapper {
    font-family: Georgia, serif;
    line-height: 1.6;
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    border-radius: 8px;
}
.si-wrapper h2 {
    color: #ffffff;
    text-align: center;
    font-size: 2.5em;
    border-bottom: none;
    padding: 1.5em 0;
    margin: 0 0 1em 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}
.si-wrapper .container {
    background: white;
    border-radius: 12px;
    padding: 2em;
    box-shadow: 0 12px 24px rgba(0,0,0,0.2);
}
.si-wrapper .header-info {
    text-align: center;
    margin-bottom: 2em;
    padding: 1em;
    background: linear-gradient(to right, #e0f2fe, #dbeafe);
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
}
.si-wrapper .header-info p {
    margin: 0.5em 0;
    color: #1e40af;
    font-size: 1.1em;
}
.si-wrapper table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    border-radius: 8px;
    overflow: hidden;
}
.si-wrapper th, .si-wrapper td {
    padding: 14px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}
.si-wrapper th {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    font-weight: bold;
    position: sticky;
    top: 0;
    z-index: 10;
    text-transform: uppercase;
    font-size: 0.9em;
    letter-spacing: 0.05em;
}
.si-wrapper tr:nth-child(even) {
    background-color: #f9fafb;
}
.si-wrapper tr:hover {
    background-color: #eff6ff;
    transform: scale(1.001);
    transition: all 0.2s ease;
}
.si-wrapper td:first-child {
    font-weight: bold;
    color: #1e40af;
    font-size: 1.05em;
}
.si-wrapper td:nth-child(2) {
    font-family: 'Courier New', monospace;
    color: #3b82f6;
    font-weight: 600;
}
.si-wrapper td:nth-child(3) {
    font-style: italic;
    color: #6b7280;
    font-size: 0.95em;
}
.si-wrapper td:nth-child(4) {
    color: #4b5563;
}
.si-wrapper a {
    color: #2563eb;
    text-decoration: none;
    transition: all 0.2s ease;
    padding: 2px 4px;
    border-radius: 3px;
}
.si-wrapper a:hover {
    background-color: #dbeafe;
    color: #1e40af;
}
.si-wrapper .back-link {
    display: inline-block;
    margin-bottom: 1.5em;
    padding: 0.75em 1.5em;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border-radius: 8px;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
}
.si-wrapper .back-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
}
@media (max-width: 1024px) {
    .si-wrapper { padding: 15px; }
    .si-wrapper .container { padding: 1.5em; }
    .si-wrapper h2 { font-size: 2em; padding: 1em 0; }
    .si-wrapper table { font-size: 0.95em; }
}
@media (max-width: 768px) {
    .si-wrapper { padding: 10px; }
    .si-wrapper .container { padding: 1em; }
    .si-wrapper h2 { font-size: 1.6em; padding: 0.75em 0; }
    .si-wrapper th, .si-wrapper td { padding: 10px 8px; font-size: 0.9em; }
    .si-wrapper table { display: block; overflow-x: auto; white-space: nowrap; }
    .si-wrapper thead, .si-wrapper tbody, .si-wrapper tr, .si-wrapper th, .si-wrapper td { display: table-cell; }
    .si-wrapper .header-info { font-size: 0.9em; }
}
@media (max-width: 480px) {
    .si-wrapper h2 { font-size: 1.4em; }
    .si-wrapper th, .si-wrapper td { padding: 8px 5px; font-size: 0.85em; }
    .si-wrapper .back-link { padding: 0.6em 1em; font-size: 0.9em; }
    .si-wrapper .header-info p { font-size: 0.95em; }
}
</style>

<div class="si-wrapper">
"""
    
    # Wrap body content in the wrapper div
    wp_content = css + body_content + "\n</div>"
    
    # Write the WordPress version
    wp_path = Path(__file__).parent / "Doctrines" / "scripture_index_wp.html"
    with open(wp_path, 'w', encoding='utf-8') as f:
        f.write(wp_content)
    
    print(f"WordPress scripture index generated: {wp_path}")

def main():
    create_wp_doctrines()
    create_wp_scripture_index()
    print("\nWordPress-ready files created!")
    print("Copy the entire content of each file and paste into WordPress Custom HTML blocks.")

if __name__ == "__main__":
    main()
