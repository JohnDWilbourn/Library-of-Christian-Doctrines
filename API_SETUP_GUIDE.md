# Bible API Setup Guide

## Overview
The doctrines library now supports live Bible verse previews using external APIs.

## Supported APIs

### 1. ESV API (English Standard Version) - RECOMMENDED
- **Website**: https://api.esv.org/
- **Cost**: Free (5,000 requests/day)
- **Quality**: Excellent, modern translation
- **Setup Time**: 5 minutes

#### Setup Steps:
1. Go to https://api.esv.org/
2. Click "Get API Key" or "Sign Up"
3. Create a free account
4. Generate an API key (available immediately)
5. Copy your API key

#### Configuration:
1. Open `Doctrines/doctrines_library_wp_clean.html`
2. Find the section with `API_CONFIG.esv.key`
3. Replace `'YOUR_ESV_API_KEY_HERE'` with your actual key
4. Change `enabled: false` to `enabled: true`
5. Save the file

Example:
```javascript
esv: {
    enabled: true,  // Changed from false
    key: 'abc123def456',  // Your actual API key
    baseUrl: 'https://api.esv.org/v3/passage/text/'
}
```

### 2. API.Bible (Alternative)
- **Website**: https://scripture.api.bible/
- **Cost**: Free (5,000 requests/day)
- **Versions**: Multiple (KJV, ASV, etc.)
- **Setup Time**: 5 minutes

#### Setup Steps:
1. Go to https://scripture.api.bible/
2. Sign up for a free account
3. Create an API key
4. Choose a Bible version (default: KJV)
5. Copy your API key and Bible ID

#### Configuration:
1. Open `Doctrines/doctrines_library_wp_clean.html`
2. Find `API_CONFIG.apiBible.key`
3. Replace `'YOUR_API_BIBLE_KEY_HERE'` with your key
4. Optionally change `bibleId` for different versions
5. Change `enabled: false` to `enabled: true`
6. Save the file

## Testing

After configuration:
1. Open the doctrines library in a browser
2. Open browser console (F12)
3. Look for "✓ Live Bible API integrated"
4. Hover over any scripture reference
5. You should see the actual verse text

## Troubleshooting

### "API key required" message appears
- Check that you set `enabled: true`
- Verify your API key is correct
- Check browser console for error messages

### Verses not loading
- Check internet connection
- Verify API key is active
- Check API rate limits (5,000/day)
- Look for errors in browser console

### CORS errors
- ESV and API.Bible both support CORS
- If using WordPress, ensure scripts are in HTML block
- May not work on local file:// protocol

## Best Practices

1. **Use Caching**: The system automatically caches API responses
2. **Monitor Usage**: Both APIs have 5,000 request/day limits
3. **Backup Plan**: Original tooltip system works without API
4. **Security**: API keys are client-side (acceptable for free tier)

## WordPress Integration

If using in WordPress Custom HTML block:
1. Configure API as described above
2. Copy entire HTML file content
3. Paste into Custom HTML block
4. API will work on frontend

Note: API keys will be visible in page source (this is normal for
free-tier APIs that allow client-side access).

## Cost Considerations

Both APIs are free with generous limits:
- **ESV**: 5,000 requests/day
- **API.Bible**: 5,000 requests/day

With caching, this easily supports hundreds of users per day.

## Alternative: No API

The system works without API keys:
- Shows placeholder message in tooltips
- Links still direct to ESV.org for full verses
- All other features work normally

## Support

- **ESV API**: https://api.esv.org/docs/
- **API.Bible**: https://scripture.api.bible/livedocs
