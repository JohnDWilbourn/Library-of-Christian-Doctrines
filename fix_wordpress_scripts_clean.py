#!/usr/bin/env python3
"""
Fix WordPress script loading issues in the clean version too
"""
import re

def fix_wordpress_scripts():
    # Read the clean file
    with open('Doctrines/doctrines_library_wp_clean.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    with open('Doctrines/doctrines_library_wp_clean.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Fixed WordPress script loading in clean version")

if __name__ == '__main__':
    fix_wordpress_scripts()
