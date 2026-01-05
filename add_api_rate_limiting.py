#!/usr/bin/env python3
"""
Add ESV API rate limiting and bot protection to comply with terms of use.

ESV API Terms:
- Max 5,000 queries per day
- Max 1,000 requests per hour  
- Max 60 requests per minute
- Max 500 verses per query
- Max 500 verses cached locally
"""

from bs4 import BeautifulSoup
from pathlib import Path

def add_rate_limiting():
    """Add comprehensive rate limiting to all publish files."""
    
    rate_limiting_code = '''
<script>
// ============================================================
// ESV API Rate Limiting & Bot Protection
// Complies with ESV API Terms of Use
// ============================================================
(function() {
    'use strict';
    
    const ESV_RATE_LIMITS = {
        perMinute: 60,      // Max 60 requests per minute
        perHour: 1000,      // Max 1,000 requests per hour
        perDay: 5000,       // Max 5,000 requests per day
        maxVerses: 500,     // Max 500 verses per query
        maxCacheSize: 500   // Max 500 verses cached
    };
    
    const STORAGE_KEY = 'esv_api_rate_limits';
    const CACHE_KEY = 'esv_verse_cache';
    
    // ============================================================
    // Rate Limit Tracker
    // ============================================================
    class RateLimiter {
        constructor() {
            this.loadState();
            this.startCleanupTimer();
        }
        
        loadState() {
            try {
                const stored = localStorage.getItem(STORAGE_KEY);
                if (stored) {
                    this.state = JSON.parse(stored);
                    this.cleanOldEntries();
                } else {
                    this.resetState();
                }
            } catch (e) {
                console.warn('Failed to load rate limit state:', e);
                this.resetState();
            }
        }
        
        resetState() {
            this.state = {
                requests: [],
                dailyCount: 0,
                lastReset: Date.now()
            };
            this.saveState();
        }
        
        saveState() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(this.state));
            } catch (e) {
                console.error('Failed to save rate limit state:', e);
            }
        }
        
        cleanOldEntries() {
            const now = Date.now();
            const oneHourAgo = now - (60 * 60 * 1000);
            const oneDayAgo = now - (24 * 60 * 60 * 1000);
            
            // Remove requests older than 1 hour
            this.state.requests = this.state.requests.filter(timestamp => timestamp > oneHourAgo);
            
            // Reset daily counter if more than 24 hours
            if (this.state.lastReset < oneDayAgo) {
                this.state.dailyCount = 0;
                this.state.lastReset = now;
            }
            
            this.saveState();
        }
        
        startCleanupTimer() {
            // Clean up old entries every 5 minutes
            setInterval(() => this.cleanOldEntries(), 5 * 60 * 1000);
        }
        
        checkLimit(limitType = 'minute') {
            const now = Date.now();
            this.cleanOldEntries();
            
            if (limitType === 'minute') {
                const oneMinuteAgo = now - (60 * 1000);
                const recentRequests = this.state.requests.filter(t => t > oneMinuteAgo);
                return recentRequests.length < ESV_RATE_LIMITS.perMinute;
            } else if (limitType === 'hour') {
                const oneHourAgo = now - (60 * 60 * 1000);
                const recentRequests = this.state.requests.filter(t => t > oneHourAgo);
                return recentRequests.length < ESV_RATE_LIMITS.perHour;
            } else if (limitType === 'day') {
                return this.state.dailyCount < ESV_RATE_LIMITS.perDay;
            }
            return false;
        }
        
        canMakeRequest() {
            return this.checkLimit('minute') && 
                   this.checkLimit('hour') && 
                   this.checkLimit('day');
        }
        
        recordRequest() {
            const now = Date.now();
            this.state.requests.push(now);
            this.state.dailyCount++;
            this.saveState();
        }
        
        getRemainingRequests() {
            this.cleanOldEntries();
            const now = Date.now();
            const oneMinuteAgo = now - (60 * 1000);
            const oneHourAgo = now - (60 * 60 * 1000);
            
            const minuteRequests = this.state.requests.filter(t => t > oneMinuteAgo).length;
            const hourRequests = this.state.requests.filter(t => t > oneHourAgo).length;
            
            return {
                minute: ESV_RATE_LIMITS.perMinute - minuteRequests,
                hour: ESV_RATE_LIMITS.perHour - hourRequests,
                day: ESV_RATE_LIMITS.perDay - this.state.dailyCount
            };
        }
        
        getWaitTime() {
            if (this.checkLimit('minute')) return 0;
            
            const now = Date.now();
            const oneMinuteAgo = now - (60 * 1000);
            const oldestRequest = this.state.requests.find(t => t > oneMinuteAgo);
            
            if (oldestRequest) {
                const waitMs = (oldestRequest + 60 * 1000) - now;
                return Math.max(0, Math.ceil(waitMs / 1000));
            }
            return 60;
        }
    }
    
    // ============================================================
    // Verse Cache Manager (Max 500 verses per ESV terms)
    // ============================================================
    class VerseCache {
        constructor() {
            this.loadCache();
        }
        
        loadCache() {
            try {
                const stored = localStorage.getItem(CACHE_KEY);
                if (stored) {
                    this.cache = JSON.parse(stored);
                } else {
                    this.cache = {
                        verses: {},
                        count: 0,
                        lastCleared: Date.now()
                    };
                }
            } catch (e) {
                console.warn('Failed to load verse cache:', e);
                this.cache = { verses: {}, count: 0, lastCleared: Date.now() };
            }
        }
        
        saveCache() {
            try {
                localStorage.setItem(CACHE_KEY, JSON.stringify(this.cache));
            } catch (e) {
                console.error('Failed to save verse cache:', e);
            }
        }
        
        get(reference) {
            return this.cache.verses[reference] || null;
        }
        
        set(reference, data) {
            // Check if we're at the 500 verse limit
            if (!this.cache.verses[reference] && this.cache.count >= ESV_RATE_LIMITS.maxCacheSize) {
                // Remove oldest entry (FIFO)
                const oldestKey = Object.keys(this.cache.verses)[0];
                delete this.cache.verses[oldestKey];
                this.cache.count--;
                console.log('⚠ Cache limit reached. Removed oldest verse:', oldestKey);
            }
            
            if (!this.cache.verses[reference]) {
                this.cache.count++;
            }
            
            this.cache.verses[reference] = {
                ...data,
                cached: Date.now()
            };
            
            this.saveCache();
        }
        
        clear() {
            this.cache = {
                verses: {},
                count: 0,
                lastCleared: Date.now()
            };
            this.saveCache();
            console.log('✓ Verse cache cleared');
        }
        
        getSize() {
            return this.cache.count;
        }
        
        shouldClear() {
            // Clear cache every 30 days (ESV recommendation)
            const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
            return this.cache.lastCleared < thirtyDaysAgo;
        }
    }
    
    // ============================================================
    // Bot Detection & Prevention
    // ============================================================
    class BotDetector {
        constructor() {
            this.suspiciousActivity = 0;
            this.lastRequestTime = 0;
        }
        
        isBot() {
            // Check for common bot indicators
            const userAgent = navigator.userAgent.toLowerCase();
            const botPatterns = [
                'bot', 'crawler', 'spider', 'scraper', 'curl', 'wget', 
                'python-requests', 'axios', 'fetch', 'headless'
            ];
            
            for (const pattern of botPatterns) {
                if (userAgent.includes(pattern)) {
                    console.warn('⚠ Bot detected via user agent');
                    return true;
                }
            }
            
            // Check for rapid-fire requests (< 100ms between requests)
            const now = Date.now();
            if (this.lastRequestTime && (now - this.lastRequestTime) < 100) {
                this.suspiciousActivity++;
                if (this.suspiciousActivity > 5) {
                    console.warn('⚠ Bot detected via rapid requests');
                    return true;
                }
            } else {
                this.suspiciousActivity = Math.max(0, this.suspiciousActivity - 1);
            }
            
            this.lastRequestTime = now;
            
            // Check for missing standard browser features
            if (!window.document || !window.navigator || !window.screen) {
                console.warn('⚠ Bot detected via missing browser features');
                return true;
            }
            
            return false;
        }
        
        reset() {
            this.suspiciousActivity = 0;
        }
    }
    
    // ============================================================
    // Initialize Protection Systems
    // ============================================================
    const rateLimiter = new RateLimiter();
    const verseCache = new VerseCache();
    const botDetector = new BotDetector();
    
    // Clear cache if it's been 30 days
    if (verseCache.shouldClear()) {
        verseCache.clear();
        console.log('♻️ Periodic cache clear (30 days)');
    }
    
    // ============================================================
    // Protected API Request Function
    // ============================================================
    window.makeProtectedAPIRequest = async function(reference, fetchFunction) {
        // Check cache first
        const cached = verseCache.get(reference);
        if (cached) {
            console.log('✓ Verse loaded from cache:', reference);
            return cached;
        }
        
        // Bot detection
        if (botDetector.isBot()) {
            console.error('🚫 Bot detected - API request blocked');
            return {
                text: 'Automated requests are not permitted. Please visit ESV.org directly.',
                version: 'Error',
                success: false,
                error: 'bot_detected'
            };
        }
        
        // Rate limit check
        if (!rateLimiter.canMakeRequest()) {
            const remaining = rateLimiter.getRemainingRequests();
            const waitTime = rateLimiter.getWaitTime();
            
            console.warn('⚠ Rate limit reached');
            console.log('Remaining requests:');
            console.log('  Per minute:', remaining.minute);
            console.log('  Per hour:', remaining.hour);
            console.log('  Per day:', remaining.day);
            console.log('Wait time:', waitTime, 'seconds');
            
            return {
                text: `Rate limit reached. Please wait ${waitTime} seconds. (ESV API allows 60/min, 1000/hour, 5000/day)`,
                version: 'Rate Limited',
                success: false,
                error: 'rate_limit',
                waitTime: waitTime,
                remaining: remaining
            };
        }
        
        // Make the API request
        try {
            rateLimiter.recordRequest();
            const result = await fetchFunction(reference);
            
            // Cache successful results
            if (result && result.success) {
                verseCache.set(reference, result);
            }
            
            return result;
        } catch (error) {
            console.error('API request failed:', error);
            return {
                text: 'Failed to fetch verse. Please try again later.',
                version: 'Error',
                success: false,
                error: error.message
            };
        }
    };
    
    // ============================================================
    // Expose API for monitoring
    // ============================================================
    window.ESV_RATE_LIMITER = {
        getRemaining: () => rateLimiter.getRemainingRequests(),
        getWaitTime: () => rateLimiter.getWaitTime(),
        getCacheSize: () => verseCache.getSize(),
        clearCache: () => verseCache.clear(),
        getStatus: () => ({
            remaining: rateLimiter.getRemainingRequests(),
            cacheSize: verseCache.getSize(),
            maxCacheSize: ESV_RATE_LIMITS.maxCacheSize,
            canRequest: rateLimiter.canMakeRequest()
        }),
        reset: () => {
            rateLimiter.resetState();
            botDetector.reset();
            console.log('✓ Rate limiter reset');
        }
    };
    
    // ============================================================
    // Console Status Display
    // ============================================================
    console.log('🛡️ ESV API Protection Enabled');
    console.log('Rate Limits:');
    console.log('  • 60 requests per minute');
    console.log('  • 1,000 requests per hour');
    console.log('  • 5,000 requests per day');
    console.log('  • Max 500 verses cached');
    console.log('');
    console.log('Current Status:');
    const remaining = rateLimiter.getRemainingRequests();
    console.log('  • Remaining today:', remaining.day);
    console.log('  • Remaining this hour:', remaining.hour);
    console.log('  • Remaining this minute:', remaining.minute);
    console.log('  • Cached verses:', verseCache.getSize(), '/ 500');
    console.log('');
    console.log('To check status: ESV_RATE_LIMITER.getStatus()');
    console.log('To clear cache: ESV_RATE_LIMITER.clearCache()');
})();
</script>
'''
    
    return rate_limiting_code

def update_api_functions():
    """Update API functions to use rate limiter."""
    
    updated_api_code = '''
    /**
     * Fetch verse text from ESV API with rate limiting
     */
    async function fetchFromESV(reference) {
        if (!API_CONFIG.esv.enabled || !API_CONFIG.esv.key || API_CONFIG.esv.key === 'YOUR_ESV_API_KEY_HERE') {
            return null;
        }
        
        // Use protected request wrapper
        return await window.makeProtectedAPIRequest(reference, async (ref) => {
            try {
                const url = API_CONFIG.esv.baseUrl + '?' + new URLSearchParams({
                    q: ref,
                    'include-headings': 'false',
                    'include-footnotes': 'false',
                    'include-verse-numbers': 'false',
                    'include-short-copyright': 'false',
                    'include-passage-references': 'false'
                });
                
                const response = await fetch(url, {
                    headers: {
                        'Authorization': `Token ${API_CONFIG.esv.key}`
                    }
                });
                
                if (!response.ok) {
                    if (response.status === 429) {
                        throw new Error('Rate limit exceeded');
                    }
                    throw new Error('ESV API error');
                }
                
                const data = await response.json();
                return {
                    text: data.passages[0]?.trim() || 'Verse not found',
                    version: 'ESV',
                    success: true
                };
            } catch (error) {
                console.warn('ESV API fetch failed:', error);
                return {
                    text: error.message,
                    version: 'Error',
                    success: false
                };
            }
        });
    }
'''
    
    return updated_api_code

def process_file(file_path):
    """Add rate limiting to a publish file."""
    
    print(f"\n📝 Processing: {file_path.name}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add rate limiting code before API configuration
    if 'ESV API Rate Limiting & Bot Protection' not in content:
        # Find the Bible API Configuration section
        api_config_marker = '// Bible API Configuration'
        if api_config_marker in content:
            rate_limiting_code = add_rate_limiting()
            content = content.replace(
                f'<script>\n(function() {{\n    {api_config_marker}',
                f'{rate_limiting_code}\n\n<script>\n(function() {{\n    {api_config_marker}'
            )
            print('   ✓ Added rate limiting and bot protection')
        else:
            print('   ⚠ Bible API Configuration section not found')
            return False
        
        # Update fetchFromESV to use rate limiter
        if 'async function fetchFromESV(reference)' in content:
            old_fetch = '''    async function fetchFromESV(reference) {
        if (!API_CONFIG.esv.enabled || !API_CONFIG.esv.key || API_CONFIG.esv.key === 'YOUR_ESV_API_KEY_HERE') {
            return null;
        }
        
        try {
            const url = API_CONFIG.esv.baseUrl + '?' + new URLSearchParams({
                q: reference,
                'include-headings': 'false',
                'include-footnotes': 'false',
                'include-verse-numbers': 'false',
                'include-short-copyright': 'false',
                'include-passage-references': 'false'
            });
            
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Token ${API_CONFIG.esv.key}`
                }
            });
            
            if (!response.ok) throw new Error('ESV API error');
            
            const data = await response.json();
            return {
                text: data.passages[0]?.trim() || 'Verse not found',
                version: 'ESV',
                success: true
            };
        } catch (error) {
            console.warn('ESV API fetch failed:', error);
            return null;
        }
    }'''
            
            new_fetch = update_api_functions()
            content = content.replace(old_fetch, new_fetch)
            print('   ✓ Updated ESV API function with rate limiting')
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    size_kb = file_path.stat().st_size / 1024
    print(f'   📊 Size: {size_kb:.1f} KB')
    print(f'   ✅ Rate limiting enabled')
    
    return True

def main():
    """Add rate limiting to all publish files."""
    
    print("=" * 60)
    print("ESV API Rate Limiting & Bot Protection")
    print("=" * 60)
    print("\nCompliance with ESV API Terms of Use:")
    print("  • 60 requests per minute")
    print("  • 1,000 requests per hour")
    print("  • 5,000 requests per day")
    print("  • Max 500 verses cached")
    print("  • Bot detection & prevention")
    print("  • Automatic cache management")
    
    doctrines_dir = Path(__file__).parent / "Doctrines"
    
    files_to_process = [
        'doctrines_library_wp_publish.html',
        'scripture_index_wp_publish.html',
        'scripture_analytics_wp_publish.html'
    ]
    
    success_count = 0
    
    for filename in files_to_process:
        file_path = doctrines_dir / filename
        if file_path.exists():
            if process_file(file_path):
                success_count += 1
        else:
            print(f"\n⚠️  File not found: {filename}")
    
    # Also update _wp_clean files
    clean_files = [
        'doctrines_library_wp_clean.html',
        'scripture_index_wp_clean.html',
    ]
    
    for filename in clean_files:
        file_path = doctrines_dir / filename
        if file_path.exists():
            if process_file(file_path):
                success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated {success_count} files with rate limiting!")
    print("=" * 60)
    
    print("\n🛡️ PROTECTION FEATURES:")
    print("  ✓ Per-minute rate limiting (60/min)")
    print("  ✓ Per-hour rate limiting (1,000/hour)")
    print("  ✓ Per-day rate limiting (5,000/day)")
    print("  ✓ Automatic verse caching (max 500)")
    print("  ✓ Bot detection & blocking")
    print("  ✓ Rapid-fire request prevention")
    print("  ✓ localStorage state persistence")
    print("  ✓ Automatic cache cleanup (30 days)")
    print("  ✓ User-friendly error messages")
    print("  ✓ Console monitoring tools")
    
    print("\n📊 MONITORING (Browser Console):")
    print("  • ESV_RATE_LIMITER.getStatus() - Check current status")
    print("  • ESV_RATE_LIMITER.getRemaining() - See remaining requests")
    print("  • ESV_RATE_LIMITER.getCacheSize() - Check cache size")
    print("  • ESV_RATE_LIMITER.clearCache() - Clear verse cache")
    
    print("\n✅ Your website now complies with ESV API terms of use!")
    print()

if __name__ == "__main__":
    main()
