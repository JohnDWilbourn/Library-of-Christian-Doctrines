# Consolidation and Proofing Workflow

## Overview

This guide helps you consolidate multiple HTML page fragments into single documents and proof them before generating WordPress pages.

## Workflow Steps

### Step 1: Gather Your HTML Pages

Collect all HTML fragments for a doctrine. These might be:
- Multiple page files (page1.html, page2.html, etc.)
- A single file with multiple `<!DOCTYPE html>` declarations
- OCR-generated HTML files

### Step 2: Consolidate Pages

Use the consolidation script to merge fragments:

```bash
# Basic usage
python3 Doctrines/doctrine-of-divine-essence/consolidate_doctrine.py <input_file> [output_file]

# Example: Consolidate Divine Essence
cd Doctrines/doctrine-of-divine-essence
python3 consolidate_doctrine.py doctrine-of-divine-essence.html

# Example: Consolidate any doctrine
python3 consolidate_doctrine.py path/to/doctrine.html path/to/doctrine_consolidated.html
```

**What it does:**
- Finds all `<!DOCTYPE html>` boundaries
- Extracts body content from each fragment
- Merges into single HTML document
- Adds section separators
- Creates clean, readable output

**Output:** `*_consolidated.html` file

### Step 3: Proof the Content

Use the proofing tool to review the consolidated content:

```bash
python3 proof_consolidated_content.py <consolidated_file.html>

# Example
python3 proof_consolidated_content.py Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html
```

**What it checks:**
- ✅ Multiple DOCTYPE declarations
- ✅ Continuation markers "(Continued)"
- ✅ Duplicate headings
- ✅ Empty sections
- ✅ Unclosed HTML tags
- ✅ Scripture reference formatting
- ✅ Content statistics

**Output:** `*_review_report.html` - Open in browser to review

### Step 4: Review Checklist

Open the review report HTML file and check:

- [ ] All content sections present and in order
- [ ] No duplicate headings or titles
- [ ] Scripture references properly formatted
- [ ] All links work correctly
- [ ] Content flows logically
- [ ] No continuation markers or artifacts
- [ ] Spelling and grammar checked
- [ ] Ready for WordPress generation

### Step 5: Fix Issues (if needed)

Common fixes:

**Remove continuation markers:**
```bash
# Find them
grep -n "(Continued)" consolidated_file.html

# Edit manually or use sed
sed -i 's/(Continued)//g' consolidated_file.html
```

**Remove duplicate titles:**
- Open consolidated file
- Find duplicate `<h1>` tags
- Remove all but the first one

**Clean empty sections:**
- Look for empty `<div class="section">` tags
- Remove them

### Step 6: Generate WordPress Page

Once content is proofed and ready:

```bash
python3 generate_standalone_doctrine_page.py "Doctrine Name" consolidated_file.html output_file.html

# Example
python3 generate_standalone_doctrine_page.py "Doctrine of Divine Essence" \
    Doctrines/doctrine-of-divine-essence/doctrine-of-divine-essence_consolidated.html \
    Doctrines/doctrine-of-divine-essence_wp_standalone.html
```

## Quick Reference

### Consolidate Multiple Page Files

If you have separate page files (page1.html, page2.html, etc.):

```bash
# Option 1: Concatenate first, then consolidate
cat page1.html page2.html page3.html > combined.html
python3 consolidate_doctrine.py combined.html

# Option 2: Use consolidate script directly (if it supports multiple files)
# (May need to modify script for this)
```

### Common Issues and Solutions

| Issue | Detection | Solution |
|-------|-----------|----------|
| Multiple DOCTYPEs | Proof tool shows error | Already handled by consolidation |
| "(Continued)" markers | Proof tool warning | Remove manually or with sed |
| Duplicate H1 headings | Proof tool warning | Keep first, remove others |
| Empty sections | Proof tool warning | Remove empty divs |
| Missing scripture links | Proof tool info | Run `link_verses_in_doctrines.py` |

## File Naming Convention

For each doctrine, maintain these files:

1. **Original**: `doctrine-name.html` (raw fragments)
2. **Consolidated**: `doctrine-name_consolidated.html` (merged, ready for proofing)
3. **Review Report**: `doctrine-name_consolidated_review_report.html` (proofing output)
4. **WordPress**: `doctrine-name_wp_standalone.html` (final WordPress page)

## Example: Complete Workflow

```bash
# 1. Consolidate
cd Doctrines/my-doctrine/
python3 ../doctrine-of-divine-essence/consolidate_doctrine.py \
    my-doctrine.html \
    my-doctrine_consolidated.html

# 2. Proof
cd ../..
python3 proof_consolidated_content.py \
    Doctrines/my-doctrine/my-doctrine_consolidated.html

# 3. Review (open in browser)
# Open: Doctrines/my-doctrine/my-doctrine_consolidated_review_report.html

# 4. Fix issues (if any)
# Edit: Doctrines/my-doctrine/my-doctrine_consolidated.html

# 5. Generate WordPress page
python3 generate_standalone_doctrine_page.py \
    "My Doctrine" \
    Doctrines/my-doctrine/my-doctrine_consolidated.html \
    Doctrines/my-doctrine_wp_standalone.html
```

## Tips

- **Always keep originals**: Don't delete original fragment files until WordPress page is published
- **Review in browser**: Open consolidated HTML in browser to see how it looks
- **Check scripture links**: Ensure all scripture references link to ESV.org or Bible Gateway
- **Test navigation**: After generating WordPress page, test all navigation links
- **Version control**: Consider committing consolidated files before generating WordPress pages

---

**Tools:**
- `consolidate_doctrine.py` - Merges HTML fragments
- `proof_consolidated_content.py` - Reviews and reports issues
- `generate_standalone_doctrine_page.py` - Creates WordPress-ready pages
