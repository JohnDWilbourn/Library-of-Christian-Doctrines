#!/usr/bin/env python3
"""
Add PDF Export Functionality
Adds client-side PDF generation using jsPDF library loaded from CDN.
"""

from bs4 import BeautifulSoup

def add_pdf_export_script():
    """Generate JavaScript for PDF export functionality."""
    
    return """
<!-- PDF Export Functionality -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<style>
.export-menu {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 9999;
}
.export-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    padding: 1em 1.5em;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5em;
    font-size: 16px;
}
.export-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
}
.export-options {
    position: absolute;
    bottom: 70px;
    right: 0;
    background: white;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    padding: 0.5em;
    display: none;
    flex-direction: column;
    gap: 0.5em;
    min-width: 200px;
}
.export-options.show {
    display: flex;
}
.export-option-btn {
    background: white;
    border: 2px solid #e5e7eb;
    padding: 0.75em 1em;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    color: #374151;
    transition: all 0.2s ease;
    text-align: left;
}
.export-option-btn:hover {
    border-color: #10b981;
    background: #f0fdf4;
    color: #059669;
}
.export-progress {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2em 3em;
    border-radius: 12px;
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    z-index: 10000;
    display: none;
    flex-direction: column;
    align-items: center;
    gap: 1em;
}
.export-progress.show {
    display: flex;
}
.progress-bar {
    width: 300px;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #10b981, #059669);
    width: 0%;
    transition: width 0.3s ease;
}
@media print {
    .export-menu, .search-container, .tag-filter-container, .hierarchy-nav {
        display: none !important;
    }
}
</style>

<div class="export-menu">
    <button class="export-btn" id="exportMenuBtn">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 3a1 1 0 00-1 1v5H6a1 1 0 000 2h3v5a1 1 0 102 0v-5h3a1 1 0 100-2h-3V4a1 1 0 00-1-1z"/>
        </svg>
        Export
    </button>
    <div class="export-options" id="exportOptions">
        <button class="export-option-btn" onclick="exportToPrint()">
            🖨️ Print / Save as PDF
        </button>
        <button class="export-option-btn" onclick="exportToSimplePDF()">
            📄 Download PDF (Simple)
        </button>
        <button class="export-option-btn" onclick="exportSelectedDoctrine()">
            📋 Export Current View
        </button>
        <button class="export-option-btn" onclick="exportAllText()">
            📝 Download as Text
        </button>
    </div>
</div>

<div class="export-progress" id="exportProgress">
    <div style="font-size: 1.2em; font-weight: 600; color: #374151;">Generating PDF...</div>
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>
    <div style="font-size: 0.9em; color: #6b7280;" id="progressText">Preparing export...</div>
</div>

<script>
(function() {
    const exportMenuBtn = document.getElementById('exportMenuBtn');
    const exportOptions = document.getElementById('exportOptions');
    const exportProgress = document.getElementById('exportProgress');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    
    // Toggle export menu
    exportMenuBtn.addEventListener('click', function() {
        exportOptions.classList.toggle('show');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!exportMenuBtn.contains(e.target) && !exportOptions.contains(e.target)) {
            exportOptions.classList.remove('show');
        }
    });
    
    // Export to print (browser's native print/PDF)
    window.exportToPrint = function() {
        exportOptions.classList.remove('show');
        window.print();
    };
    
    // Export to simple PDF using jsPDF
    window.exportToSimplePDF = async function() {
        exportOptions.classList.remove('show');
        exportProgress.classList.add('show');
        progressText.textContent = 'Initializing PDF...';
        progressFill.style.width = '10%';
        
        try {
            // Check if jsPDF is loaded
            if (typeof window.jspdf === 'undefined') {
                alert('PDF library is loading. Please try again in a moment.');
                exportProgress.classList.remove('show');
                return;
            }
            
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF('p', 'pt', 'letter');
            
            progressText.textContent = 'Collecting doctrine content...';
            progressFill.style.width = '30%';
            
            // Get all visible sections
            const sections = Array.from(document.querySelectorAll('.bd-wrapper section[id]'))
                .filter(s => s.style.display !== 'none');
            
            let yPos = 40;
            const pageHeight = doc.internal.pageSize.height;
            const margin = 40;
            const maxWidth = doc.internal.pageSize.width - (margin * 2);
            
            // Add title
            doc.setFontSize(24);
            doc.setFont(undefined, 'bold');
            doc.text('Complete Library of Christian Doctrines', margin, yPos);
            yPos += 40;
            
            progressText.textContent = 'Adding doctrines to PDF...';
            progressFill.style.width = '50%';
            
            // Process each section
            for (let i = 0; i < sections.length; i++) {
                const section = sections[i];
                const h2 = section.querySelector('h2');
                
                if (h2) {
                    // Check if we need a new page
                    if (yPos > pageHeight - 100) {
                        doc.addPage();
                        yPos = 40;
                    }
                    
                    // Add doctrine title
                    doc.setFontSize(16);
                    doc.setFont(undefined, 'bold');
                    const title = h2.textContent.trim();
                    const titleLines = doc.splitTextToSize(title, maxWidth);
                    doc.text(titleLines, margin, yPos);
                    yPos += titleLines.length * 20 + 10;
                    
                    // Add basic content note
                    doc.setFontSize(10);
                    doc.setFont(undefined, 'normal');
                    doc.text('See online version for full content and scripture references.', margin, yPos);
                    yPos += 30;
                }
                
                // Update progress
                const progress = 50 + (i / sections.length) * 40;
                progressFill.style.width = progress + '%';
            }
            
            progressText.textContent = 'Finalizing PDF...';
            progressFill.style.width = '95%';
            
            // Save PDF
            const filename = 'Christian-Doctrines-Library-' + new Date().toISOString().split('T')[0] + '.pdf';
            doc.save(filename);
            
            progressFill.style.width = '100%';
            progressText.textContent = 'PDF downloaded successfully!';
            
            setTimeout(() => {
                exportProgress.classList.remove('show');
                progressFill.style.width = '0%';
            }, 2000);
            
        } catch (error) {
            console.error('PDF export error:', error);
            alert('Error generating PDF. Please use Print/Save as PDF option instead.');
            exportProgress.classList.remove('show');
        }
    };
    
    // Export currently visible doctrines
    window.exportSelectedDoctrine = function() {
        exportOptions.classList.remove('show');
        
        const visibleSections = Array.from(document.querySelectorAll('.bd-wrapper section[id]'))
            .filter(s => s.style.display !== 'none');
        
        if (visibleSections.length === 0) {
            alert('No doctrines are currently visible. Please adjust your filters.');
            return;
        }
        
        // Use print with current view
        window.print();
    };
    
    // Export as plain text
    window.exportAllText = function() {
        exportOptions.classList.remove('show');
        
        let textContent = 'COMPLETE LIBRARY OF CHRISTIAN DOCTRINES\\n';
        textContent += '=' .repeat(50) + '\\n\\n';
        
        const sections = document.querySelectorAll('.bd-wrapper section[id]');
        sections.forEach(section => {
            const h2 = section.querySelector('h2');
            if (h2) {
                textContent += h2.textContent.trim() + '\\n';
                textContent += '-'.repeat(h2.textContent.trim().length) + '\\n';
                
                // Get text content (simplified)
                const paragraphs = section.querySelectorAll('p, li');
                paragraphs.forEach(p => {
                    textContent += p.textContent.trim() + '\\n';
                });
                
                textContent += '\\n\\n';
            }
        });
        
        // Create and download blob
        const blob = new Blob([textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Christian-Doctrines-Library-' + new Date().toISOString().split('T')[0] + '.txt';
        a.click();
        URL.revokeObjectURL(url);
    };
    
    console.log('✓ PDF export functionality enabled');
})();
</script>
"""

def add_pdf_export(html_file, output_file):
    """Add PDF export functionality to HTML file."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already exists
    if 'export-menu' in content:
        print(f"ℹ PDF export already exists in {html_file}")
        return
    
    # Find the last closing div and insert before it
    last_div_pos = content.rfind('</div>')
    if last_div_pos != -1:
        before = content[:last_div_pos]
        after = content[last_div_pos:]
        result = before + add_pdf_export_script() + '\n' + after
    else:
        result = content + add_pdf_export_script()
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added PDF export to {output_file}")

def main():
    """Main execution."""
    print("Adding PDF export functionality...\n")
    
    # Add to doctrines library
    add_pdf_export(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    # Add to scripture index
    add_pdf_export(
        'Doctrines/scripture_index_wp_clean.html',
        'Doctrines/scripture_index_wp_clean.html'
    )
    
    # Add to analytics
    try:
        add_pdf_export(
            'Doctrines/scripture_analytics_wp.html',
            'Doctrines/scripture_analytics_wp.html'
        )
    except FileNotFoundError:
        pass
    
    print("\n✓ PDF export functionality added!")
    print("  - Fixed export button in bottom-right corner")
    print("  - Print/Save as PDF (browser native)")
    print("  - Download PDF (jsPDF)")
    print("  - Export current view")
    print("  - Download as plain text")

if __name__ == '__main__':
    main()
