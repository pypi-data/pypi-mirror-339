from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from typing import Dict, List, Optional
import nltk
from collections import defaultdict
import heapq


class StructureAnalyzer:
    def __init__(self):
        self.patterns = {
            "content_selectors": ["div.content", "article", "section.main"],
            "link_patterns": [
                r"(https?://[^\s'\"]+)",
                r"data-href=['\"]([^'\"]+)['\"]",
            ],
        }
        self.learned_patterns = []
        self.tag_frequency = defaultdict(int)
        nltk.download("punkt")

    def analyze(self, html: str, base_url: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        return {
            "navigation": self._find_navigation(soup),
            "content_blocks": self._find_content_blocks(soup),
            "dynamic_elements": self._find_dynamic_elements(soup),
            "lazy_loaded": self._detect_lazy_load(soup),
            "javascript_events": self._analyze_javascript_events(soup),
            "semantic_analysis": self._semantic_analysis(soup),
        }

    def extract_data(self, html: str, target_elements: Optional[Dict] = None) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        data = {}
        if target_elements:
            data = {
                key: soup.select_one(selector).text.strip()
                for key, selector in target_elements.items()
                if soup.select_one(selector)
            }
        else:
            inferred = self.infer_selectors(html)
            for key, selector in inferred.items():
                element = soup.select_one(selector)
                if element:
                    data[key] = element.text.strip()
        data["title"] = soup.title.string if soup.title else "N/A"
        return data

    def infer_selectors(self, html: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")
        selectors = {}
        for tag in soup.find_all(["h1", "h2", "p", "div"]):
            classes = tag.get("class", ["generic"])
            if classes and any(c for c in classes if len(c) > 2):
                key = f"{tag.name}_{classes[0]}"
                selectors[key] = f"{tag.name}.{classes[0]}"
                self.tag_frequency[f"{tag.name}.{classes[0]}"] += 1
        return dict(
            heapq.nlargest(3, selectors.items(), key=lambda x: self.tag_frequency[x[1]])
        )

    def find_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        links = [
            urljoin(base_url, a["href"])
            for a in soup.find_all("a", href=True)
            if a["href"]
        ]
        scripts = soup.find_all("script")
        for script in scripts:
            for pattern in self.patterns["link_patterns"]:
                matches = re.finditer(pattern, script.text)
                links.extend(match.group(1) for match in matches if match.group(1))
        return list(set(links))

    def _find_navigation(self, soup):
        nav = soup.find("nav")
        return {
            "main_menu": (
                [a["href"] for a in nav.find_all("a", href=True)] if nav else []
            )
        }

    def _find_content_blocks(self, soup):
        blocks = []
        for tag in soup.find_all(["div", "article", "section", "main"]):
            classes = tag.get("class", ["generic"])
            if classes or tag.name:
                block_data = {
                    "type": tag.name,
                    "selector": (
                        ".".join(classes) if classes != ["generic"] else tag.name
                    ),
                    "count": len(tag.find_all(recursive=False)),
                    "attributes": dict(tag.attrs),
                    "text_density": (
                        len(tag.text.split()) / len(tag.text) if tag.text else 0
                    ),
                }
                blocks.append(block_data)
        return sorted(blocks, key=lambda x: x["text_density"], reverse=True)[:5]

    def _find_dynamic_elements(self, soup):
        scripts = soup.find_all("script")
        return {
            "xhr_detected": any(
                "xhr" in script.text.lower() or "fetch" in script.text.lower()
                for script in scripts
            ),
            "event_listeners": any(
                "addEventListener" in script.text.lower() for script in scripts
            ),
            "inline_scripts": len(scripts) > 0,
            "interaction_points": len(soup.find_all(["a", "button", "input"])),
        }

    def _detect_lazy_load(self, soup):
        attrs = ["data-src", "data-lazy", "loading='lazy'", "srcset"]
        return any(
            any(attr in str(tag) for attr in attrs)
            for tag in soup.find_all(["img", "iframe", "video"])
        )

    def _analyze_javascript_events(self, soup):
        events = {}
        scripts = soup.find_all("script")
        for script in scripts:
            if script.text:
                event_matches = re.finditer(
                    r"addEventListener\(['\"]([^'\"]+)['\"]", script.text
                )
                for match in event_matches:
                    events[match.group(1)] = True
        return events if events else {"none": True}

    def _semantic_analysis(self, soup):
        text = soup.get_text()
        sentences = nltk.sent_tokenize(text)
        return {
            "sentence_count": len(sentences),
            "avg_sentence_length": (
                sum(len(nltk.word_tokenize(s)) for s in sentences) / len(sentences)
                if sentences
                else 0
            ),
            "key_phrases": nltk.pos_tag(nltk.word_tokenize(text))[
                :5
            ],  # Ambil 5 frase utama
        }

    def update_patterns(self, data: Dict):
        if "content" in data and data["content"]:
            content_preview = data["content"][:20].replace(" ", "_")
            new_selector = f"div:contains('{content_preview}')"
            if (
                new_selector not in self.patterns["content_selectors"]
                and new_selector not in self.learned_patterns
            ):
                self.learned_patterns.append(new_selector)
                self.patterns["content_selectors"].append(new_selector)
