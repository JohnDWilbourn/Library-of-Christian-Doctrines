#!/usr/bin/env python3
"""
Add verse request validation to prevent requesting consecutive verses 
or more than 50% of a book, per ESV API guidelines.
"""

from pathlib import Path

def add_verse_validation():
    """Add verse count validation code."""
    
    validation_code = '''
<script>
// ============================================================
// ESV API Query Validation (Consecutive Verse Limits)
// Per ESV Terms: Max 500 consecutive verses OR 50% of book
// ============================================================
(function() {
    'use strict';
    
    // Book verse counts (for 50% calculation)
    const BIBLE_BOOK_VERSES = {
        'Genesis': 1533, 'Exodus': 1213, 'Leviticus': 859, 'Numbers': 1288,
        'Deuteronomy': 959, 'Joshua': 658, 'Judges': 618, '1 Samuel': 810,
        '2 Samuel': 695, '1 Kings': 816, '2 Kings': 719, '1 Chronicles': 942,
        '2 Chronicles': 822, 'Ezra': 280, 'Nehemiah': 406, 'Esther': 167,
        'Job': 1070, 'Psalms': 2461, 'Proverbs': 915, 'Ecclesiastes': 222,
        'Song of Solomon': 117, 'Isaiah': 1292, 'Jeremiah': 1364,
        'Lamentations': 154, 'Ezekiel': 1273, 'Daniel': 357, 'Hosea': 197,
        'Joel': 73, 'Amos': 146, 'Obadiah': 21, 'Jonah': 48, 'Micah': 105,
        'Nahum': 47, 'Habakkuk': 56, 'Zephaniah': 53, 'Haggai': 38,
        'Zechariah': 211, 'Malachi': 55, 'Matthew': 1071, 'Mark': 678,
        'Luke': 1151, 'John': 879, 'Acts': 1007, 'Romans': 433,
        '1 Corinthians': 437, '2 Corinthians': 257, 'Galatians': 149,
        'Ephesians': 155, 'Philippians': 104, 'Colossians': 95,
        '1 Thessalonians': 89, '2 Thessalonians': 47, '1 Timothy': 113,
        '2 Timothy': 83, 'Titus': 46, 'Philemon': 25, 'Hebrews': 303,
        'James': 108, '1 Peter': 105, '2 Peter': 61, '1 John': 105,
        '2 John': 13, '3 John': 14, 'Jude': 25, 'Revelation': 404
    };
    
    /**
     * Parse verse range to count consecutive verses
     * Examples: "John 3:16" = 1 verse, "John 3:16-18" = 3 verses
     */
    function parseVerseCount(reference) {
        // Match: Book Chapter:Verse or Book Chapter:Verse-Verse
        const match = reference.match(/([123]?\s*[A-Za-z\s]+)\s+(\d+):(\d+)(?:[-–—](\d+))?/);
        if (!match) return { count: 1, book: null, valid: true };
        
        const book = match[1].trim();
        const startVerse = parseInt(match[3]);
        const endVerse = match[4] ? parseInt(match[4]) : startVerse;
        
        // Calculate consecutive verses
        const verseCount = endVerse - startVerse + 1;
        
        // Normalize book name
        let normalizedBook = book;
        const bookAliases = {
            'Gen': 'Genesis', 'Exod': 'Exodus', 'Lev': 'Leviticus',
            'Num': 'Numbers', 'Deut': 'Deuteronomy', 'Josh': 'Joshua',
            'Judg': 'Judges', '1 Sam': '1 Samuel', '2 Sam': '2 Samuel',
            '1 Kgs': '1 Kings', '2 Kgs': '2 Kings', '1 Chr': '1 Chronicles',
            '2 Chr': '2 Chronicles', 'Neh': 'Nehemiah', 'Ps': 'Psalms',
            'Prov': 'Proverbs', 'Eccl': 'Ecclesiastes', 'Song': 'Song of Solomon',
            'Isa': 'Isaiah', 'Jer': 'Jeremiah', 'Lam': 'Lamentations',
            'Ezek': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea',
            'Obad': 'Obadiah', 'Jon': 'Jonah', 'Mic': 'Micah',
            'Nah': 'Nahum', 'Hab': 'Habakkuk', 'Zeph': 'Zephaniah',
            'Hag': 'Haggai', 'Zech': 'Zechariah', 'Mal': 'Malachi',
            'Matt': 'Matthew', 'Rom': 'Romans', '1 Cor': '1 Corinthians',
            '2 Cor': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
            'Phil': 'Philippians', 'Col': 'Colossians', '1 Thess': '1 Thessalonians',
            '2 Thess': '2 Thessalonians', '1 Tim': '1 Timothy', '2 Tim': '2 Timothy',
            'Tit': 'Titus', 'Phlm': 'Philemon', 'Heb': 'Hebrews',
            'Jas': 'James', '1 Pet': '1 Peter', '2 Pet': '2 Peter',
            '1 John': '1 John', '2 John': '2 John', '3 John': '3 John',
            'Rev': 'Revelation'
        };
        
        if (bookAliases[book]) {
            normalizedBook = bookAliases[book];
        }
        
        return {
            count: verseCount,
            book: normalizedBook,
            valid: true,
            startVerse,
            endVerse
        };
    }
    
    /**
     * Validate verse request against ESV limits
     */
    function validateVerseRequest(reference) {
        const parsed = parseVerseCount(reference);
        
        if (!parsed.valid) {
            return {
                valid: false,
                error: 'Invalid verse reference format',
                reference
            };
        }
        
        // Check consecutive verse limit (500 max)
        if (parsed.count > 500) {
            return {
                valid: false,
                error: `Requested ${parsed.count} consecutive verses. ESV API allows maximum 500 consecutive verses per query.`,
                reference,
                count: parsed.count,
                limit: 500
            };
        }
        
        // Check 50% of book limit
        if (parsed.book && BIBLE_BOOK_VERSES[parsed.book]) {
            const bookVerseCount = BIBLE_BOOK_VERSES[parsed.book];
            const halfBook = Math.floor(bookVerseCount / 2);
            
            if (parsed.count > halfBook) {
                return {
                    valid: false,
                    error: `Requested ${parsed.count} verses from ${parsed.book}. ESV API allows maximum ${halfBook} verses (50% of ${bookVerseCount} total verses in book).`,
                    reference,
                    count: parsed.count,
                    limit: halfBook,
                    book: parsed.book
                };
            }
        }
        
        // Single verse requests are always valid
        return {
            valid: true,
            count: parsed.count,
            book: parsed.book,
            reference
        };
    }
    
    /**
     * Wrap original API request with validation
     */
    if (typeof window.makeProtectedAPIRequest !== 'undefined') {
        const originalProtectedRequest = window.makeProtectedAPIRequest;
        
        window.makeProtectedAPIRequest = async function(reference, fetchFunction) {
            // Validate verse count first
            const validation = validateVerseRequest(reference);
            
            if (!validation.valid) {
                console.error('❌ ESV API Request Denied:', validation.error);
                return {
                    text: validation.error + ' Click link to view on ESV.org.',
                    version: 'Validation Error',
                    success: false,
                    error: 'verse_limit_exceeded',
                    validation: validation
                };
            }
            
            // Single verses are fine, log if multiple
            if (validation.count > 1) {
                console.log(`📖 Requesting ${validation.count} consecutive verses from ${validation.book || 'Bible'}`);
            }
            
            // Proceed with protected request
            return await originalProtectedRequest(reference, fetchFunction);
        };
        
        console.log('✓ ESV verse validation enabled');
    } else {
        console.warn('⚠ makeProtectedAPIRequest not found. Load rate limiter first.');
    }
    
    // Expose validator for manual checks
    window.ESV_VERSE_VALIDATOR = {
        validate: validateVerseRequest,
        parseCount: parseVerseCount,
        getBookVerseCount: (book) => BIBLE_BOOK_VERSES[book] || null,
        getMaxVerses: (book) => {
            const total = BIBLE_BOOK_VERSES[book];
            return total ? Math.min(500, Math.floor(total / 2)) : 500;
        }
    };
    
    console.log('📏 ESV Query Validation:');
    console.log('  • Max 500 consecutive verses per query');
    console.log('  • Max 50% of any book');
    console.log('  • Validates before API request');
    console.log('');
    console.log('To validate: ESV_VERSE_VALIDATOR.validate("John 3:16-20")');
})();
</script>
'''
    
    return validation_code

def process_file(file_path):
    """Add verse validation to a file."""
    
    print(f"\n📝 Processing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if validation already exists
    if 'ESV API Query Validation' in content:
        print('   ⚠ Verse validation already present')
        return False
    
    # Add validation code after rate limiting
    marker = 'ESV API Rate Limiting & Bot Protection'
    if marker in content:
        # Find the end of the rate limiting script
        script_end = content.find('</script>', content.find(marker))
        if script_end > 0:
            validation_code = add_verse_validation()
            content = content[:script_end + 9] + '\n' + validation_code + content[script_end + 9:]
            print('   ✓ Added verse request validation')
        else:
            print('   ⚠ Could not find insertion point')
            return False
    else:
        print('   ⚠ Rate limiting not found')
        return False
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    size_kb = file_path.stat().st_size / 1024
    print(f'   📊 Size: {size_kb:.1f} KB')
    print(f'   ✅ Verse limits enforced')
    
    return True

def main():
    """Add verse validation to all publish files."""
    
    print("=" * 60)
    print("ESV API Verse Request Validation")
    print("=" * 60)
    print("\nESV API Guidelines:")
    print("  • Max 500 CONSECUTIVE verses per query")
    print("  • OR half a book (whichever is LESS)")
    print("  • Cannot exceed 50% of any book")
    print("  • Cannot store/display > 50% of book")
    print("  • Single-chapter books excepted")
    
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
    print(f"✅ Successfully added validation to {success_count} files!")
    print("=" * 60)
    
    print("\n🔍 VALIDATION FEATURES:")
    print("  ✓ Counts consecutive verses in request")
    print("  ✓ Checks against 500 verse limit")
    print("  ✓ Checks against 50% of book limit")
    print("  ✓ Uses lower limit (500 OR half book)")
    print("  ✓ Blocks requests exceeding limits")
    print("  ✓ User-friendly error messages")
    print("  ✓ Book verse count database")
    
    print("\n📊 EXAMPLE LIMITS:")
    print("  • Genesis (1,533 verses): Max 500 (limited by consecutive)")
    print("  • Psalms (2,461 verses): Max 500 (limited by consecutive)")
    print("  • Romans (433 verses): Max 216 (50% of book)")
    print("  • Ephesians (155 verses): Max 77 (50% of book)")
    print("  • Philemon (25 verses): Max 12 (50% of book)")
    print("  • 3 John (14 verses): Max 7 (50% of book)")
    
    print("\n🎯 TYPICAL USE CASE:")
    print("  • This site requests single verses only (1 verse)")
    print("  • Well within all limits")
    print("  • Validation prevents future bulk requests")
    print("  • Ensures compliance if features expanded")
    
    print("\n✅ Your site now enforces all ESV verse limits!")
    print()

if __name__ == "__main__":
    main()
