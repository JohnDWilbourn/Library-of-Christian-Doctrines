# Bible Doctrines Project - Change Log
## January 5, 2026

### Mobile Rendering Fixes
- ✅ Added viewport meta tag to doctrines_library_wp_publish.html for proper mobile rendering
- ✅ Fixed duplicate `<style>` tag in scripture_index_wp_publish.html
- ✅ Removed on-screen notification system that was showing error messages
- ✅ Fixed title visibility - added inline styles with dark mode support
- ✅ Hidden WordPress auto-generated page titles to prevent duplicates

### Scripture Index Improvements
- ✅ Fixed mobile table display issues (removed conflicting CSS)
- ✅ Updated all doctrine links from local paths to full WordPress URLs
- ✅ Added ESV API integration for verse excerpt population
- ✅ Created populate_scripture_index.py script for batch verse fetching
- ✅ Added API usage tracker widget (visible only to admin in browser)

### Navigation Updates
- ✅ Cross-page navigation working on all three pages (Library, Index, Analytics)
- ✅ Current page shows as non-clickable span
- ✅ Full URLs for all inter-page links

### Code Quality
- ✅ Commented out all console.log statements
- ✅ Removed unused showNotification function
- ✅ Added comprehensive .gitignore for security

### API Management
- ESV API Key: Configured and working (2ff0...5465)
- Usage: 182 total requests as of session end
- Limit: 5,000 requests/day
- Strategy: Pre-populate verses server-side to minimize viewer API calls

### Files Ready for WordPress Upload
1. doctrines_library_wp_publish.html - Main doctrine library with fixes
2. scripture_index_wp_publish.html - Scripture index with API integration
3. scripture_analytics_wp_publish.html - Analytics page (already good)

### Pending Work
- [ ] Run populate_scripture_index.py to permanently embed all verses
- [ ] Upload updated HTML files to WordPress after verse population
- [ ] Consider PWA icon integration (3 sets available: old-church-1, bible-1, cross-1)
- [ ] Fix WordPress theme errors (5Gwdossier.css, barrier_cleared.png)

### Virtual Environment
- Created: ~/bible_venv
- Installed: requests library
- Location: Home directory (VAULT drive doesn't support symlinks)

### Security Notes
- API key excluded from git via .gitignore
- populate_scripture_index.py excluded (contains API key)
- Error screenshots and temp files excluded
- WordPress credentials in project-notes.txt excluded
