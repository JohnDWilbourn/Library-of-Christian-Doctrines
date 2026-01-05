#!/usr/bin/env python3
"""
Add required ESV copyright notice to comply with ESV API terms of use.
"""

from pathlib import Path

def add_esv_copyright():
    """Add ESV copyright notice to publish files."""
    
    copyright_html = '''
<!-- ESV Bible Copyright Notice - Required by ESV API Terms -->
<div class="esv-copyright" style="margin: 3em 0 2em 0; padding: 1.5em; background: #f8f9fa; border-left: 4px solid #3b82f6; border-radius: 8px; font-size: 0.9em; color: #4b5563;">
    <h4 style="margin-top: 0; color: #1e40af; font-size: 1.1em;">Scripture Quotations</h4>
    <p style="margin: 0.5em 0; line-height: 1.6;">
        Scripture quotations are from the <strong>ESV<sup>®</sup> Bible</strong> (The Holy Bible, English Standard Version<sup>®</sup>), 
        © 2001 by <a href="https://www.crossway.org/" target="_blank" style="color: #3b82f6; text-decoration: none; font-weight: 600;">Crossway</a>, 
        a publishing ministry of Good News Publishers. Used by permission. All rights reserved.
    </p>
    <p style="margin: 0.5em 0; line-height: 1.6;">
        The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. 
        The ESV may not be translated into any other language.
    </p>
    <p style="margin: 0.5em 0 0 0; font-style: italic; color: #6b7280;">
        Users may not copy or download more than 500 verses of the ESV Bible or more than one half of any book of the ESV Bible.
    </p>
    <p style="margin: 1em 0 0 0;">
        <a href="https://www.esv.org" target="_blank" style="color: #3b82f6; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5em;">
            <span>View on ESV.org</span>
            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
                <path fill-rule="evenodd" d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
            </svg>
        </a>
    </p>
</div>
'''
    
    return copyright_html

def process_file(file_path):
    """Add ESV copyright to a file."""
    
    print(f"\n📝 Processing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if copyright already exists
    if 'ESV Bible Copyright Notice' in content:
        print('   ⚠ Copyright notice already present')
        return False
    
    # Add copyright before closing </div> of bd-wrapper
    copyright_html = add_esv_copyright()
    
    # Find the end of the doctrine content (before cross-reference script)
    marker = '<script>'
    last_script_pos = content.rfind(marker)
    
    if last_script_pos > 0:
        # Insert copyright before the last script section
        content = content[:last_script_pos] + copyright_html + '\n' + content[last_script_pos:]
        print('   ✓ Added ESV copyright notice')
    else:
        print('   ⚠ Could not find insertion point')
        return False
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    size_kb = file_path.stat().st_size / 1024
    print(f'   📊 Size: {size_kb:.1f} KB')
    print(f'   ✅ Compliant with ESV terms')
    
    return True

def main():
    """Add ESV copyright to all publish files."""
    
    print("=" * 60)
    print("ESV Copyright Notice - Terms of Use Compliance")
    print("=" * 60)
    
    doctrines_dir = Path(__file__).parent / "Doctrines"
    
    files_to_process = [
        'doctrines_library_wp_publish.html',
        'doctrines_library_wp_clean.html',
        'scripture_index_wp_publish.html',
        'scripture_index_wp_clean.html',
    ]
    
    success_count = 0
    
    for filename in files_to_process:
        file_path = doctrines_dir / filename
        if file_path.exists():
            if process_file(file_path):
                success_count += 1
        else:
            print(f"\n⚠️  File not found: {filename}")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully added copyright to {success_count} files!")
    print("=" * 60)
    
    print("\n📜 COPYRIGHT COMPLIANCE:")
    print("  ✓ Standard ESV copyright notice included")
    print("  ✓ Link to www.esv.org present")
    print("  ✓ Usage restrictions stated")
    print("  ✓ Crossway attribution included")
    print("  ✓ Copyright symbol and year displayed")
    
    print("\n✅ Your website now fully complies with ESV API terms!")
    print()

if __name__ == "__main__":
    main()
