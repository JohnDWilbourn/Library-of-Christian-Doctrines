# WordPress Deployment Guide - Version 3.0

## 🚀 Quick Start - Deploy to WordPress

This guide will help you deploy the Bible Doctrines Library (Version 3.0 - Professional Edition) to your WordPress site.

---

## 📦 Files Overview

### WordPress Content Files (Ready to Copy/Paste):
- **doctrines_library_wp_publish.html** (596 KB) - Main doctrines library with all features
- **scripture_index_wp_publish.html** (279 KB) - Scripture reference index
- **scripture_analytics_wp_publish.html** (24 KB) - Analytics dashboard

### PWA Support Files (Upload to Site Root):
- **manifest.json** - PWA manifest for app installation
- **service-worker.js** - Offline caching and updates

### Development Files (Keep for Future Updates):
- **doctrines_library_wp_clean.html** - Development version of main library
- **scripture_index_wp_clean.html** - Development version of index
- **scripture_analytics_wp.html** - Development version of analytics

---

## 📋 Step-by-Step Deployment

### Step 1: Update WordPress Pages (Main Content)

#### For Main Doctrines Library Page:
1. Open [Doctrines/doctrines_library_wp_publish.html](Doctrines/doctrines_library_wp_publish.html)
2. Select ALL content (Ctrl+A / Cmd+A)
3. Copy (Ctrl+C / Cmd+C)
4. Go to: `intelligencereport.info/bible-doctrines`
5. Edit page in WordPress
6. **Replace existing Custom HTML block** or **Add new Custom HTML block**
7. Paste the content
8. Click "Update" or "Publish"

#### For Scripture Index Page:
1. Open [Doctrines/scripture_index_wp_publish.html](Doctrines/scripture_index_wp_publish.html)
2. Copy all content
3. Go to: `intelligencereport.info/bible-doctrines-scripture-index`
4. Edit page, paste into Custom HTML block
5. Publish

#### For Analytics Dashboard:
1. Open [Doctrines/scripture_analytics_wp_publish.html](Doctrines/scripture_analytics_wp_publish.html)
2. Copy all content
3. Go to: `intelligencereport.info/bible-doctrines-analytics`
4. Edit page, paste into Custom HTML block
5. Publish

### Step 2: Upload PWA Files (Optional but Recommended)

#### Upload to Site Root via FTP/File Manager:
1. Connect to your site via FTP or cPanel File Manager
2. Navigate to your site's root directory (usually `public_html` or `www`)
3. Upload these files:
   - `manifest.json`
   - `service-worker.js`

**Note:** These files must be in the root directory for PWA to work!

#### Verify Upload:
- Visit: `https://intelligencereport.info/manifest.json` (should show JSON)
- Visit: `https://intelligencereport.info/service-worker.js` (should show JavaScript)

### Step 3: Create App Icons (For PWA)

#### Icon Requirements:
- **192x192 pixels** - `icon-192.png`
- **512x512 pixels** - `icon-512.png`
- Format: PNG with transparency
- Style: Simple, recognizable icon (Bible, cross, book, etc.)

#### Icon Creation Tools:
- **Online:** https://realfavicongenerator.net/
- **Canva:** https://www.canva.com/ (free)
- **GIMP:** Free image editor
- **Adobe Express:** https://www.adobe.com/express/

#### Upload Icons:
1. Create/save icons as `icon-192.png` and `icon-512.png`
2. Upload to site root (same location as manifest.json)
3. Verify at:
   - `https://intelligencereport.info/icon-192.png`
   - `https://intelligencereport.info/icon-512.png`

### Step 4: Configure Bible API (Optional but Recommended)

#### Get ESV API Key (Free):
1. Visit: https://api.esv.org/
2. Click "Get API Key"
3. Sign up (free account)
4. Copy your API key

#### Add API Key to WordPress:
1. Edit the main doctrines page in WordPress
2. Find this section in the Custom HTML block:
   ```javascript
   const API_CONFIG = {
       enabled: false,  // Change to true
       apiKey: '',      // Paste your API key here
   ```
3. Change to:
   ```javascript
   const API_CONFIG = {
       enabled: true,
       apiKey: 'YOUR_ESV_API_KEY_HERE',
   ```
4. Update/Publish

**Result:** Verse tooltips will now show actual Bible text!

**Without API Key:** Tooltips show "Hover over verses to see preview (API key required)"

---

## ✅ Verification Checklist

After deployment, verify these features work:

### On Desktop:
- [ ] Page loads correctly
- [ ] Search box filters doctrines in real-time
- [ ] Category buttons filter by theological category
- [ ] Tag pills are visible and clickable
- [ ] Verse references are clickable links
- [ ] Hovering over verses shows tooltip (with or without API)
- [ ] Cross-reference button appears (bottom-right)
- [ ] PDF export button appears (bottom-right)
- [ ] Install app button appears (top-right, if PWA configured)

### On Mobile:
- [ ] Page is responsive and readable
- [ ] Search works on mobile
- [ ] Category buttons work
- [ ] Cross-reference panel slides in
- [ ] Export menu works
- [ ] PWA install prompt appears (if configured)
- [ ] Can add to home screen

### PWA Features (if configured):
- [ ] Install prompt appears in browser
- [ ] App installs to home screen/desktop
- [ ] App launches in standalone mode
- [ ] App works offline (visit once, then disable wifi)
- [ ] Service worker registers (check browser console)

---

## 🎯 Feature Overview

### Included Features (All Automatic):

#### 1. Search & Filter
- Real-time search across all doctrines
- Filter by theological category (11 categories)
- Filter by keyword tags (18 tags)
- Combined filtering (search + category + tag)

#### 2. Verse Preview
- Hover over any scripture reference
- Shows verse text in tooltip
- Live API integration (ESV + API.Bible)
- Caching to reduce API calls

#### 3. Cross-References
- Click any verse to see related verses
- Shows connection strength
- Lists doctrines containing each verse
- 937 relationship sets from 1,022 verses

#### 4. PDF Export
- **Print/Save as PDF** - Browser native
- **Download PDF** - Client-side jsPDF
- **Export Current View** - Print filtered results
- **Download as Text** - Plain text export

#### 5. Doctrine Hierarchy
- 11 theological categories
- Color-coded navigation
- Category headers throughout
- One-click filtering

#### 6. Mobile App (PWA)
- Installable on any device
- Works offline
- App icon on home screen
- Push notifications ready
- Automatic updates

#### 7. Keyword Tagging
- 18 theological topic tags
- Click to filter by tag
- Multi-tag support
- Visual tag pills

#### 8. Analytics Dashboard
- Most-cited books
- Most-referenced verses
- Scripture usage statistics
- 1,490+ references tracked

---

## 🔧 Troubleshooting

### Issue: PWA Not Appearing

**Cause:** Missing files or incorrect location

**Solutions:**
1. Verify manifest.json is in site root
2. Check service-worker.js is in site root
3. Ensure HTTPS is enabled (required for PWA)
4. Clear browser cache and reload
5. Check browser console for errors

### Issue: Verse Tooltips Don't Show Text

**Cause:** API key not configured or invalid

**Solutions:**
1. Get free API key from https://api.esv.org/
2. Add to API_CONFIG in HTML
3. Set enabled: true
4. Verify API key is valid
5. Check browser console for API errors

**Note:** Tooltips still appear without API, just show placeholder text

### Issue: Cross-References Not Working

**Cause:** JavaScript not loading

**Solutions:**
1. Check browser console for errors
2. Verify Custom HTML block includes all content
3. Clear WordPress cache (if using cache plugin)
4. Try different browser
5. Disable browser ad-blockers

### Issue: Export Button Not Visible

**Cause:** CSS conflict or JavaScript not loading

**Solutions:**
1. Check browser console for errors
2. Verify jsPDF loaded from CDN
3. Clear browser cache
4. Check for WordPress theme conflicts
5. Try incognito/private browsing mode

### Issue: Categories Not Filtering

**Cause:** JavaScript error or content mismatch

**Solutions:**
1. Check browser console for errors
2. Verify all doctrines have data-category attribute
3. Clear browser cache
4. Reload page
5. Check if search box has value (clear it)

---

## 📱 Mobile App Installation

### Android (Chrome):
1. Visit the page on Chrome
2. Look for "Install" icon in address bar
3. Or: Menu → "Install app" or "Add to Home screen"
4. Confirm installation
5. App appears on home screen

### iOS (Safari):
1. Visit the page on Safari
2. Tap Share button (square with arrow)
3. Scroll down, tap "Add to Home Screen"
4. Enter name, tap "Add"
5. App icon appears on home screen

### Desktop (Chrome/Edge):
1. Visit the page
2. Look for install icon in address bar (⊕)
3. Click to install
4. App appears in Start Menu/Applications
5. Launch like any other app

---

## 🔐 Security & Performance

### HTTPS Required:
- PWA features require HTTPS
- Service workers require secure context
- Most modern hosting provides free SSL

### Performance Optimization:
- **Caching:** Service worker caches pages for offline use
- **CDN:** jsPDF and html2canvas loaded from CDN
- **Lazy Loading:** Features load as needed
- **Debouncing:** Search optimized to reduce lag
- **API Caching:** Bible verses cached to reduce API calls

### Privacy:
- No user data collected by the app
- Google Analytics configured (if enabled)
- API calls to ESV.org (if API configured)
- All processing client-side

---

## 📊 File Size Information

| File | Size | Purpose |
|------|------|---------|
| doctrines_library_wp_publish.html | 596 KB | Main content with all features |
| scripture_index_wp_publish.html | 279 KB | Reverse scripture index |
| scripture_analytics_wp_publish.html | 24 KB | Analytics dashboard |
| manifest.json | 1 KB | PWA configuration |
| service-worker.js | 3 KB | Offline caching |
| icon-192.png | ~10 KB | Small app icon |
| icon-512.png | ~30 KB | Large app icon |
| **Total** | **~943 KB** | Complete deployment |

**Note:** Files are optimized but rich with features. Consider enabling gzip compression on your server for faster loading.

---

## 🎓 Additional Resources

### Documentation:
- [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) - Detailed API configuration
- [PWA_DEPLOYMENT_GUIDE.md](PWA_DEPLOYMENT_GUIDE.md) - Advanced PWA setup
- [VERSION_3.0_SUMMARY.md](VERSION_3.0_SUMMARY.md) - Complete feature list
- [ENHANCEMENTS.md](ENHANCEMENTS.md) - Version 2.0 features
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) - Project overview

### External Resources:
- ESV API: https://api.esv.org/
- API.Bible: https://scripture.api.bible/
- PWA Guide: https://web.dev/progressive-web-apps/
- Manifest Generator: https://app-manifest.firebaseapp.com/
- jsPDF: https://github.com/parallax/jsPDF

### Support:
- Repository: https://github.com/JohnDWilbourn/Library-of-Christian-Doctrines
- Issues: https://github.com/JohnDWilbourn/Library-of-Christian-Doctrines/issues

---

## 🎉 You're Ready to Publish!

### Quick Recap:
1. ✅ Copy/paste 3 HTML files to WordPress pages
2. ✅ Upload manifest.json and service-worker.js to site root
3. ✅ Create and upload app icons (192x192, 512x512)
4. ✅ Configure ESV API key (optional)
5. ✅ Test on desktop and mobile
6. ✅ Install as app and test offline

**Version:** 3.0 - Professional Edition  
**Status:** Production Ready  
**License:** MIT (Open Source)

**All features included and ready to use!**

Enjoy your professional-grade Bible Doctrines Library! 📖✨
