import random
from typing import Dict, Optional
import uuid
from faker import Faker
import brotli


class DisguiseManager:
    def __init__(self, mode: str = "default", locale: str = "en_US"):
        self.mode = mode
        self.fake = Faker(locale)
        self.user_agents = {
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

    def get_headers(self, session_id: Optional[str] = None) -> Dict:
        mode_agents = self.user_agents.get(self.mode, self.user_agents["default"])
        # Tentukan encoding yang didukung
        try:
            import brotli

            encoding = "gzip, deflate, br"
        except ImportError:
            encoding = "gzip, deflate"

        headers = {
            "User-Agent": mode_agents,
            "Accept": "text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": encoding,
            "Connection": "keep-alive",
        }
        # Hanya tambahkan header tambahan untuk mode tertentu
        if self.mode not in ["googlebot", "default"]:
            headers.update(
                {
                    "Referer": self.fake.url(),
                    "X-Forwarded-For": self.fake.ipv4(),
                    "X-Request-ID": session_id or str(uuid.uuid4()),
                }
            )
        return headers

    def switch_mode(self, randomize: bool = False) -> str:
        modes = list(self.user_agents.keys())
        if randomize:
            self.mode = random.choice(modes)
        else:
            current_idx = modes.index(self.mode) if self.mode in modes else -1
            self.mode = modes[(current_idx + 1) % len(modes)]
        return self.mode

    def mimic_behavior(self, pattern: str = "browsing") -> Dict:
        behaviors = {
            "browsing": {"Cache-Control": "no-cache", "Pragma": "no-cache"},
            "crawling": {"If-Modified-Since": self.fake.date_time().isoformat()},
            "api_call": {"Content-Type": "application/json"},
        }
        return behaviors.get(pattern, {})
