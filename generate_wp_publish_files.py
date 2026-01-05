#!/usr/bin/env python3
"""
Generate final WordPress publish files from the enhanced _wp_clean.html files.
Preserves all v3.0 features while creating clean, WordPress-ready content.
"""

from pathlib import Path
import re

def extract_wp_content(html_content):
    """
    Extract content suitable for WordPress Custom HTML blocks.
    Removes any residual HTML document structure tags while preserving all features.
    """
    # Remove DOCTYPE, html, head, body tags if present
    html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'<html[^>]*>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</html>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'<head[^>]*>.*?</head>', '', html_content, flags=re.IGNORECASE | re.DOTALL)
    html_content = re.sub(r'<body[^>]*>', '', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'</body>', '', html_content, flags=re.IGNORECASE)
    
    # Clean up extra whitespace
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    
    return html_content.strip()

def create_publish_file(source_file, output_file):
    """
    Create a WordPress publish file from source.
    """
    print(f"\n📝 Processing: {source_file.name}")
    
    # Read source file
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract WordPress-ready content
    wp_content = extract_wp_content(content)
    
    # Add header comment
    header = f"""<!-- 
============================================================
WordPress Publish Version - Ready to Copy/Paste
============================================================
File: {source_file.name}
Version: 3.0 - Professional Edition
Generated: January 5, 2026

DEPLOYMENT INSTRUCTIONS:
1. Copy this entire file content
2. Go to WordPress page editor
3. Add a "Custom HTML" block
4. Paste the content
5. Update/Publish the page

FEATURES INCLUDED:
✅ Real-time search & filter
✅ Keyword tagging (18 categories)
✅ Doctrine hierarchy (11 theological categories)
✅ Verse preview tooltips
✅ Live Bible API integration (ESV + API.Bible)
✅ Cross-reference engine (937 relationships)
✅ PDF export (4 methods)
✅ PWA support (installable app)
✅ Offline capability
✅ Mobile-optimized
✅ Google Analytics integration

ADDITIONAL SETUP (Optional but Recommended):
• ESV API: Get free key from https://api.esv.org/
• PWA: Upload manifest.json and service-worker.js to site root
• Icons: Add 192x192 and 512x512 PNG app icons
• HTTPS: Required for PWA functionality

For detailed setup instructions, see:
• API_SETUP_GUIDE.md
• PWA_DEPLOYMENT_GUIDE.md

============================================================
-->

"""
    
    # Combine header and content
    final_content = header + wp_content
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    # Get file size
    size_kb = output_file.stat().st_size / 1024
    
    print(f"   ✓ Created: {output_file.name}")
    print(f"   📊 Size: {size_kb:.1f} KB")
    print(f"   🎯 Ready for WordPress Custom HTML block")
    
    return True

def main():
    """Generate all WordPress publish files."""
    
    print("=" * 60)
    print("WordPress Publish File Generator - Version 3.0")
    print("=" * 60)
    
    doctrines_dir = Path(__file__).parent / "Doctrines"
    
    # Define source and output file pairs
    files_to_process = [
        {
            'source': 'doctrines_library_wp_clean.html',
            'output': 'doctrines_library_wp_publish.html',
            'description': 'Main Doctrines Library (All Features)'
        },
        {
            'source': 'scripture_index_wp_clean.html',
            'output': 'scripture_index_wp_publish.html',
            'description': 'Scripture Reference Index'
        },
        {
            'source': 'scripture_analytics_wp.html',
            'output': 'scripture_analytics_wp_publish.html',
            'description': 'Scripture Analytics Dashboard'
        }
    ]
    
    success_count = 0
    
    for file_info in files_to_process:
        source_path = doctrines_dir / file_info['source']
        output_path = doctrines_dir / file_info['output']
        
        if not source_path.exists():
            print(f"\n⚠️  Source file not found: {file_info['source']}")
            continue
        
        print(f"\n📄 {file_info['description']}")
        if create_publish_file(source_path, output_path):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully created {success_count} WordPress publish files!")
    print("=" * 60)
    
    print("\n📦 FILES READY FOR WORDPRESS:")
    print("   📁 Doctrines/doctrines_library_wp_publish.html")
    print("   📁 Doctrines/scripture_index_wp_publish.html")
    print("   📁 Doctrines/scripture_analytics_wp_publish.html")
    
    print("\n🚀 DEPLOYMENT STEPS:")
    print("   1. Open each *_wp_publish.html file")
    print("   2. Copy the entire content")
    print("   3. In WordPress, add Custom HTML block")
    print("   4. Paste content and publish")
    
    print("\n📋 WORDPRESS PAGES TO UPDATE:")
    print("   • intelligencereport.info/bible-doctrines")
    print("   • intelligencereport.info/bible-doctrines-scripture-index")
    print("   • intelligencereport.info/bible-doctrines-analytics")
    
    print("\n🔧 ADDITIONAL FILES TO UPLOAD (for PWA):")
    print("   • manifest.json (site root)")
    print("   • service-worker.js (site root)")
    print("   • App icons: 192x192.png and 512x512.png")
    
    print("\n📖 DOCUMENTATION:")
    print("   • API_SETUP_GUIDE.md - Configure ESV Bible API")
    print("   • PWA_DEPLOYMENT_GUIDE.md - Mobile app setup")
    print("   • VERSION_3.0_SUMMARY.md - Complete feature list")
    
    print("\n🎉 Version 3.0 - Professional Edition is ready to publish!")
    print()

if __name__ == "__main__":
    main()
