#!/usr/bin/env python3
"""
Fix all unlinked scripture references in doctrine library files.
Converts plain text scripture references to ESV API hyperlinks.
"""

import re
from pathlib import Path

def fix_unlinked_references(content):
    """Fix unlinked scripture references."""
    
    # Pattern 1: (1 John 4:8b; 4:16) - split chapter:verse references
    content = re.sub(
        r'\(1 John 4:8b; 4:16\)',
        r'(<a href="https://www.esv.org/1+John+4:8" target="_blank">1 John 4:8b</a>; <a href="https://www.esv.org/1+John+4:16" target="_blank">4:16</a>)',
        content
    )
    
    # Pattern 2: Simple unlinked references like (Acts 1:8a)
    content = re.sub(
        r'\(Acts 1:8a\)',
        r'(<a href="https://www.esv.org/Acts+1:8" target="_blank">Acts 1:8a</a>)',
        content
    )
    
    # Pattern 3: (Acts 4:12b; with already linked reference after)
    content = re.sub(
        r'\(Acts 4:12b; ',
        r'(<a href="https://www.esv.org/Acts+4:12" target="_blank">Acts 4:12b</a>; ',
        content
    )
    
    # Pattern 4: (1 John 3:23b)
    content = re.sub(
        r'\(1 John 3:23b\)',
        r'(<a href="https://www.esv.org/1+John+3:23" target="_blank">1 John 3:23b</a>)',
        content
    )
    
    # Pattern 5: verse references in Acts 1 section
    content = re.sub(r'\(verse 5\)', r'(<a href="https://www.esv.org/Acts+1:5" target="_blank">verse 5</a>)', content)
    content = re.sub(r'\(verse 6\)', r'(<a href="https://www.esv.org/Acts+1:6" target="_blank">verse 6</a>)', content)
    content = re.sub(r'\(verses 7–10\)', r'(<a href="https://www.esv.org/Acts+1:7-10" target="_blank">verses 7–10</a>)', content)
    content = re.sub(r'\(verse 11\)', r'(<a href="https://www.esv.org/Acts+1:11" target="_blank">verse 11</a>)', content)
    content = re.sub(r'\(verse 12\)', r'(<a href="https://www.esv.org/Acts+1:12" target="_blank">verse 12</a>)', content)
    content = re.sub(r'\(verses 13–15\)', r'(<a href="https://www.esv.org/Acts+1:13-15" target="_blank">verses 13–15</a>)', content)
    content = re.sub(r'\(verse 16\)', r'(<a href="https://www.esv.org/Acts+1:16" target="_blank">verse 16</a>)', content)
    
    # Pattern 6: Devil's Seven references
    content = re.sub(r'\(John 8:44\)', r'(<a href="https://www.esv.org/John+8:44" target="_blank">John 8:44</a>)', content)
    content = re.sub(
        r'\(Luke 4:5–7; John 12:31; 14:30; 16:11; 2 Cor\. 4:4; Eph\. 2:2\)',
        r'(<a href="https://www.esv.org/Luke+4:5-7" target="_blank">Luke 4:5–7</a>; <a href="https://www.esv.org/John+12:31" target="_blank">John 12:31</a>; <a href="https://www.esv.org/John+14:30" target="_blank">14:30</a>; <a href="https://www.esv.org/John+16:11" target="_blank">16:11</a>; <a href="https://www.esv.org/2+Corinthians+4:4" target="_blank">2 Cor. 4:4</a>; <a href="https://www.esv.org/Ephesians+2:2" target="_blank">Eph. 2:2</a>)',
        content
    )
    content = re.sub(
        r'\(Luke 8:12; 2 Cor\. 4:3–4; 2 Thess\. 2:7–10; 2 Pet\. 2; Rev\. 17\)',
        r'(<a href="https://www.esv.org/Luke+8:12" target="_blank">Luke 8:12</a>; <a href="https://www.esv.org/2+Corinthians+4:3-4" target="_blank">2 Cor. 4:3–4</a>; <a href="https://www.esv.org/2+Thessalonians+2:7-10" target="_blank">2 Thess. 2:7–10</a>; <a href="https://www.esv.org/2+Peter+2" target="_blank">2 Pet. 2</a>; <a href="https://www.esv.org/Revelation+17" target="_blank">Rev. 17</a>)',
        content
    )
    content = re.sub(
        r'\(Job 1:6–11; Zech\. 3:1–2; Rev\. 12:9–10\)',
        r'(<a href="https://www.esv.org/Job+1:6-11" target="_blank">Job 1:6–11</a>; <a href="https://www.esv.org/Zechariah+3:1-2" target="_blank">Zech. 3:1–2</a>; <a href="https://www.esv.org/Revelation+12:9-10" target="_blank">Rev. 12:9–10</a>)',
        content
    )
    content = re.sub(r'\(James 4:7–8\)', r'(<a href="https://www.esv.org/James+4:7-8" target="_blank">James 4:7–8</a>)', content)
    content = re.sub(r'\(1 Kings 19:10–14\)', r'(<a href="https://www.esv.org/1+Kings+19:10-14" target="_blank">1 Kings 19:10–14</a>)', content)
    content = re.sub(
        r'\(Acts 13:6–10; 2 Cor\. 11:13–15\)',
        r'(<a href="https://www.esv.org/Acts+13:6-10" target="_blank">Acts 13:6–10</a>; <a href="https://www.esv.org/2+Corinthians+11:13-15" target="_blank">2 Cor. 11:13–15</a>)',
        content
    )
    content = re.sub(
        r'\(Luke 4:3; 1 Cor\. 10:19–21\)',
        r'(<a href="https://www.esv.org/Luke+4:3" target="_blank">Luke 4:3</a>; <a href="https://www.esv.org/1+Corinthians+10:19-21" target="_blank">1 Cor. 10:19–21</a>)',
        content
    )
    content = re.sub(r'\(1 John 4:1\)', r'(<a href="https://www.esv.org/1+John+4:1" target="_blank">1 John 4:1</a>)', content)
    
    # Pattern 7: Prayer doctrine references
    content = re.sub(
        r'\(John 14:13–14; 16:23–24; Eph\. 5:20\)',
        r'(<a href="https://www.esv.org/John+14:13-14" target="_blank">John 14:13–14</a>; <a href="https://www.esv.org/John+16:23-24" target="_blank">16:23–24</a>; <a href="https://www.esv.org/Ephesians+5:20" target="_blank">Eph. 5:20</a>)',
        content
    )
    content = re.sub(r'\(1 John 1:9\)(?!</a>)', r'(<a href="https://www.esv.org/1+John+1:9" target="_blank">1 John 1:9</a>)', content)
    content = re.sub(r'\(John 15:7\)', r'(<a href="https://www.esv.org/John+15:7" target="_blank">John 15:7</a>)', content)
    content = re.sub(r'\(1 John 5:14\)', r'(<a href="https://www.esv.org/1+John+5:14" target="_blank">1 John 5:14</a>)', content)
    content = re.sub(r'\(James 4:2–4\)', r'(<a href="https://www.esv.org/James+4:2-4" target="_blank">James 4:2–4</a>)', content)
    content = re.sub(r'\(1 John 3:22\)', r'(<a href="https://www.esv.org/1+John+3:22" target="_blank">1 John 3:22</a>)', content)
    content = re.sub(r'\(Job 35:12–13\)', r'(<a href="https://www.esv.org/Job+35:12-13" target="_blank">Job 35:12–13</a>)', content)
    
    # Pattern 8: Royal Family references
    content = re.sub(
        r'\(Acts 1:5; Rom\. 6:3–4; Gal\. 3:26–28\)',
        r'(<a href="https://www.esv.org/Acts+1:5" target="_blank">Acts 1:5</a>; <a href="https://www.esv.org/Romans+6:3-4" target="_blank">Rom. 6:3–4</a>; <a href="https://www.esv.org/Galatians+3:26-28" target="_blank">Gal. 3:26–28</a>)',
        content
    )
    content = re.sub(r'\(John 7:37–39\)', r'(<a href="https://www.esv.org/John+7:37-39" target="_blank">John 7:37–39</a>)', content)
    
    # Pattern 9: Money doctrine
    content = re.sub(
        r'\(Jude 11; cf\. Num\. 22—24\)',
        r'(<a href="https://www.esv.org/Jude+1:11" target="_blank">Jude 11</a>; cf. <a href="https://www.esv.org/Numbers+22" target="_blank">Num. 22—24</a>)',
        content
    )
    
    return content

def main():
    """Fix unlinked references in both publish files."""
    print("Fixing unlinked scripture references...")
    
    files = [
        Path(__file__).parent / "Doctrines" / "doctrines_library_wp_publish.html",
        Path(__file__).parent / "Doctrines" / "doctrines_library_wp_clean.html"
    ]
    
    for filepath in files:
        if not filepath.exists():
            print(f"  ⚠ Skipping {filepath.name} - not found")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_count = len(re.findall(r'<a href="https://www.esv.org/', content))
        
        content = fix_unlinked_references(content)
        
        new_count = len(re.findall(r'<a href="https://www.esv.org/', content))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ {filepath.name}: {original_count} → {new_count} references (+{new_count - original_count})")
    
    print("\n✓ All files updated!")
    print("\nNext: Run generate_scripture_index.py and generate_analytics.py to update indexes")

if __name__ == "__main__":
    main()
