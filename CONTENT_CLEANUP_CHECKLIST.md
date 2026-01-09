# Content Cleanup Checklist for All Doctrine Pages

This checklist ensures consistent removal of source material artifacts across all doctrine HTML files.

## Usage

Run this checklist on EVERY doctrine page before polishing or publishing to WordPress.

## Universal Cleanup Patterns

### 1. Remove "Appendix" References ⚠️ CRITICAL

**Why:** Appendix references are artifacts from source PDFs/documents and have no target in web pages.

**Search Command:**
```bash
grep -in "appendix" [filename].html
```

**What to Remove:**
- `(see Appendix B)` or `(see Appendix X)`
- `[See Appendix X]`
- Section headers: `<h2>Appendix A: Title</h2>`
- Footnote references to appendices: `<sup>81</sup> See Appendix B.`
- CSS classes or IDs: `.appendix-title`, `#appendix-section`
- Table of contents entries for appendices

**How to Remove:**
```html
<!-- BEFORE -->
<p>The sovereignty of God is explained in the doctrine of the divine decree (see Appendix B).</p>

<!-- AFTER - Option 1: Simple removal -->
<p>The sovereignty of God is explained in the doctrine of the divine decree.</p>

<!-- AFTER - Option 2: Inline expansion if critical -->
<p>The sovereignty of God is explained in the doctrine of the divine decree in eternity past.</p>
```

**Edge Cases:**
- If footnote ONLY says "See Appendix X" → Remove entire footnote and superscript reference
- If footnote has other content + appendix reference → Keep footnote, remove only appendix reference
- If section titled "Appendix X" has important content → Integrate content into main body OR retitle without "Appendix"

### 2. Remove Dangling Cross-References

**Pattern:** References to sections that don't exist in the web version

**Examples:**
- `(See page 47)`
- `(Reference Chapter 12, Section III)`
- `As discussed on page 123`

**Solution:** Remove or replace with direct topic reference:
```html
<!-- BEFORE -->
<p>This concept is explained on page 47.</p>

<!-- AFTER -->
<p>This concept is explained earlier in this doctrine.</p>
<!-- OR simply remove if redundant -->
```

### 3. Clean Up Footnote Numbering

**Pattern:** Ensure footnotes are sequential and have corresponding text

**Check:**
- Verify every `<sup>XX</sup>` has matching footnote content
- Ensure numbering is sequential (81, 82, 83... no gaps)
- Remove orphaned footnote numbers

**Example Issue:**
```html
<!-- PROBLEM: Footnote 85 references missing Appendix B -->
<sup>85</sup>

<!-- At bottom of page -->
<p><sup>85.</sup> See Appendix B for complete explanation.</p>

<!-- SOLUTION: Remove both -->
```

### 4. Remove PDF/Print Artifacts

**Patterns to Remove:**
- Page break indicators: `<!-- Page Break -->`
- Print margins: `margin-top: 72pt;` (72pt = 1 inch, typical PDF margin)
- Page numbers in content: `Page 47 of 312`
- Running headers/footers embedded in content

### 5. Check for Placeholder Text

**Patterns:**
- `[TODO: Add content here]`
- `[EDITOR'S NOTE: ...]`
- `[INSERT DIAGRAM]`
- `[To be completed]`

**Solution:** Either complete the TODO or remove if not applicable to web version

## Document-Specific Checklist

### For Each Doctrine Page:

- [ ] **Search for "Appendix" (case-insensitive)**
  - [ ] Inline text references removed
  - [ ] Section headers removed or retitled
  - [ ] Footnote references removed
  - [ ] CSS classes/IDs cleaned up
  - [ ] TOC entries removed

- [ ] **Search for page references**
  - [ ] `page [0-9]+` pattern removed
  - [ ] `p. [0-9]+` pattern removed
  - [ ] Chapter/section cross-refs verified or removed

- [ ] **Verify footnotes**
  - [ ] All superscripts have matching footnotes
  - [ ] Numbering is sequential
  - [ ] No orphaned footnote numbers
  - [ ] No footnotes pointing to appendices

- [ ] **Check for PDF artifacts**
  - [ ] No page break comments
  - [ ] No excessive margins (72pt+)
  - [ ] No embedded page numbers

- [ ] **Verify all internal links**
  - [ ] No broken anchor links
  - [ ] No links to non-existent sections
  - [ ] Cross-page navigation links are correct

- [ ] **Check for placeholder text**
  - [ ] No TODO markers
  - [ ] No editorial notes
  - [ ] No missing content indicators

## Grep Commands Cheat Sheet

```bash
# Search for "Appendix" references
grep -in "appendix" filename.html

# Search for page number references
grep -iE "(page|p\.) [0-9]+" filename.html

# Search for footnote superscripts
grep -oE "<sup>[0-9]+</sup>" filename.html | sort -u

# Search for TODO/placeholder text
grep -iE "(todo|editor|insert|to be completed)" filename.html

# Search for all superscript numbers (to verify footnotes)
grep -oE "<sup>[0-9]+</sup>" filename.html | sed 's/<[^>]*>//g' | sort -n

# Find potential orphaned footnotes
grep -E "<p[^>]*><sup>[0-9]+\.</sup>" filename.html
```

## Automated Cleanup Script (Optional)

```bash
#!/bin/bash
# cleanup_doctrine.sh - Run basic cleanup on a doctrine HTML file

FILE="$1"

if [ -z "$FILE" ]; then
    echo "Usage: ./cleanup_doctrine.sh <filename.html>"
    exit 1
fi

echo "Checking $FILE for common artifacts..."

echo -e "\n=== Appendix References ==="
grep -in "appendix" "$FILE" || echo "✓ No appendix references found"

echo -e "\n=== Page Number References ==="
grep -iE "(page|p\.) [0-9]+" "$FILE" || echo "✓ No page references found"

echo -e "\n=== Placeholder Text ==="
grep -iE "(todo|editor|insert|to be completed)" "$FILE" || echo "✓ No placeholders found"

echo -e "\n=== Footnote Numbers Found ==="
grep -oE "<sup>[0-9]+</sup>" "$FILE" | sed 's/<[^>]*>//g' | sort -n | uniq

echo -e "\nDone! Review output above and manually clean up any issues found."
```

## Status Log

Track cleanup status for each doctrine page:

| Page | Appendix Clean | Page Refs Clean | Footnotes Verified | Date | Notes |
|------|---------------|-----------------|-------------------|------|-------|
| Divine Decree | ✓ | - | - | 2026-01-08 | Verified clean |
| Divine Essence | ? | ? | ? | - | Not yet checked |
| Scripture Index | N/A | N/A | N/A | - | No doctrinal content |
| Analytics | N/A | N/A | N/A | - | No doctrinal content |
| Doctrines Library | ? | ? | ? | - | Contains multiple doctrines |

## Priority Order

When cleaning multiple pages, prioritize in this order:

1. **Individual doctrine pages being published** (highest priority)
2. **Doctrines Library main page** (affects all doctrines)
3. **Standalone doctrine pages** (medium priority)
4. **Draft/work-in-progress pages** (lowest priority)

## Notes

- This checklist should be run BEFORE any styling or functionality work
- Content cleanup is faster and less error-prone than visual polish
- One grep command can save multiple queries later
- Always verify changes in WordPress preview before final publish

---

**Document Version:** 1.0
**Created:** 2026-01-08
**Last Updated:** 2026-01-08
**Related Documents:** DIVINE_DECREE_POLISH_INSTRUCTIONS.md
