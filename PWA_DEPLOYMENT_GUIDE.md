# Progressive Web App (PWA) Deployment Guide

## Overview
The doctrines library is now a Progressive Web App (PWA) that can be installed on mobile and desktop devices for an app-like experience.

## Features

### ✅ Installable
- Add to home screen on mobile
- Install as desktop app
- Runs in standalone mode (no browser UI)

### ✅ Offline Support
- Service worker caches content
- Works without internet connection
- Automatic cache updates

### ✅ Native Feel
- Full-screen experience
- App icon on device
- Splash screen on launch
- Status bar theming

## Deployment Steps

### 1. Upload Files to WordPress

Upload these files to your WordPress site:
- `manifest.json` → Root or wp-content/uploads/
- `service-worker.js` → Root directory
- Create app icons (192x192 and 512x512)

### 2. Create App Icons

You need two icon sizes:
- **192x192 pixels** - For home screen
- **512x512 pixels** - For splash screen

Icon suggestions:
- Use a Bible or cross symbol
- Simple, recognizable design
- High contrast for visibility
- Save as PNG with transparency

Tools for creating icons:
- Canva.com (free templates)
- Figma (professional design)
- IconKitchen.com (app icon generator)

### 3. Update Manifest Paths

Edit `manifest.json` to match your WordPress structure:
```json
{
  "start_url": "/your-doctrine-page-url/",
  "icons": [
    {
      "src": "/wp-content/uploads/doctrine-icon-192.png",
      ...
    }
  ]
}
```

### 4. WordPress Configuration

#### Option A: Custom HTML Block (Current Method)
The PWA code is already embedded in the HTML files. No additional configuration needed.

#### Option B: Theme Integration
For better control, add to your theme:

1. Add to `header.php`:
```php
<link rel="manifest" href="<?php echo get_template_directory_uri(); ?>/manifest.json">
<meta name="theme-color" content="#3b82f6">
```

2. Add service worker registration:
```php
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js');
}
</script>
```

### 5. HTTPS Requirement

⚠️ **CRITICAL**: PWAs require HTTPS!

- Ensure your site uses HTTPS (WordPress.com includes this)
- Get free SSL with Let's Encrypt
- PWAs won't work on HTTP (except localhost)

### 6. Testing

#### Desktop (Chrome/Edge):
1. Visit your doctrines page
2. Look for install icon in address bar (⊕)
3. Click "Install" or use menu → "Install app"

#### Mobile (Android):
1. Visit page in Chrome
2. Tap menu (⋮)
3. Select "Add to Home screen" or "Install app"
4. Confirm installation

#### Mobile (iOS/Safari):
1. Visit page in Safari
2. Tap share icon (□↑)
3. Select "Add to Home Screen"
4. Name the app and confirm

### 7. Verify Installation

After deployment:
1. Open Chrome DevTools (F12)
2. Go to "Application" tab
3. Check "Manifest" section
4. Verify "Service Workers" are active
5. Test "Add to home screen"

## Troubleshooting

### Install Button Not Showing
- Verify HTTPS is active
- Check manifest.json loads (no 404)
- Clear browser cache
- Check console for errors

### Icons Not Loading
- Verify icon paths in manifest.json
- Check icons are correct sizes
- Use PNG format
- Test icon URLs directly

### Offline Mode Not Working
- Check service-worker.js is at root
- Verify no console errors
- Service worker needs time to cache
- May need to revisit page twice

### iOS Specific Issues
- Safari has limited PWA support
- No install prompt (manual add)
- Service worker may be restricted
- Test on actual device, not simulator

## Customization

### Change App Name
Edit `manifest.json`:
```json
{
  "name": "Your Custom Name",
  "short_name": "Custom"
}
```

### Change Theme Color
Edit `manifest.json` and meta tag:
```json
"theme_color": "#your-color"
```

### Add More Cached Pages
Edit `service-worker.js`:
```javascript
const urlsToCache = [
  '/your-page-1/',
  '/your-page-2/',
  '/images/your-image.jpg'
];
```

## Maintenance

### Updating Content
When you update doctrines:
1. Update cache version in `service-worker.js`:
```javascript
const CACHE_NAME = 'doctrines-v2'; // Increment version
```
2. This forces users to get fresh content

### Monitoring Usage
- Use Google Analytics to track PWA installs
- Monitor service worker errors in console
- Check PWA scores with Lighthouse

## Best Practices

1. **Keep It Light**: PWAs should load fast
2. **Test Offline**: Verify offline functionality works
3. **Update Regularly**: Keep service worker cache fresh
4. **Mobile First**: Design for small screens
5. **Monitor Performance**: Use Lighthouse audits

## Benefits for Users

- ⚡ Faster load times
- 📱 Works offline
- 🏠 Add to home screen
- 🔔 Optional push notifications (future)
- 💾 Less data usage
- 🚀 App-like experience

## Future Enhancements

- Push notifications for new doctrines
- Background sync for bookmarks
- Share target (share verses to app)
- Media caching for images
- Multiple language support

## Resources

- PWA Documentation: https://web.dev/progressive-web-apps/
- Manifest Generator: https://app-manifest.firebaseapp.com/
- Icon Generator: https://realfavicongenerator.net/
- Lighthouse Testing: Built into Chrome DevTools
- PWA Builder: https://www.pwabuilder.com/

## Support

If users have issues installing:
1. Verify they're on HTTPS
2. Check browser compatibility
3. Clear browser cache
4. Try incognito/private mode
5. Check console for errors
