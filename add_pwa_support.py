#!/usr/bin/env python3
"""
Add Progressive Web App (PWA) Capabilities
Makes the doctrines library installable as a mobile/desktop app.
"""

import json

def create_manifest():
    """Create PWA manifest file."""
    
    manifest = {
        "name": "Complete Library of Christian Doctrines",
        "short_name": "Doctrines",
        "description": "Comprehensive Christian doctrines with scripture references",
        "start_url": "/complete-library-of-christian-doctrine/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#3b82f6",
        "orientation": "any",
        "icons": [
            {
                "src": "/wp-content/uploads/doctrine-icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "/wp-content/uploads/doctrine-icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["education", "reference", "books"],
        "screenshots": [
            {
                "src": "/wp-content/uploads/doctrine-screenshot.png",
                "sizes": "540x720",
                "type": "image/png"
            }
        ]
    }
    
    with open('manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print("✓ Created manifest.json")

def create_service_worker():
    """Create service worker for offline functionality."""
    
    service_worker = """// Service Worker for Christian Doctrines Library PWA
const CACHE_NAME = 'doctrines-v1';
const urlsToCache = [
  '/complete-library-of-christian-doctrine/',
  '/comprehensive-biblical-reference-guide/',
  // Add other resources as needed
];

// Install service worker and cache resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch from cache or network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(response => {
          // Check if valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        });
      })
  );
});

// Update service worker
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
"""
    
    with open('service-worker.js', 'w', encoding='utf-8') as f:
        f.write(service_worker)
    
    print("✓ Created service-worker.js")

def add_pwa_support():
    """Generate HTML to add PWA support."""
    
    return """
<!-- PWA Support -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#3b82f6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Doctrines">

<script>
// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('✓ Service Worker registered:', registration.scope);
      })
      .catch(error => {
        console.log('Service Worker registration failed:', error);
      });
  });
}

// PWA Install Prompt
let deferredPrompt;
let installButton;

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the mini-infobar from appearing
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  
  // Show custom install button
  if (!installButton) {
    createInstallButton();
  }
});

function createInstallButton() {
  installButton = document.createElement('button');
  installButton.id = 'pwaInstallBtn';
  installButton.innerHTML = `
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" style="margin-right: 0.5em;">
      <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
    </svg>
    Install App
  `;
  installButton.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    color: white;
    border: none;
    padding: 0.75em 1.25em;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    transition: all 0.3s ease;
    z-index: 10000;
    display: flex;
    align-items: center;
    animation: slideIn 0.5s ease;
  `;
  
  installButton.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    
    // Show the install prompt
    deferredPrompt.prompt();
    
    // Wait for the user's response
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`PWA install outcome: ${outcome}`);
    
    // Clear the deferred prompt
    deferredPrompt = null;
    
    // Remove the install button
    installButton.remove();
    installButton = null;
  });
  
  installButton.addEventListener('mouseenter', () => {
    installButton.style.transform = 'translateY(-2px)';
    installButton.style.boxShadow = '0 6px 16px rgba(139, 92, 246, 0.5)';
  });
  
  installButton.addEventListener('mouseleave', () => {
    installButton.style.transform = 'translateY(0)';
    installButton.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.4)';
  });
  
  // Add animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideIn {
      from {
        transform: translateX(100px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  `;
  document.head.appendChild(style);
  
  document.body.appendChild(installButton);
}

// Handle successful installation
window.addEventListener('appinstalled', () => {
  console.log('✓ PWA installed successfully');
  deferredPrompt = null;
  if (installButton) {
    installButton.remove();
    installButton = null;
  }
});

// Offline/Online detection
window.addEventListener('online', () => {
  console.log('✓ Back online');
  showNotification('Back online!', 'success');
});

window.addEventListener('offline', () => {
  console.log('⚠ Offline mode');
  showNotification('Offline - using cached content', 'warning');
});

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: ${type === 'success' ? '#10b981' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
    color: white;
    padding: 1em 2em;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    z-index: 10001;
    animation: slideDown 0.3s ease;
  `;
  
  const animStyle = document.createElement('style');
  animStyle.textContent = `
    @keyframes slideDown {
      from { transform: translate(-50%, -100px); opacity: 0; }
      to { transform: translate(-50%, 0); opacity: 1; }
    }
  `;
  document.head.appendChild(animStyle);
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.animation = 'slideDown 0.3s ease reverse';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

console.log('✓ PWA support enabled');
console.log('  - Can be installed as app');
console.log('  - Offline caching available');
console.log('  - Works on mobile and desktop');
</script>
"""

def add_pwa_to_file(html_file, output_file):
    """Add PWA support to HTML file."""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already exists
    if 'serviceWorker' in content:
        print(f"ℹ PWA support already exists in {html_file}")
        return
    
    # Insert after opening div or at beginning
    wrapper_match = content.find('<div class=')
    if wrapper_match != -1:
        before = content[:wrapper_match]
        after = content[wrapper_match:]
        result = before + add_pwa_support() + '\n' + after
    else:
        result = add_pwa_support() + '\n' + content
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✓ Added PWA support to {output_file}")

def create_pwa_guide():
    """Create guide for PWA deployment."""
    
    guide = """# Progressive Web App (PWA) Deployment Guide

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
"""
    
    with open('PWA_DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✓ Created PWA_DEPLOYMENT_GUIDE.md")

def main():
    """Main execution."""
    print("Adding Progressive Web App (PWA) capabilities...\n")
    
    # Create manifest
    create_manifest()
    
    # Create service worker
    create_service_worker()
    
    # Add PWA support to HTML files
    add_pwa_to_file(
        'Doctrines/doctrines_library_wp_clean.html',
        'Doctrines/doctrines_library_wp_clean.html'
    )
    
    add_pwa_to_file(
        'Doctrines/scripture_index_wp_clean.html',
        'Doctrines/scripture_index_wp_clean.html'
    )
    
    # Create deployment guide
    create_pwa_guide()
    
    print("\n✓ PWA capabilities added!")
    print("  - manifest.json created")
    print("  - service-worker.js created")
    print("  - Install prompt enabled")
    print("  - Offline caching configured")
    print("  - Works on mobile and desktop")
    print("\n📱 See PWA_DEPLOYMENT_GUIDE.md for deployment instructions")
    print("   Note: Requires HTTPS and app icons (192x192, 512x512)")

if __name__ == '__main__':
    main()
