import asyncio
import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
from .structure import StructureAnalyzer
from .disguise import DisguiseManager
from .api_reverse import ApiReverser
from .relations import RelationMapper
from .storage import StorageManager
from .exceptions import ConnectionBlockedError, InvalidTargetError
from .utils.logger import log_action
from .utils.helpers import validate_url, sanitize_data, extract_features
from .utils.timers import AdaptiveTimer
from .configs.settings import DEFAULT_TIMEOUT, MAX_DEPTH, USER_AGENTS, ADVANCED_CONFIG
from cachetools import LRUCache, TTLCache
from aiohttp import ClientSession, ClientTimeout
from aiolimiter import AsyncLimiter
from aiohttp_retry import RetryClient, ExponentialRetry
import random
import time
import aiohttp


class WebChameleon:
    def __init__(
        self,
        target: str,
        disguise_as: str = "default",
        auto_learn: bool = True,
        max_concurrent: int = 5,
        auth_config: Optional[Dict] = None,
        custom_settings: Optional[Dict] = None,
    ):
        if not validate_url(target):
            raise InvalidTargetError(
                "Target URL must be valid and start with http:// or https://"
            )
        self.target = target
        self.session = requests.Session()
        self.async_session = None
        self.session.timeout = DEFAULT_TIMEOUT
        self.disguise = DisguiseManager(mode=disguise_as)
        self.analyzer = StructureAnalyzer()
        self.api_reverser = ApiReverser()
        self.mapper = RelationMapper()
        self.storage = StorageManager()
        self.auto_learn = auto_learn
        self.max_concurrent = max_concurrent
        self.rate_limit = AsyncLimiter(max_concurrent, DEFAULT_TIMEOUT)
        self.cache = {
            "short_term": LRUCache(maxsize=1000),
            "long_term": TTLCache(maxsize=5000, ttl=3600),
        }
        self.status_log = {
            "pages_scraped": 0,
            "blocks_encountered": 0,
            "recovery_attempts": 0,
            "features": {},
        }
        self.timer = AdaptiveTimer()
        self.auth_config = auth_config or {}
        self.custom_settings = custom_settings or {}
        self.retry_options = ExponentialRetry(
            attempts=3, start_timeout=1.0, max_timeout=10.0
        )
        self.fallback_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    async def analyze_structure(self) -> Optional[Dict]:
        try:
            headers = self._get_enhanced_headers()
            session = await self._get_async_session()
            async with session as s:
                async with self.rate_limit:
                    async with s.get(
                        self.target,
                        headers=headers,
                        timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
                    ) as response:
                        if response.status == 400:
                            log_action(
                                "Status 400 detected, retrying with fallback headers"
                            )
                            async with s.get(
                                self.target,
                                headers=self.fallback_headers,
                                timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
                            ) as fallback_response:
                                if fallback_response.status != 200:
                                    self._handle_block(fallback_response.status)
                                    return None
                                text = await fallback_response.text()
                        else:
                            if response.status != 200:
                                self._handle_block(response.status)
                                return None
                            text = await response.text()
            structure = self.analyzer.analyze(text, self.target)
            self.status_log["features"].update(extract_features(structure))
            log_action(
                f"Structure analyzed for {self.target} with features {self.status_log['features']} in {self.timer.elapsed():.2f}s"
            )
            return structure
        except Exception as e:
            self._handle_block(getattr(e, "status", 500))
            return None

    async def scrape(
        self,
        target_elements: Optional[Dict] = None,
        depth: int = MAX_DEPTH,
        adaptive_depth: bool = True,
    ) -> List[Dict]:
        self.async_session = ClientSession()
        retry_client = RetryClient(
            raise_for_status=False, retry_options=self.retry_options
        )
        try:
            data = []
            urls_visited = set()
            urls_to_visit = [self.target]
            tasks = []

            effective_depth = (
                depth if not adaptive_depth else self._adjust_depth_based_on_response()
            )
            while urls_to_visit and len(urls_visited) < effective_depth:
                url = urls_to_visit.pop(0)
                if url in urls_visited or url in self.cache["short_term"]:
                    continue
                tasks.append(self._scrape_page(url, target_elements, retry_client))
                if len(tasks) >= self.max_concurrent:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    data.extend(
                        [r for r in results if not isinstance(r, Exception) and r]
                    )
                    tasks = []

            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                data.extend([r for r in results if not isinstance(r, Exception) and r])

            log_action(f"Scraped {len(data)} pages in {self.timer.elapsed():.2f}s")
            return data
        finally:
            await retry_client.close()
            if self.async_session:
                await self.async_session.close()

    async def _scrape_page(
        self, url: str, target_elements: Optional[Dict], retry_client: RetryClient
    ) -> Optional[Dict]:
        headers = self._get_enhanced_headers()
        async with self.rate_limit:
            try:
                async with retry_client.get(
                    url, headers=headers, timeout=ClientTimeout(total=DEFAULT_TIMEOUT)
                ) as response:
                    if response.status == 400:
                        log_action(
                            "Status 400 detected in scrape, retrying with fallback headers"
                        )
                        async with retry_client.get(
                            url,
                            headers=self.fallback_headers,
                            timeout=ClientTimeout(total=DEFAULT_TIMEOUT),
                        ) as fallback_response:
                            if fallback_response.status != 200:
                                self._handle_block(fallback_response.status)
                                return None
                            text = await fallback_response.text()
                    else:
                        if response.status != 200:
                            self._handle_block(response.status)
                            return None
                        text = await response.text()
                    page_data = self.analyzer.extract_data(
                        text, target_elements or self._infer_elements(text)
                    )
                    if self.auto_learn:
                        self.analyzer.update_patterns(page_data)
                    self.cache["short_term"][url] = page_data
                    self.cache["long_term"][url] = page_data
                    self.status_log["pages_scraped"] += 1
                    urls_to_visit = self.analyzer.find_links(text, self.target)
                    return sanitize_data(page_data)
            except aiohttp.ClientError as e:
                self._handle_block(500)
                return None

    async def reverse_api(
        self,
        use_playwright: bool = True,
        max_depth: int = 3,
        interactive_mode: bool = True,
    ) -> Optional[Dict]:
        try:
            headers = self._get_enhanced_headers()
            api_info = await self.api_reverser.detect_api(
                self.target,
                headers,
                use_playwright,
                max_depth,
                interactive_mode,
                self.auth_config,
            )
            if api_info:
                log_action(
                    f"API reversed for {self.target} with {len(api_info.get('endpoints', {}))} endpoints in {self.timer.elapsed():.2f}s"
                )
                return api_info
            return None
        except Exception as e:
            log_action(f"API reverse failed: {e}")
            return None

    async def map_relations(
        self,
        data: Optional[List[Dict]] = None,
        output_file: Optional[str] = None,
        weight_threshold: float = 0.5,
    ) -> Optional[Dict]:
        if not data:
            data = await self.scrape()
        relations = self.mapper.build_enhanced_graph(data, weight_threshold)
        if output_file:
            self.mapper.save_graph(relations, output_file, include_visualization=True)
            log_action(
                f"Relations saved to {output_file} with visualization in {self.timer.elapsed():.2f}s"
            )
        return relations

    async def save(
        self,
        data: List[Dict],
        filename: str,
        format: str = "json",
        compress: bool = False,
    ):
        try:
            await asyncio.to_thread(
                self.storage.save_advanced, data, filename, format, compress
            )
            log_action(
                f"Data saved to {filename} in {self.timer.elapsed():.2f}s with format {format}"
            )
        except Exception as e:
            log_action(f"Save failed: {e}")

    def status(self) -> Dict[str, Any]:
        self.status_log["timestamp"] = datetime.now().isoformat()
        self.status_log["total_runtime"] = self.timer.elapsed()
        self.status_log["cache_size"] = {k: len(v) for k, v in self.cache.items()}
        return self.status_log

    def _handle_block(self, status_code: int):
        self.status_log["blocks_encountered"] += 1
        self.status_log["recovery_attempts"] += 1
        strategies = [
            self._switch_disguise,
            self._add_delay_and_retry,
            self._adjust_rate_limit,
        ]
        strategy = random.choice(strategies)
        recovery_result = strategy(status_code)
        self.status_log["last_recovery"] = recovery_result

    def _switch_disguise(self, status_code: int) -> str:
        new_mode = self.disguise.switch_mode()
        log_action(f"Blocked ({status_code}), switched to {new_mode}")
        return f"Switched to {new_mode}"

    def _add_delay_and_retry(self, status_code: int) -> str:
        delay = self.timer.adaptive_delay(status_code)
        time.sleep(delay)
        log_action(
            f"Blocked ({status_code}), added adaptive delay of {delay:.2f}s and retrying"
        )
        return f"Added delay of {delay:.2f}s"

    def _adjust_rate_limit(self, status_code: int) -> str:
        self.rate_limit = AsyncLimiter(
            int(self.max_concurrent / 2), DEFAULT_TIMEOUT * 2
        )
        log_action(
            f"Blocked ({status_code}), adjusted rate limit to {self.max_concurrent / 2} concurrent requests"
        )
        return "Adjusted rate limit"

    def _get_enhanced_headers(self) -> Dict:
        headers = self.disguise.get_headers()
        if self.auth_config:
            headers.update(self.auth_config.get("headers", {}))
        return headers

    def _infer_elements(self, html: str) -> Dict:
        return self.analyzer.infer_selectors(html)

    def _adjust_depth_based_on_response(self) -> int:
        return min(
            MAX_DEPTH,
            int(MAX_DEPTH * (1 - self.status_log.get("blocks_encountered", 0) / 10)),
        )

    async def _get_async_session(self) -> ClientSession:
        if not self.async_session:
            self.async_session = ClientSession(
                timeout=ClientTimeout(total=DEFAULT_TIMEOUT)
            )
        return self.async_session
