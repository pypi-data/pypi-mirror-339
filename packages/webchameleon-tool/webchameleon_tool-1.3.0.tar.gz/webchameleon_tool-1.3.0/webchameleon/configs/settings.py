from typing import Dict

DEFAULT_TIMEOUT = 15  # detik
MAX_DEPTH = 10
USER_AGENTS = {
    # Desktop Browsers
    "default": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "chrome_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "firefox_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "edge_windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "safari_mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    # Mobile Browsers
    "mobile_android_chrome": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "mobile_ios_safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "mobile_app": "Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    # Crawler Bots
    "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "duckduckbot": "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)",
    "yandex": "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "baiduspider": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    # Developer/Tools
    "curl": "curl/8.1.2",
    "python_requests": "python-requests/2.31.0",
    "wget": "Wget/1.21.1 (linux-gnu)",
    # Social Media Crawlers
    "facebook_externalhit": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "twitterbot": "Twitterbot/1.0",
    "linkedinbot": "Mozilla/5.0 (compatible; LinkedInBot/1.0; +http://www.linkedin.com)",
}

ADVANCED_CONFIG = {
    "retry_attempts": 3,
    "max_parallel_tasks": 10,
    "default_auth": {"headers": {"Authorization": "Bearer dummy_token"}},
}
