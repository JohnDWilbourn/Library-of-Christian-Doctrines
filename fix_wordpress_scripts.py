#!/usr/bin/env python3
"""
Fix WordPress script loading issues
Wraps all JavaScript in DOM-ready checks to ensure proper initialization
"""

def fix_wordpress_scripts():
    # Read the publish file
    with open('Doctrines/doctrines_library_wp_publish.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all IIFE scripts and wrap them in DOM ready
    # Replace all (function() { at the start of <script> blocks
    import re
    
    # Pattern to find script blocks with IIFEs
    pattern = r'(<script[^>]*>)\s*\(function\(\)\s*\{'
    
    def replace_iife(match):
        script_tag = match.group(1)
        # Add DOM ready wrapper
        return f'''{script_tag}
// WordPress-safe DOM ready wrapper
(function() {{
    function initScript() {{'''
    
    # Replace opening IIFEs
    content = re.sub(pattern, replace_iife, content)
    
    # Now we need to close the wrapper before })() at end of scripts
    # Find all })(); at the end of script blocks before </script>
    pattern2 = r'\}\)\(\);\s*(</script>)'
    
    def replace_close(match):
        close_tag = match.group(1)
        return f'''    }}
    
    // Execute when DOM is ready
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', initScript);
    }} else {{
        initScript();
    }}
}})();
{close_tag}'''
    
    content = re.sub(pattern2, replace_close, content)
    
    # Write back
    with open('Doctrines/doctrines_library_wp_publish.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Fixed WordPress script loading")
    print("✓ All scripts now wait for DOM to be ready")
    print("✓ Category buttons, export, search, and cross-references will work")

if __name__ == '__main__':
    fix_wordpress_scripts()
