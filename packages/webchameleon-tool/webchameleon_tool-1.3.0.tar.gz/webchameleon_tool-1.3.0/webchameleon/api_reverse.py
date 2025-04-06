import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from aiohttp import ClientSession, ClientTimeout
from typing import Dict, Optional, Set
import asyncio
from datetime import datetime
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
import random

logger = logging.getLogger("webchameleon.api_reverse")


class ApiReverser:
    def __init__(self):
        self.api_endpoints = set()
        self.session = None
        self.learned_patterns = set()
        self.common_endpoints = [
            "/api/",
            "/v1/",
            "/v2/",
            "/json/",
            "/data/",
            "/endpoint/",
            "/posts",
            "/comments",
            "/users",
            "/todos",
            "/albums",
            "/products",
            "/services",
        ]
        self.retry_options = ExponentialRetry(
            attempts=3, start_timeout=1.0, max_timeout=10.0
        )

    async def detect_api(
        self,
        url: str,
        headers: Dict,
        use_playwright: bool = True,
        max_depth: int = 3,
        interactive_mode: bool = True,
        auth_config: Dict = None,
    ) -> Optional[Dict]:
        self.session = ClientSession(timeout=ClientTimeout(total=15))
        retry_client = RetryClient(
            raise_for_status=False, retry_options=self.retry_options
        )
        try:
            base_url = url.rstrip("/")
            self.api_endpoints.clear()

            # Langkah 1: Ambil respons awal dengan retry
            async with retry_client.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.warning(
                        f"Initial request failed with status {response.status}"
                    )
                    return None
                text = await response.text()

            # Langkah 2: Analisis HTML untuk pola awal
            self._analyze_html_for_api(text, base_url, auth_config)

            # Langkah 3: Simulasi interaksi dengan Playwright
            if use_playwright and interactive_mode:
                await self._simulate_advanced_interactions(
                    base_url, headers, auth_config
                )

            # Langkah 4: Penemuan endpoint heuristik
            await self._discover_endpoints(base_url, headers, max_depth, auth_config)

            if not self.api_endpoints:
                logger.info("No API endpoints detected after exhaustive search.")
                return None

            # Langkah 5: Ambil data dari endpoint
            api_data = {}
            tasks = [
                self._fetch_api_endpoint(endpoint, headers, auth_config)
                for endpoint in self.api_endpoints
            ]
            results = await asyncio.gather(*tasks)
            for endpoint, result in results:
                if result:
                    api_data[endpoint] = result

            if api_data:
                logger.info(f"Detected APIs: {list(api_data.keys())}")
                return {
                    "endpoints": api_data,
                    "last_accessed": datetime.now().isoformat(),
                    "learned_patterns": list(self.learned_patterns),
                }
            return None

        except Exception as e:
            logger.error(f"API detection failed: {e}")
            return None
        finally:
            await retry_client.close()
            if self.session:
                await self.session.close()

    async def _analyze_html_for_api(self, html: str, base_url: str, auth_config: Dict):
        soup = BeautifulSoup(html, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            if script.text:
                api_patterns = [
                    r"(https?://[^\s'\"]+/(api|v\d+)/[^\s'\"]+)",
                    r"(https?://[^\s'\"]+/json/[^\s'\"]+)",
                    r"(['\"])((?:/[^/]+)+)(['\"])\s*:\s*['\"]?(?:get|post|fetch|axios)",
                ]
                for pattern in api_patterns:
                    matches = re.finditer(pattern, script.text)
                    for match in matches:
                        full_url = (
                            match.group(1)
                            if "http" in match.group(0)
                            else urljoin(base_url, match.group(2))
                        )
                        if validate_url(full_url):
                            self.api_endpoints.add(full_url)
                            self.learned_patterns.add(
                                urlparse(full_url).path.split("/")[1]
                            )

    async def _simulate_advanced_interactions(
        self, base_url: str, headers: Dict, auth_config: Dict
    ):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True, args=["--disable-gpu", "--no-sandbox"]
            )
            context = await browser.new_context(user_agent=headers["User-Agent"])
            if auth_config and auth_config.get("cookies"):
                await context.add_cookies(auth_config["cookies"])
            page = await context.new_page()
            page.on(
                "request",
                lambda request: self._capture_api_request(request.url, auth_config),
            )
            page.on("response", lambda response: self._capture_api_response(response))

            try:
                await page.goto(base_url, wait_until="networkidle", timeout=30000)
                await self._interact_with_page(page)
            except PlaywrightTimeoutError:
                logger.warning("Timeout during Playwright simulation.")
            finally:
                await browser.close()

    async def _interact_with_page(self, page):
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        await asyncio.sleep(2)
        elements = await page.query_selector_all("a, button, input, [data-click]")
        for i, elem in enumerate(elements[: min(5, len(elements))]):
            try:
                await elem.click()
                await asyncio.sleep(random.uniform(1, 3))
            except Exception:
                continue
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)

    async def _discover_endpoints(
        self, base_url: str, headers: Dict, max_depth: int, auth_config: Dict
    ):
        visited = set()
        queue = [base_url]
        retry_client = RetryClient(
            raise_for_status=False, retry_options=self.retry_options
        )

        while queue and len(visited) < max_depth:
            current_url = queue.pop(0)
            if current_url in visited:
                continue
            visited.add(current_url)

            for segment in self.common_endpoints + list(self.learned_patterns):
                new_url = urljoin(current_url, segment)
                if new_url not in visited and validate_url(new_url):
                    try:
                        async with retry_client.head(
                            new_url, headers=headers
                        ) as check_response:
                            if check_response.status == 200 and any(
                                fmt
                                in check_response.headers.get(
                                    "Content-Type", ""
                                ).lower()
                                for fmt in ["application/json", "application/xml"]
                            ):
                                self.api_endpoints.add(new_url)
                                self.learned_patterns.add(
                                    segment.split("/")[0] if "/" in segment else segment
                                )
                            elif check_response.status in [301, 302]:
                                redirect_url = check_response.headers.get("Location")
                                if redirect_url and validate_url(redirect_url):
                                    queue.append(redirect_url)
                    except aiohttp.ClientError:
                        continue

    async def _fetch_api_endpoint(
        self, endpoint: str, headers: Dict, auth_config: Dict
    ) -> tuple:
        try:
            enhanced_headers = headers.copy()
            if auth_config:
                enhanced_headers.update(auth_config.get("headers", {}))
            async with self.session.get(endpoint, headers=enhanced_headers) as response:
                content_type = response.headers.get("Content-Type", "")
                if response.status == 200 and any(
                    fmt in content_type.lower()
                    for fmt in ["application/json", "application/xml"]
                ):
                    data = (
                        await response.json()
                        if "json" in content_type
                        else await response.text()
                    )
                    return endpoint, {
                        "method": "GET",
                        "headers_used": enhanced_headers,
                        "response": data,
                        "content_type": content_type,
                        "status": response.status,
                    }
                return endpoint, None
        except Exception as e:
            logger.warning(f"Failed to fetch {endpoint}: {e}")
            return endpoint, None

    def _capture_api_request(self, url: str, auth_config: Dict):
        parsed = urlparse(url)
        path_segments = parsed.path.split("/")
        if any(
            seg for seg in path_segments if seg in ["api", "v1", "v2", "json", "data"]
        ):
            self.api_endpoints.add(url)
            self.learned_patterns.add(
                path_segments[1] if path_segments[1] else parsed.netloc
            )

    def _capture_api_response(self, response):
        url = response.url
        content_type = response.headers.get("Content-Type", "")
        if response.status == 200 and any(
            fmt in content_type.lower()
            for fmt in ["application/json", "application/xml"]
        ):
            self.api_endpoints.add(url)
            parsed = urlparse(url)
            self.learned_patterns.add(
                parsed.path.split("/")[1]
                if parsed.path.split("/")[1]
                else parsed.netloc
            )


def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
