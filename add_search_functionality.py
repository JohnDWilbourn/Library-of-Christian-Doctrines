#!/usr/bin/env python3
"""
Add Enhanced Search/Filter Features
Adds JavaScript-based search and filter functionality to the doctrines library and scripture index.
"""

from bs4 import BeautifulSoup
import re

def add_search_to_doctrines(html_file, output_file):
    """Add enhanced search functionality to doctrines library."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create soup
    soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    # Find the wrapper div
    wrapper = soup.find('div', class_='bd-wrapper')
    if not wrapper:
        print("Error: Could not find bd-wrapper")
        return
    
    # Create search box HTML
    search_html = """
<div class="search-container" style="margin: 2em 0; text-align: center;">
    <input type="text" id="doctrineSearch" placeholder="🔍 Search doctrines and scriptures..." style="width: 80%; max-width: 600px; padding: 12px 20px; font-size: 16px; border: 2px solid #3b82f6; border-radius: 25px; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2); transition: all 0.3s ease; outline: none;">
    <div id="searchResults" style="margin-top: 1em; text-align: center; color: #6b7280; font-style: italic;"></div>
</div>
<script>
(function() {
    const searchInput = document.getElementById('doctrineSearch');
    const searchResults = document.getElementById('searchResults');
    const sections = document.querySelectorAll('.bd-wrapper section[id]');
    
    // Add focus effect
    searchInput.addEventListener('focus', function() {
        this.style.borderColor = '#2563eb';
        this.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
    });
    
    searchInput.addEventListener('blur', function() {
        this.style.borderColor = '#3b82f6';
        this.style.boxShadow = '0 2px 8px rgba(59, 130, 246, 0.2)';
    });
    
    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            // Show all sections
            sections.forEach(section => {
                section.style.display = '';
                section.style.opacity = '1';
            });
            searchResults.textContent = '';
            return;
        }
        
        let visibleCount = 0;
        let matchedSections = [];
        
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            const heading = section.querySelector('h2');
            const doctrineName = heading ? heading.textContent : '';
            
            if (text.includes(searchTerm)) {
                section.style.display = '';
                section.style.opacity = '1';
                section.style.animation = 'fadeIn 0.3s ease-in';
                visibleCount++;
                matchedSections.push(doctrineName);
            } else {
                section.style.display = 'none';
                section.style.opacity = '0';
            }
        });
        
        // Update results text
        if (visibleCount === 0) {
            searchResults.textContent = 'No doctrines found matching "' + this.value + '"';
            searchResults.style.color = '#ef4444';
        } else if (visibleCount === sections.length) {
            searchResults.textContent = '';
        } else {
            searchResults.textContent = 'Found ' + visibleCount + ' doctrine(s) matching "' + this.value + '"';
            searchResults.style.color = '#10b981';
        }
    });
    
    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
    
    // Add keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            this.dispatchEvent(new Event('input'));
            this.blur();
        }
    });
})();
</script>
"""
    
    # Find the h1 and insert search box after it
    h1 = wrapper.find('h1')
    if h1:
        search_soup = BeautifulSoup(search_html, 'html.parser')
        h1.insert_after(search_soup)
    
    # Extract just the body content
    result = str(wrapper)
    
    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added search functionality to {output_file}")

def add_search_to_index(html_file, output_file):
    """Add enhanced search functionality to scripture index."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(f'<html><body>{content}</body></html>', 'html.parser')
    
    # Find the wrapper div
    wrapper = soup.find('div', class_='si-wrapper')
    if not wrapper:
        print("Error: Could not find si-wrapper")
        return
    
    # Create search box HTML
    search_html = """
<div class="search-container" style="margin: 2em 0; text-align: center;">
    <input type="text" id="scriptureSearch" placeholder="🔍 Search by book, chapter, or verse..." style="width: 80%; max-width: 600px; padding: 12px 20px; font-size: 16px; border: 2px solid #3b82f6; border-radius: 25px; box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2); transition: all 0.3s ease; outline: none;">
    <div id="searchResults" style="margin-top: 1em; text-align: center; color: #6b7280; font-style: italic;"></div>
</div>
<script>
(function() {
    const searchInput = document.getElementById('scriptureSearch');
    const searchResults = document.getElementById('searchResults');
    const table = document.querySelector('.si-wrapper table');
    const rows = table ? table.querySelectorAll('tbody tr, tr:not(:first-child)') : [];
    
    // Add focus effect
    searchInput.addEventListener('focus', function() {
        this.style.borderColor = '#2563eb';
        this.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
    });
    
    searchInput.addEventListener('blur', function() {
        this.style.borderColor = '#3b82f6';
        this.style.boxShadow = '0 2px 8px rgba(59, 130, 246, 0.2)';
    });
    
    // Search functionality
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            // Show all rows
            rows.forEach(row => {
                if (row.querySelector('th')) return; // Skip header row
                row.style.display = '';
            });
            searchResults.textContent = '';
            return;
        }
        
        let visibleCount = 0;
        
        rows.forEach(row => {
            if (row.querySelector('th')) return; // Skip header row
            
            const text = row.textContent.toLowerCase();
            
            if (text.includes(searchTerm)) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });
        
        // Update results text
        if (visibleCount === 0) {
            searchResults.textContent = 'No scriptures found matching "' + this.value + '"';
            searchResults.style.color = '#ef4444';
        } else {
            searchResults.textContent = 'Showing ' + visibleCount + ' of ' + (rows.length - 1) + ' scripture references';
            searchResults.style.color = '#10b981';
        }
    });
    
    // Add keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            this.value = '';
            this.dispatchEvent(new Event('input'));
            this.blur();
        }
    });
})();
</script>
"""
    
    # Find the container div and insert search box at the beginning
    container = wrapper.find('div', class_='container')
    if container:
        search_soup = BeautifulSoup(search_html, 'html.parser')
        # Insert after the back link
        back_link = container.find('a', class_='back-link')
        if back_link:
            back_link.insert_after(search_soup)
    
    # Extract just the body content
    result = str(wrapper)
    
    # Write to output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added search functionality to {output_file}")

def main():
    """Main execution."""
    print("Adding enhanced search/filter functionality...\n")
    
    # Add search to doctrines library
    add_search_to_doctrines(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    # Add search to scripture index
    add_search_to_index(
        'Doctrines/scripture_index_wp_clean.html',
        'Doctrines/scripture_index_wp_clean.html'
    )
    
    print("\n✓ Enhanced search functionality added to both files!")
    print("  - Doctrines library: Real-time section filtering")
    print("  - Scripture index: Real-time table row filtering")
    print("  - Features: Keyboard shortcuts (ESC to clear), visual feedback, result counts")

if __name__ == '__main__':
    main()
